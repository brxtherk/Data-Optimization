# 공장 생산 계획

from ortools.linear_solver import pywraplp

# 솔버 생성
solver = pywraplp.Solver.CreateSolver("GLOP")

# 결정 변수
INF = solver.infinity()
x1 = solver.NumVar(0, INF, 'x1') # 제품 A 생산량
x2 = solver.NumVar(0, INF, 'x2') # 제품 B 생산량

# 제약 조건
c1 = solver.Add(2*x1 + x2 <= 8, '기계_제약')
c2 = solver.Add(x1 + 3*x2 <= 9, '조립_제약')

# 목적 함수
solver.Maximize(3*x1 + 5*x2)

# 풀기
status = solver.Solve()

STATUS_NAME = {
    pywraplp.Solver.OPTIMAL: 'OPTIMAL',
    pywraplp.Solver.FEASIBLE: 'FEASIBLE',
    pywraplp.Solver.INFEASIBLE: 'INFEASIBLE',
    pywraplp.Solver.UNBOUNDED: 'UNBOUNDED'
}

print('='*45)
print(f'상태: {STATUS_NAME.get(status, status)}')

if status == pywraplp.Solver.OPTIMAL:
    print(f'제품 A(x1): {x1.solution_value():.4f} 개')
    print(f'제품 B(x2): {x2.solution_value():.4f} 개')
    print(f'최대 이익 : {solver.Objective().Value():.4f} 만원')
    print('-'*45)
    print('[쌍대값/Shadow Price]')
    print(f'y1(기계 제약): {c1.dual_value():.4f} 만원/시간')
    print(f'y2(조립 제약): {c2.dual_value():.4f} 만원/시간')
    print('-'*45)
    print('[환산 비용/Reduced Cost]')
    print(f'rc(x1): {x1.reduced_cost():.4f}')
    print(f'rc(x2): {x2.reduced_cost():.4f}')

## 민감도 분석
from ortools.linear_solver import pywraplp
import numpy as np
import matplotlib.pyplot as plt


def solve_lp(c1_val, c2_val=5, b1=8, b2=9):
    s = pywraplp.Solver.CreateSolver("GLOP")
    INF = s.infinity()
    x1 = s.NumVar(0, INF, 'x1')
    x2 = s.NumVar(0, INF, 'x2')
    s.Add(2*x1 + x2 <= b1)
    s.Add(x1 + 3*x2 <= b2)
    s.Maximize(c1_val*x1 + c2_val*x2)
    if s.Solve() == pywraplp.OPTIMAL:
        return x1.solution_value(), x2.solution_value(), s.Objective().Value()
    return None, None, None

c1_range = np.linspace(0, 12, 200)
x1_vals, x2_vals, z_vals = [], [], []
for c1v in c1_range:
    xv1, xv2, zv = solve_lp(c1v)
    x1_vals.append(xv1) ; x2_vals.append(xv2) ; z_vals.append(zv)

fig, axes = plt.subplots(1, 2, figsize=(13, 5))

ax = axes[0]
ax.plot(c1_range, x1_vals, 'b-', lw=2, label=r'$x_1^*$ (제품 A)')
ax.plot(c1_range, x2_vals, 'r-', lw=2, label=r'$x_2^*$ (제품 B)')
ax.axvline(3, color='gray', ls='--', label='현재 $c_1=3$')
ax.axvline(2.5, color='orange', ls=':', lw=1.5, label='임계점 $c_1=2.5$')
ax.axvline(10,color='purple', ls=':', lw=1.5, label='임계점 $c_1=10$')  ## 기울기 계산
ax.set_xlabel(r'$c_1$(제품 A 단위 이익)', fontsize=11)
ax.set_ylabel('최적 생산량', fontsize=11)
ax.set_title(r'$c_1$ 변화에 따른 최적 생산량', fontsize=12, fontweight='bold')
ax.legend(fontsize=8); ax.grid(True, alpha=0.3)

