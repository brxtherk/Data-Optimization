# 예제 1

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
from ortools.linear_solver import pywraplp

plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['figure.figsize'] = (8, 5)

# 데이터 불러오기
sales = pd.read_csv('sales_log.csv',     parse_dates=['date'])
prod = pd.read_csv('production_log.csv', parse_dates=['date'])
res = pd.read_csv('resource_today.csv')

print("=== 판매 기록 ===")
print(sales.head())
print("\n=== 생산 로그 ===")
print(prod.head())

# 일별 제품별 판매량 집계
daily = (sales
         .groupby(['date', 'product'])['quantity']
         .sum()
         .unstack())
print("기초 통계:")
print(daily.describe().round(1))

import platform

if platform.system() == 'Windows':
    plt.rcParams['font.family'] = 'Malgun Gothic'  # 맑은 고딕
elif platform.system() == 'Darwin':
    plt.rcParams['font.family'] = 'AppleGothic'
else: # Linux(Colab 등)
    plt.rcParams['font.family'] = 'NanumGothic'

plt.rcParams['axes.unicode_minus'] = False

# 박스플롯으로 분포 확인
fig, axes = plt.subplots(1, 2, figsize=(10,4))
for ax, col, color in zip(axes, ['A', 'B'], ['steelblue', 'tomato']):
    daily[col].plot(kind='box', ax=ax, color=color, patch_artist=True)
    ax.set_title(f'빵 {col} 일별 판매량 분포')
    ax.set_ylabel('판매량 (개)')

plt.tight_layout()
plt.show()

# 이상치 제거 (IQR 방법)
def remove_outliers(s):
    Q1, Q3 = s.quantile(0.25), s.quantile(0.75)
    return s[(s >= Q1 - 1.5*(Q3-Q1)) & (s <= Q3 + 1.5*(Q3-Q1))]

daily_clean = daily.apply(remove_outliers)

# 수요 파라미터: 75분위 사용(재고 부족 방지)
## 첫 풀이에는 75분위 수를 쓴다.
D = daily_clean.quantile(0.75)
print("\n 평균 또는 75분위?")
print(f"평균 A = {daily_clean['A'].mean():.0f}, B = {daily_clean['B'].mean():.0f}")
print(f"75%: A = {D['A']:.0f}, B = {D['B']:.0f} <- 더 보수적, 기회 손실 감소")

# 판매가(평균)
unit_price = sales.groupby('product')['price'].mean()
print("평균 판매가:")
print(unit_price.round(0))

fig, axes = plt.subplots(1, 2, figsize=(11, 4))
unit_vc = {}

for ax, pid, color in zip(axes, ['A', 'B'], ['steelblue', 'tomato']):
    grp = prod[prod['product'] == pid]
    X = sm.add_constant(grp['quantity'])
    model = sm.OLS(grp['total_cost'], X).fit()  # 회귀분석

    fixed_cost = model.params['const']
    var_cost = model.params['quantity']  # 단위 변동비
    unit_vc[pid] = var_cost

    # 산점도 + 회귀선
    ax.scatter(grp['quantity'], grp['total_cost'], alpha=0.5, color=color, label='실제 데이터')
    x_line = np.linspace(grp['quantity'].min(), grp['quantity'].max(), 100)
    ax.plot(x_line, model.params['const'] + model.params['quantity']*x_line,
            color='black', linewidth=2, label='회귀선')
    ax.set_title(f'빵 {pid}: 총원가 vs 생산량\n고정비={fixed_cost:,.0f}원 변동비={var_cost:,.0f}원/R2={model.rsquared:.3f}')
    ax.set_xlabel('생산량 (개)'); ax.set_ylabel('총원가 (원)')
    ax.legend()

plt.tight_layout()
plt.show()

print("\n단위 변동비 (회귀 기울기):")
for k, v in unit_vc.items():
    print(f"빵 {k}: {v:,.0f}원")

