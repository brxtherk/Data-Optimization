# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 11:42:58 2026

@author: redti
"""
# 예제

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
from ortools.linear_solver import pywraplp

plt.rcParams['font.family'] = 'DejaVuSans'
plt.rcParams['figure.figsize'] = (8, 5)

# 데이터 불러오기
sales = pd.read_csv('sales_log.csv', parse_dates=['date'])
prod = pd.read_csv('production_log.csv', parse_dates=['date'])
res = pd.read_csv('resource_today.csv')

print("=== 판매기록 ===")
print(sales.head())
print("\n=== 생산로그 ===")
print(prod.head())

# 일별 제품별 판매량 집계
daily = (sales
         .groupby(['date', 'product'])['quantity']
         .sum()
         .unstack())

print("기초통계:")
print(daily.describe().round(1))

import platform

if platform.system() == 'Windows':
    plt.rcParams['font.family'] ='Malgun Gothic'# 맑은고딕
elif platform.system() =='Darwin': # macOS
    plt.rcParams['font.family'] = 'AppleGothic'
else: # Linux (Colab등)
    plt.rcParams['font.family'] ='NanumGothic'
    
plt.rcParams['axes.unicode_minus'] =False

# 박스플롯으로 분포 확인
fig, axes = plt.subplots(1, 2, figsize=(10, 4))
for ax, col, color in zip(axes, ['A', 'B'], ['steelblue', 'tomato']):
    daily[col].plot(kind='box', ax=ax, color=color, patch_artist=True)
    ax.set_title(f'빵 {col} 일별 판매량 분포')
    ax.set_ylabel('판매량 (개)')
plt.tight_layout()
plt.show()

# 이상치 제거 (IQR 방법)
def remove_outliers(s):
    Q1, Q3 = s.quantile(0.25), s.quantile(0.75)
    return s[(s >= Q1 - 1.5 * (Q3 - Q1)) & (s <= Q3 + 1.5 * (Q3 - Q1))]

daily_clean = daily.apply(remove_outliers)

# 수요 파라미터: 75분위 사용 (재고부족 방지)
D = daily_clean.quantile(0.75)
print("\n💡 평균 또는 75분위?")
print(f" 평균: A={daily_clean['A'].mean():.0f}, B={daily_clean['B'].mean():.0f}")
print(f" 75%: A={D['A']:.0f}, B={D['B']:.0f} <- 더 보수적, 기회손실 감소")

# 판매가 평균 추출
unit_price = sales.groupby('product')['price'].mean()
print("평균 판매가:")
print(unit_price.round(0))

fig, axes = plt.subplots(1, 2, figsize=(11, 4))
unit_vc = {}
for ax, pid, color in zip(axes, ['A', 'B'], ['steelblue', 'tomato']):
    grp = prod[prod['product'] == pid]
    X = sm.add_constant(grp['quantity'])
    model = sm.OLS(grp['total_cost'], X).fit() # 회귀분석
    fixed_cost = model.params['const']  
    var_cost = model.params['quantity'] # 단위 변동비
    unit_vc[pid] = var_cost
    
    # 산점도 + 회귀선
    ax.scatter(grp['quantity'], grp['total_cost'], alpha=0.5, color=color, label='실제 데이터')
    x_line = np.linspace(grp['quantity'].min(), grp['quantity'].max(), 100)
    ax.plot(x_line, model.params['const'] + model.params['quantity'] * x_line,
            color='black', linewidth=2, label='회귀선')   
    ax.set_title(f'빵 {pid}: 총원가 vs 생산량\n고정비={fixed_cost:,.0f}원 변동비={var_cost:,.0f}원/ R2={model.rsquared:.3f}')
    ax.set_xlabel('생산량 (개)')
    ax.set_ylabel('총원가 (원)')
    ax.legend()
    
plt.tight_layout()
plt.show()

print("\n단위 변동비 (회귀 기울기):")
for k, v in unit_vc.items():
    print(f" 빵 {k}: {v:,.0f}원")

# 단위 이익 계산
p = {pid: unit_price[pid] - unit_vc[pid] for pid in ['A', 'B']}
print("단위 이익 p:")
for k, v in p.items():
    print(f" 빵 {k}: {unit_price[k]:,.0f}원(판매가) - {unit_vc[k]:,.0f}원(변동비) = {v:,.0f}원")

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
print(f"\n오늘 가용 오븐: {CAP} 시간")
print(f"오늘 가용 재료: {MAT} kg")

params = pd.DataFrame({
    '파라미터': ['p (단위이익, 원)', 'a (오븐시간/개)', 'm (재료kg/개)', 'D (수요상한, 개)'],
    '빵 A': [round(p['A'], 0), round(a['A'], 3), round(m['A'], 3), round(D['A'], 0)],
    '빵 B': [round(p['B'], 0), round(a['B'], 3), round(m['B'], 3), round(D['B'], 0)],
    '추출 방법': ['판매가 평균 - 회귀 변동비', '생산로그 집계', '생산로그 집계', '판매기록 75분위']
})
print("=" * 60)
print("LP 투입 파라미터 Summary")
print("=" * 60)
print(params.to_string(index=False))
print(f"\n CAP (가용 오븐시간) = {CAP}")
print(f" MAT (가용 재료) = {MAT} kg")

solver = pywraplp.Solver.CreateSolver('GLOP')   # GLOP : 연속 LP 전용 solver

# 변수 선언
inf = solver.infinity()
xA = solver.NumVar(0, inf, 'xA')
xB = solver.NumVar(0, inf, 'xB')

# 제약 조건
solver.Add(a['A'] * xA + a['B'] * xB <= CAP)    # 오븐 용량
solver.Add(m['A'] * xA + m['B'] * xB <= MAT)    # 재료 한도
solver.Add(xA <= D['A'])    # 수요 상한 A
solver.Add(xB <= D['B'])    # 수요 상한 B

# 목적 함수 (최대화)
solver.Maximize(p['A'] * xA + p['B'] * xB)

# 풀이
status = solver.Solve()

# status 코드 : 0=OPTIMAL, 1=FEASIBLE, 2=INFEASIBLE, 3=UNBOUNDED
status_map = {0: 'OPTIMAL', 1: 'FEASIBLE', 2: 'INFEASIBLE', 3: 'UNBOUNDED'}
print(f"풀이상태: {status_map.get(status, status)}")
print()
xA_val = xA.solution_value()
xB_val = xB.solution_value()
obj_val = solver.Objective().Value()
print(f"최적생산량: 빵 A = {xA_val:.0f} 개, 빵 B = {xB_val:.0f} 개")
print(f"최대이익: {obj_val:,.0f} 원")
print()
print(f"오븐사용: {a['A'] * xA_val + a['B'] * xB_val:.1f} / {CAP} 시간")
print(f"재료사용: {m['A'] * xA_val + m['B'] * xB_val:.1f} / {MAT} kg")

# 실행 가능 영역 시각화
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

# 최적해 (OR-Tools 결과 사용)
ax.scatter(xA_val, xB_val, color='red', zorder=5, s=150)
ax.annotate(f"최적해\n({xA_val:.0f}개, {xB_val:.0f}개)\n이익 {obj_val:,.0f}원",
            xy=(xA_val, xB_val),
            xytext=(xA_val + 5, xB_val + 5),
            fontsize=10,
            bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7))

ax.set_xlim(0, D['A'] * 1.3)
ax.set_ylim(0, D['B'] * 1.5)
ax.set_xlabel('빵 A 생산량 (개)')
ax.set_ylabel('빵 B 생산량 (개)')
ax.set_title('생산계획 LP — 실행 가능 영역 및 최적해')
ax.legend(loc='upper right')
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# 민감도 분석 함수
def solve_lp(p_A, p_B, D_A, D_B):
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
profits_D = [solve_lp(p['A'], p['B'], D['A'] * s, D['B'] * s)[0] for s in scales]

# 단위이익 파라미터 변화 vs 이익
profits_p = [solve_lp(p['A'] * s, p['B'] * s, D['A'], D['B'])[0] for s in scales]

fig, axes = plt.subplots(1, 2, figsize=(12, 4))
for ax, profits, title, color in zip(axes, [profits_D, profits_p], 
                                     ['수요 파라미터 추정오차 → 이익변화', '단위이익 파라미터 오차 → 이익변화'], 
                                     ['steelblue', 'tomato']):
    ax.plot(scales, profits, marker='o', color=color, linewidth=2)
    ax.axvline(1.0, color='black', linestyle='--')
    ax.set_xlabel('파라미터 추정 배율 (1.0 = 정확)')
    ax.set_ylabel('최적 이익 (원)')
    ax.set_title(title)
    ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

print("파라미터 오차가 클수록 의사결정 품질이 떨어집니다.")
print(f" 수요를 30% 과대추정 시 → 실현 이익 하락 가능성")
print(f" 단위이익을 30% 과소추정 시 → 수익성 높은 제품 과소 생산")

# 실습

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
from ortools.linear_solver import pywraplp

plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['figure.figsize'] = (8, 5)

import platform

if platform.system() == 'Windows':
    plt.rcParams['font.family'] = 'Malgun Gothic'
elif platform.system() == 'Darwin':
    plt.rcParams['font.family'] = 'Apple Gothic'
else:
    plt.rcParams['font.family'] = 'NanumGothic'


# 1. 최적화 모형 수립
# ---------------------------------------------------------
# 목적함수 : 최소화 C_A * xA + C_B * xB (총 배송 비용)

# 제약조건 :
#   1) 시간 제약: h_A * xA + h_B * xB <= CAP (기사 가동 시간)
#   2) 연료 제약: f_A * xA + f_B * xB <= FUEL (연료 사용량)
#   3) 수요 제약: xA >= D_A, xB >= D_B (계약 최소 처리량)
# ---------------------------------------------------------

# 2. 파일로부터 데이터 읽기
delivery = pd.read_csv('delivery_log.csv')
contract = pd.read_csv('contract_demand.csv')
capacity = pd.read_csv('capacity_today.csv')

# 3. 데이터 분석하여 파라미터 추정

# 수요 파라미터 (D_A, D_B): 주간 계약량 / 7 (일간 환산)
D = {
    'A': contract.loc[contract['route'] == 'A', 'weekly_min_deliveries'].values[0] / 7,
    'B': contract.loc[contract['route'] == 'B', 'weekly_min_deliveries'].values[0] / 7
    }

# 비용 파라미터 (C_A, C_B): 회귀분석을 통한 단위 비용(기울기) 추출
unit_cost = {}

for route in ['A', 'B']:
    grp = delivery[delivery['route'] == route]
    X = sm.add_constant(grp['num_deliveries'])
    model = sm.OLS(grp['weekly_cost'], X).fit() # 회귀분석
    
    unit_cost[route] = model.params['num_deliveries'] # 단위 변동비

# 자원 파라미터 (h, f): 건당 평균 소모량 집계
res_params = (delivery
              .groupby('route')
              .apply(lambda x: pd.Series({
                  'h': x['driver_hours'].sum() / x['num_deliveries'].sum(),
                  'f': x['fuel_liters'].sum() / x['num_deliveries'].sum()
               })))

h = res_params['h'].to_dict()
f = res_params['f'].to_dict()

# 4-4. 가용 자원 (CAP, FUEL)
CAP = capacity.loc[0, 'available_driver_hours']
FUEL = capacity.loc[0, 'available_fuel_liters']

print("=== 추출된 파라미터 Summary ===")
print(f" 단위비용: A={unit_cost['A']:,.0f}원, B={unit_cost['B']:,.0f}원")
print(f" 건당시간: A={h['A']:.2f}h, B={h['B']:.2f}h")
print(f" 일일수요(하한): A={D['A']:.1f}건, B={D['B']:.1f}건")

# 4. 최적화 모양에 대한 ortools 코드 작성
solver = pywraplp.Solver.CreateSolver('GLOP')   # GLOP: 연속 LP 전용 solver

# 변수 선언
inf = solver.infinity()
xA = solver.NumVar(D['A'], inf, 'xA') # 하한을 D['A']로 설정
xB = solver.NumVar(D['B'], inf, 'xB') # 하한을 D['B']로 설정

# 제약 조건
solver.Add(h['A'] * xA + h['B'] * xB <= CAP)
solver.Add(f['A'] * xA + f['B'] * xB <= FUEL)

# 목적 함수(최소화)
solver.Minimize(unit_cost['A'] * xA + unit_cost['B'] * xB)

# 풀이
status = solver.Solve()

status_map = {0: 'OPTIMAL', 1: 'FEASIBLE', 2: 'INFEASIBLE', 3: 'UNBOUNDED'}
print(f"풀이상태: {status_map.get(status, status)}")
print()

if status == 0: 
    xA_val = xA.solution_value()
    xB_val = xB.solution_value()
    obj_val = solver.Objective().Value()

    print(f"최적 배송량: 노선 A = {xA_val:.1f} 건, 노선 B = {xB_val:.1f} 건")
    print(f"최소 비용: {obj_val:,.0f} 원")
    print()
    print(f"시간 가용: {h['A']*xA_val + h['B']*xB_val:.1f} / {CAP} 시간")
    print(f"연료 가용: {f['A']*xA_val + f['B']*xB_val:.1f} / {FUEL} L")
else:
    print("현재 자원으로는 최소 계약 물량을 배송할 수 없습니다.")

# 5. 시각화 (Optional)
fig, ax = plt.subplots(figsize=(8, 6))

xv = np.linspace(0, D['A'] * 3, 400)

# 제약 경계선
y_time = (CAP - h['A'] * xv) / h['B']
y_fuel = (FUEL - f['A'] * xv) / f['B']

ax.plot(xv, np.clip(y_time, 0, None), label=f'기사 시간 한도 ({CAP}h)', color='steelblue')
ax.plot(xv, np.clip(y_fuel, 0, None), label=f'연료량 한도 ({FUEL}L)', color='orange')
ax.axvline(D['A'], color='red', linestyle='--', label='최소 계약 A')
ax.axhline(D['B'], color='green', linestyle='--', label='최소 계약 B')

# 실행 가능 영역 색칠 (수요 하한선 위쪽 & 자원 한계선 아래쪽)
y_top = np.minimum(y_time, y_fuel)

mask = (xv >= D['A']) 
ax.fill_between(xv[mask], D['B'], y_top[mask], 
                where=(y_top[mask] >= D['B']), 
                alpha=0.15, color='steelblue', label='실행 가능 영역')

if status == 0:
    ax.scatter(xA_val, xB_val, color='red', zorder=5, s=150)
    ax.annotate(f"최적해\n({xA_val:.1f}건, {xB_val:.1f}건)\n비용 {obj_val:,.0f}원",
                xy=(xA_val, xB_val),
                xytext=(xA_val + 3, xB_val + 2),
                fontsize=10,
                bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7))

ax.set_xlim(0, D['A'] * 2.5)
ax.set_ylim(0, D['B'] * 2.5)
ax.set_xlabel('노선 A 배송 건수 (건)', fontsize=12)
ax.set_ylabel('노선 B 배송 건수 (건)', fontsize=12)
ax.set_title('배송계획 LP — 실행 가능 영역 및 최적해', fontsize=13)
ax.legend(loc='upper right')
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# 6. 민감도 분석

# 6-1. A, B 계약량 증감에 따른 비용 변화 (평균 계약량의 70% ~ 150%)
print("\n--- 1. 계약량 증감 민감도 분석 ---")

ratios = np.linspace(0.7, 1.5, 9) # 0.7, 0.8, ..., 1.5까지 9개 지점
results_cost = []

for r in ratios:
    s_sub = pywraplp.Solver.CreateSolver('GLOP')
    sxA = s_sub.NumVar(D['A'] * r, s_sub.infinity(), 'sxA')
    sxB = s_sub.NumVar(D['B'] * r, s_sub.infinity(), 'sxB')
    s_sub.Add(h['A'] * sxA + h['B'] * sxB <= CAP)
    s_sub.Add(f['A'] * sxA + f['B'] * sxB <= FUEL)
    s_sub.Minimize(unit_cost['A'] * sxA + unit_cost['B'] * sxB)
    
    if s_sub.Solve() == pywraplp.Solver.OPTIMAL:
        current_cost = s_sub.Objective().Value()
        results_cost.append(current_cost)
        print(f"계약량 {int(r*100)}% 수준: 최소 비용 {current_cost:,.0f}원")
    else:
        results_cost.append(None)
        print(f"계약량 {int(r*100)}% 수준: 실행 불가능 (자원 부족)")

plt.figure(figsize=(8, 5))
plt.plot(ratios, results_cost, marker='o', color='blue', linewidth=2)
plt.axvline(1.0, color='red', linestyle='--', label='현재 계약량(100%)')
plt.title('계약량 변화에 따른 최소 배송 비용 추이')
plt.xlabel('계약량 배율 (1.0 = 현재)')
plt.ylabel('총 배송 비용 (원)')
plt.grid(True, alpha=0.3)
plt.legend()
plt.show()

# 6-2. 수요 2배 증가 시 부족 자원량 계산

# 수요가 2배일 때 필요한 총 자원량 계산 (수학 모형의 왼쪽 항)
D2_A, D2_B = D['A'] * 2, D['B'] * 2
total_req_h = h['A'] * D2_A + h['B'] * D2_B
total_req_f = f['A'] * D2_A + f['B'] * D2_B

# 현재 가용량(CAP, FUEL)과의 차이 계산
lack_h = max(0, total_req_h - CAP)
lack_f = max(0, total_req_f - FUEL)

print(f"수요 2배 시 필요 시간: {total_req_h:.1f}h (현재 {CAP}h 대비 {lack_h:.1f}h 추가 필요)")
print(f"수요 2배 시 필요 연료: {total_req_f:.1f}L (현재 {FUEL}L 대비 {lack_f:.1f}L 추가 필요)")

if lack_h > 0 or lack_f > 0:
    print(f"\n Feasible solution이 존재하려면 기사 시간 {lack_h:.1f}h와 연료 {lack_f:.1f}L가 더 필요합니다.")