ax = axes[1]
ax.plot(c1_range, z_vals, 'g-', lw=2)
ax.axvline(3, color='gray', ls='--', label='현재 $c_1=3$')
ax.scatter([3],[19], color='red', s=80, zorder=5, label='z*=19')
ax.set_xlabel(r'$c_1$(제품 A 단위 이익)', fontsize=11)
ax.set_ylabel('최적 이익 z*', fontsize=11)
ax.set_title(r'$c_1$ 변화에 따른 최적 생산량', fontsize=12, fontweight='bold')
ax.legend(fontsize=8); ax.grid(True, alpha=0.3)

plt.suptitle('목적함수 계수 민감도 분석', fontsize=14, fontweight='bold')
plt.tight_layout(); plt.show()

print('c1의 허용 범위: 2.5<= c1 <= 10.0(현재 기저 유지)')
print('c1 < 2.5 -> 기저 변경: x1=0, x2=3이 최적')
print('c1 > 10.0    -> 기저 변경: x1=4, x2=0이 최적')


## RHS 민감도
from ortools.linear_solver import pywraplp
import numpy as np
import matplotlib.pyplot as plt

b1_range = np.linspace(2, 16, 200)
z_b1, sp_b1 = [], []

for b1v in b1_range:
    s = pywraplp.Solver.CreateSolver('GLOP')
    INF = s.infinity()
    x1 = s.NumVar(0, INF, 'x1')
    x2 = s.NumVar(0, INF, 'x2')
    ct1 = s.Add(2*x1 + x2 <= b1v)
    s.Add(x1 + 3*x2 <= 9)
    s.Maximize(3*x1 + 5*x2)
    if s.solve() == pywraplp.Solver.OPTIMAL:
        z_b1.append(s.Objective().Value())
        sp_b1.append(ct1.dual_value())
    else:
        z_b1.append(np.nan); sp_b1.append(np.nan)

fig, axes = plt.subplots(1, 2, figsize=(13,5))

ax = axes[0]
ax.plot(b1_range, z_b1, 'b-', lw=2)
ax.axvline(8, color='gray', ls='--', label='현재 $b_1=8$')
ax.scatter([8],[19], color='red', s=80, zorder=5, label='현재 z*=19')
b1_tan=np.array([4, 14])
ax.plot(b1_tan, 19+0.8*(b1_tan-8), 'r--', alpha=0.6, label='기울기=0.8 (shadow price)')
ax.set_xlabel(r'$b_1$ (기계 가용 시간)', fontsize=11)
ax.set_ylabel('최적 이익 z*', fontsize=11)
ax.set_title(r'$b_1$ 변화에 따른 최적 이익', fontsize=12, fontweight='bold')
ax.legend(fontsize=9); ax.grid(True, alpha=0.3)

ax = axes[1]
ax.plot(b1_range, sp_b1,'r-',lw=2)
ax.axvline(8,color='gray',ls='--',label='현재 $b_1=8$')
ax.axhline(0.8,color='orange',ls=':',label='y1*=0.8')
ax.fill_between([3,12],[0,0],[1,1],alpha=0.1,color='green',label='Shadow price 유효 구간')
ax.set_xlabel(r'$b_1$ (기계 가용 시간)',fontsize=11)
ax.set_ylabel('Shadow Price $y_1$',fontsize=11)
ax.set_title('Shadow Price 유효 범위',fontsize=12,fontweight='bold')
ax.legend(fontsize=9); ax.grid(True,alpha=0.3); ax.set_ylim(-0.1,1.8)

plt.suptitle('RHS 민감도 분석 (기계 제약 b1)',fontsize=14,fontweight='bold')
plt.tight_layout(); plt.show()
print('RHS 민감도 결과:')
print(' 기계 제약 (b1=8): shadow price y1* = 0.80 만원/시간')
print(' 조립 제약 (b2=9): shadow price y2* = 1.40 만원/시간')
print(' → 기계 1시간 추가 → 이익 +0.80만원')
print(' → 조립 1시간 추가 → 이익 +1.40만원')
print(' 조립 인력 확충이 더 효과적!')