# 단위 이익 계산
p = {pid: unit_price[pid] - unit_vc[pid] for pid in ['A', 'B']}
print("단위 이익 p:")
for k, v in p.items():
    print(f"빵 {k}: {unit_price[k]:,.0f}원(판매가) - {unit_vc[k]:,.0f}원(변동비) = {v:,.0f}원")

# 단위당 오븐 시간 & 재료 사용량 (생산 로그 평균)
resource_params = (prod
                   .groupby('product')
                   .apply(lambda x: pd.Series({
                       'a (오븐시간/개)': x['oven_hours'].sum() / x['quantity'].sum(),
                       'm (재료kg/개)': x['material_kg'].sum() / x['quantity'].sum()
                   })))

print(resource_params.round(3))

a = resource_params['a (오븐시간/개)'].to_dict()
m = resource_params['m (재료kg/개)'].to_dict()

# 오늘 가용 자원
CAP = res.loc[0, 'available_oven_hours']
MAT = res.loc[0, 'available_material_kg']
print(f"\n오늘 가용 오븐: {CAP}시간")
print(f"오늘 가용 재료: {MAT}kg")

params = pd.DataFrame({
    '파라미터': ['p(단위이익, 원)', 'a(오븐시간/개)', 'm(재료kg/개)', 'D(수요상한, 개)'],
    '빵 A': [round(p['A'],0), round(a['A'],3), round(m['A'],3), round(D['A'],0)],
    '빵 B': [round(p['B'],0), round(a['B'],3), round(m['B'],3), round(D['B'],0)],
    '추출 방법': ['판매가 평균 - 회귀 변동비', '생산로그 집계', '생산로그 집계', '판매기록 75분위']
})

## LP 모형 수립 및 풀이
solver = pywraplp.Solver.CreateSolver('GLOP')

# ======== 변수 선언 (하한=0, 상한=무한대)=========
inf = solver.infinity()
xA = solver.NumVar(0, inf, 'xA')
xB = solver.NumVar(0, inf, 'xB')

# =======제약 조건=================
solver.Add(a['A']*xA + a['B']*xB <= CAP)  # 오븐 용량
solver.Add(m['A']*xA + m['B']*xB <= MAT)  # 재료 한도
solver.Add(xA <= D['A'])    # 수요 상한 A
solver.Add(xB <= D['B'])    # 수요 상한 B

# ========목적함수(최대화)=======
solver.Maximize(p['A']*xA + p['B']*xB)

# ======풀이=========
status = solver.Solve()

# status 코드: 0=OPTIMAL, 1=FEASIBLE, 2=INFEASIBLE, 3=UNBOUNDED
status_map = {0: 'OPTIMAL', 1: 'FEASIBLE', 2: 'INFEASIBLE', 3: 'UNBOUNDED'}
print(f"풀이 상태: {status_map.get(status, status)}")
print()

xA_val = xA.solution_value()
xB_val = xB.solution_value()
obj_val = solver.Objective().Value()
print(f"최적 생산량: 빵 A = {xA_val:.0f}개, 빵 B = {xB_val:.0f}개")
print(f"최대 이익: {obj_val:,.0f}원")
print()
print(f"오븐 사용: {a['A']*xA_val + a['B']*xB_val:.1f} / {CAP} 시간")
print(f"재료 사용: {m['A']*xA_val + m['B']*xB_val:.1f} / {MAT} kg")

## LP모형 결과 시각화

# 실행 가능 영영 시각화
fig, ax = plt.subplots(figsize=(8, 7))

xv = np.linspace(0, D['A'] * 1.3, 400)

# 제약 경계선
y_oven = (CAP - a['A'] * xv) / a['B']
y_mat = (MAT - m['A'] * xv) / m['B']

ax.plot(xv, np.clip(y_oven, 0, None), label=f'오븐 용량 ({CAP}h)', color='steelblue', linewidth=2)
ax.plot(xv, np.clip(y_mat, 0, None), label=f'재료 한도 ({MAT}kg)', color='orange', linewidth=2)
ax.axvline(D['A'], color='gray', linestyle='--', linewidth=1.5, label=f'수요 상한 A ({D["A"]:.0f}개)')
ax.axhline(D['B'], color='green', linestyle='--', linewidth=1.5, label=f'수요 상한 B ({D["B"]:.0f}개)')

# 실행 가능 영역 색칠 
yf = np.minimum(np.minimum(y_oven, y_mat), D['B'])
yf = np.clip(yf, 0, None)
mask = xv <= D['A']
ax.fill_between(xv[mask], 0, yf[mask], alpha=0.15, color='steelblue', label='실행 가능 영역')

# 최적해 (Or-Tools 결과 사용)
ax.scatter(xA_val, xB_val, color='red', zorder=5, s=150)
ax.annotate(f"최적해\n({xA_val:.0f}개, {xB_val:.0f}개\n이익 {obj_val:,.0f}원",
            xy=(xA_val, xB_val),
            xytext=(xA_val + 5, xB_val + 5),
            fontsize=10,
            bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7))

ax.set_xlim(0, D['A'] * 1.3)
ax.set_ylim(0, D['B'] * 1.5)
ax.set_xlabel('빵 A 생산량 (개)', fontsize=12)
ax.set_ylabel('빵 B 생산량 (개)', fontsize=12)
ax.set_title('생산계획 LP - 실행 가능 영역 및 최적해', fontsize=13)
ax.legend(loc='upper right')
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

## 민감도 분석
def solve_lp(p_A, p_B, D_A, D_B):
    """OR-Tools로 LP를 풀고 (최적이익, xA, xB) 반환"""
    s = pywraplp.Solver.CreateSolver('GLOP')
    inf = s.infinity()
    xA2 = s.NumVar(0, inf, 'xA')
    xB2 = s.NumVar(0, inf, 'xB')
    s.Add(a['A'] * xA2 + a['B'] * xB2 <= CAP)
    s.Add(m['A'] * xA2 + m['B'] * xB2 <= MAT)
    s.Add(xA2 <= D_A)
    s.Add(xB2 <= D_B)
    s.Maximize(p_A * xA2 + p_B * xB2)
    s.Solve()
    return s.Objective().Value(), xA2.solution_value(), xB2.solution_value()

scales = np.linspace(0.7, 1.3, 13)

# 수요 파라미터 변화 vs 이익
profits_D = [solve_lp(p['A'], p['B'], D['A']*s, D['B']*s)[0] for s in scales]

# 단위이익 파라미터 변화 vs 이익
profits_p = [solve_lp(p['A']*s, p['B']*s, D['A'], D['B'])[0] for s in scales]

fig, axes = plt.subplots(1, 2, figsize=(12, 4))

for ax, profits, title, color in zip(
    axes,
    [profits_D, profits_p],
    ['수요 파라미터 추정 오차 -> 이익 변화', '단위이익 파라미터 오차 -> 이익 변화'],
    ['steelblue', 'tomato']
):
    ax.plot(scales, profits, marker='o', color=color, linewidth=2)
    ax.axvline(1.0, color='black', linestyle='--', label='기준 (오차 0%)')
    ax.set_xlabel('파라미터 추정 배율 (1.0 = 정확)')
    ax.set_ylabel('최적 이익 (원)')
    ax.set_title(title)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:,.0f}'))
    ax.legend(); ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

print("파라미터 오차가 클수록 의사결정 품질이 떨어집니다.")
print(f" 수요를 30% 과대 추정 시 -> 실현 이익 하락 가능성")
print(f" 단위이익을 30% 과소 추정 시 -> 수익성 높은 제품 과소 생산")

# 수요를 과대 추정(1.3 방향)하더라도 자원 제약(오븐, 재료)으로 인해 실제 실현 가능한 이익은 정체됩니다. 즉, 무작정 수요를 높게 예측한다고 해서 이익이 무한정 늘어나지 않는 '자원 병목' 상태임을 시각적으로 확인할 수 있습니다

# 실습

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
from ortools.linear_solver import pywraplp

plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['figure.figsize'] = (8, 5)

import platform

if platform.system() == 'Windows':
    plt.rcParams['font.family'] = 'Malgun Gothic'  # 맑은 고딕
elif platform.system() == 'Darwin':
    plt.rcParams['font.family'] = 'AppleGothic'
else: # Linux(Colab 등)
    plt.rcParams['font.family'] = 'NanumGothic'

plt.rcParams['axes.unicode_minus'] = False

# 파일로부터 데이터 읽기
capacity = pd.read_csv('capacity_today.csv')
demand = pd.read_csv('contract_demand.csv')
delivery = pd.read_csv('delivery_log.csv', parse_dates=['week_start'])

print("===== 배송 로그 =====")
print(delivery.head())

# 데이터 분석하여 파라미터 추정

D = dict(zip(demand['route'], demand['weekly_min_deliveries'] / 7))
routes = D.keys()

resource_params = (delivery
                   .groupby('route')
                   .apply(lambda x: pd.Series({
                       'c (비용/건)': (x['weekly_cost'].sum()/7) / x['num_deliveries'].sum(),
                       'h (기사시간/건)': x['driver_hours'].sum() / x['num_deliveries'].sum(),
                       'f (연료/건)' : x['fuel_liters'].sum() / x['num_deliveries'].sum()
                   })))
c = resource_params['c (비용/건)'].to_dict()
h = resource_params['h (기사시간/건)'].to_dict()
f = resource_params['f (연료/건)'].to_dict()


# 오늘 가용 자원
CAP = capacity.loc[0, 'available_driver_hours']
FUEL = capacity.loc[0, 'available_fuel_liters']
print(f"\n오늘 가용 기사시간: {CAP}")
print(f"오늘 가용 연료량: {FUEL}")

params = pd.DataFrame({
    '파라미터' : ['c (단위비용, 건)', 'h (단위 기사시간/건)', 'f (단위 연료량/건)', 'D (수요 상한, 건)'],
    '노선 A' : [round(c['A'], 0), round(h['A'], 3), round(f['A'], 3), round(D['A'])],
    '노선 B' : [round(c['B'], 0), round(h['B'], 3), round(f['B'], 3), round(D['B'])]
    })
print("=" * 60)
print("LP 투입 파라미터 Summary")
print("=" * 60)
print(params.to_string(index=False))
print(f"\n CAP (가용 기사시간) = {CAP}h")
print(f" FUEL (가용 연료량) = {FUEL}l")

solver = pywraplp.Solver.CreateSolver("GLOP")

# 변수 선언
inf = solver.infinity()
xA = solver.NumVar(D['A'], inf,  "xA")
xB = solver.NumVar(D['B'], inf, "xB")

# 제약조건
solver.Add(h['A']*xA + h['B']*xB <= CAP)
solver.Add(f['A']*xA + f['B']*xB <= FUEL)

# 목적함수
solver.Minimize(c['A']*xA + c['B']*xB)

# 풀이
status = solver.Solve()

# status 코드 : 0=OPTIMAL, 1=FEASIBLE, 2=INFEASIBLE, 3=UNBOUNDED
status_map = {0: 'OPTIMAL', 1: 'FEASIBLE', 2: 'INFEASIBLE', 3: 'UNBOUNDED'}
print(f"풀이상태: {status_map.get(status, status)}")
print()
xA_val = xA.solution_value()
xB_val = xB.solution_value()
obj_val = solver.Objective().Value()
print(f"최적 배송 건수: 노선 A = {xA_val:.0f} 건, 노선 B = {xB_val:.0f} 건")
print(f"최소비용: {obj_val:,.0f} 원")
print()
print(f"가용 기사시간: {h['A'] * xA_val + h['B'] * xB_val:.1f} / {CAP} h")
print(f"가용 연료량: {f['A'] * xA_val + f['B'] * xB_val:.1f} / {FUEL} l")

# 실행 가능영역 시각화
fig, ax = plt.subplots(figsize=(8, 7))

xv = np.linspace(0, D['A'] * 3, 500)

# 제약 경계선
y_time = (CAP - h['A'] * xv) / h['B']
y_fuel = (FUEL - f['A'] * xv) / f['B']

ax.plot(xv, np.clip(y_time, 0, None), label=f'기사 시간 한도 ({CAP}h)', color='steelblue', linewidth=2)
ax.plot(xv, np.clip(y_fuel, 0, None), label=f'연료량 한도 ({FUEL}L)', color='orange', linewidth=2)
ax.axvline(D['A'], color='red', linestyle='--', linewidth=1.5, label=f"최소 계약 A ({D['A']:.0f}건)")
ax.axhline(D['B'], color='green', linestyle='--', linewidth=1.5, label=f"최소 계약 B ({D['B']:.0f}건)")

#실행 가능 영역(Feasible Region) 색칠
y_top = np.minimum(y_time, y_fuel)
y_top = np.clip(y_top, D['B'], None)

mask = xv >= D['A']
ax.fill_between(xv[mask], D['B'], y_top[mask], alpha=0.2, color='skyblue', label='배송 가능 영역')

# 5. 최적해 표시 (솔버 결과가 성공일 때만)
if status == 0:
    ax.scatter(xA_val, xB_val, color='red', zorder=5, s=150)
    ax.annotate(f"최적 배송안\n(A:{xA_val:.1f}건, B:{xB_val:.1f}건)\n최소비용: {obj_val:,.0f}원",
                xy=(xA_val, xB_val),
                xytext=(xA_val + 2, xB_val + 2),
                fontsize=10,
                bbox=dict(boxstyle='round,pad=0.4', facecolor='yellow', alpha=0.7))

# 6. 그래프 마무리 (데코레이션)
ax.set_xlim(0, D['A'] * 2.5)
ax.set_ylim(0, D['B'] * 2.5)
ax.set_xlabel('노선 A 배송 건수 (건)', fontsize=12)
ax.set_ylabel('노선 B 배송 건수 (건)', fontsize=12)
ax.set_title('배송 노선 최적화 — 실행 가능 영역 및 최적해', fontsize=14, pad=15)
ax.legend(loc='upper right', fontsize=10)
ax.grid(True, alpha=0.3, linestyle=':')

plt.tight_layout()
plt.show()

## 민감도 분석

def solve_lp(c_A, c_B, D_A, D_B):
    s = pywraplp.Solver.CreateSolver("GLOP")
    inf = s.infinity()
    xA2 = s.NumVar(D_A, inf, 'xA')
    xB2 = s.NumVar(D_B, inf, 'xB')
    s.Add(h['A']*xA2 + h['B']*xB2 <= CAP)
    s.Add(f['A']*xA2 + f['B']*xB2 <= FUEL)
    s.Minimize(c_A*xA2 + c_B*xB2)
    s.Solve()
    return s.Objective().Value(), xA2.solution_value(), xB2.solution_value()

scales = np.linspace(0.7, 1.5, 17)

# 수요 파라미터 변화vs이익
costs_D_AB = [solve_lp(c['A'], c['B'], D['A']*s, D['B']*s)[0] for s in scales]
costs_D_A = [solve_lp(c['A'], c['B'], D['A']*s, D['B'])[0] for s in scales]
costs_D_B = [solve_lp(c['A'], c['B'], D['A'], D['B']*s)[0] for s in scales]

fig, axes = plt.subplots(1, 3, figsize=(12,4))
for ax, costs, title, color in zip(axes, [costs_D_AB, costs_D_A, costs_D_B],
                                   ['수요 파라미터(A,B) 추정오차 → 이익변화', '수요 파라미터(A) 추정오차 → 이익변화', '수요 파라미터(B) 추정오차 → 이익변화'],
                                   ['steelblue', 'tomato', 'green']):
    ax.plot(scales, costs, marker='o', color=color, linewidth=2)
    ax.axvline(1.0, color='black', linestyle='--')
    ax.set_xlabel('파라미터 추정 배율(1.0 = 정확)')
    ax.set_ylabel('최적 이익 (원)')
    ax.set_title(title)
    ax.grid(True, alpha=0.3)
    
plt.tight_layout()
plt.show()