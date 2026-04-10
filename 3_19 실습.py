# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 14:34:10 2026

@author: redti
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
from ortools.linear_solver import pywraplp

plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['figure.figsize'] = (8, 5)

import platform

if platform.system() == 'Windows':
    plt.rcParams['font.family'] = 'Malgun Gothic'
elif platform.system() == 'Darwin':
    plt.rcParams['font.family'] = 'Apple Gothic'
else:
    plt.rcParams['font.family'] = 'NanumGothic'
plt.rcParams['axes.unicode_minus'] = False

# [1. 최적화 모형 수립 (주석)]
# ---------------------------------------------------------
# (1) 의사결정 변수: xA(노선 A 배송 건수), xB(노선 B 배송 건수)
# (2) 목적함수: Minimize Total Cost = (unit_cost_A * xA) + (unit_cost_B * xB)
# (3) 제약조건: 
#     - 시간 제약: (h_A * xA) + (h_B * xB) <= CAP
#     - 연료 제약: (f_A * xA) + (f_B * xB) <= FUEL
#     - 최소 계약량: xA >= D_A, xB >= D_B
# ---------------------------------------------------------

# [3. 파일로부터 데이터 읽기]
delivery = pd.read_csv('delivery_log.csv')
contract = pd.read_csv('contract_demand.csv')
capacity = pd.read_csv('capacity_today.csv')

# [4. 데이터 분석 및 파라미터 추정]
# 비용(C), 시간(h), 연료(f), 수요(D), 가용량(CAP, FUEL)
unit_cost = {}
for route in ['A', 'B']:
    grp = delivery[delivery['route'] == route]
    X = sm.add_constant(grp['num_deliveries'])
    model = sm.OLS(grp['weekly_cost'], X).fit()
    unit_cost[route] = model.params['num_deliveries']

res_params = delivery.groupby('route').apply(lambda x: pd.Series({
    'h': x['driver_hours'].sum() / x['num_deliveries'].sum(),
    'f': x['fuel_liters'].sum() / x['num_deliveries'].sum()
}))
h, f = res_params['h'].to_dict(), res_params['f'].to_dict()

D = {
    'A': contract.loc[contract['route'] == 'A', 'weekly_min_deliveries'].values[0] / 7,
    'B': contract.loc[contract['route'] == 'B', 'weekly_min_deliveries'].values[0] / 7
}
CAP = capacity.loc[0, 'available_driver_hours']
FUEL = capacity.loc[0, 'available_fuel_liters']

# [5. 최적화 모형 (OR-Tools)]
solver = pywraplp.Solver.CreateSolver('GLOP')
xA = solver.NumVar(D['A'], solver.infinity(), 'xA')
xB = solver.NumVar(D['B'], solver.infinity(), 'xB')
solver.Add(h['A'] * xA + h['B'] * xB <= CAP)
solver.Add(f['A'] * xA + f['B'] * xB <= FUEL)
solver.Minimize(unit_cost['A'] * xA + unit_cost['B'] * xB)
solver.Solve()
xA_val, xB_val = xA.solution_value(), xB.solution_value()
obj_val = solver.Objective().Value()

# [6. 시각화 (Optional - 실행 가능 영역)]
fig, ax = plt.subplots(figsize=(8, 7))
xv = np.linspace(0, D['A'] * 3, 400)
y_time = (CAP - h['A'] * xv) / h['B']
y_fuel = (FUEL - f['A'] * xv) / f['B']

ax.plot(xv, np.clip(y_time, 0, None), label=f'시간 제약 ({CAP}h)', color='steelblue', lw=2)
ax.plot(xv, np.clip(y_fuel, 0, None), label=f'연료 제약 ({FUEL}L)', color='orange', lw=2)
ax.axvline(D['A'], color='gray', ls='--', label=f'최소 계약 A ({D["A"]:.1f}건)')
ax.axhline(D['B'], color='green', ls='--', label=f'최소 계약 B ({D["B"]:.1f}건)')

# 영역 색칠 (빵 문제와 같은 스타일, 단 하한선이 D['B'])
y_top = np.minimum(y_time, y_fuel)
ax.fill_between(xv, D['B'], y_top, where=(xv >= D['A']) & (y_top >= D['B']), 
                alpha=0.2, color='skyblue', label='실행 가능 영역')

ax.scatter(xA_val, xB_val, color='red', zorder=5, s=150)
ax.annotate(f"최적해\n({xA_val:.1f}건, {xB_val:.1f}건)\n비용 {obj_val:,.0f}원",
            xy=(xA_val, xB_val), xytext=(xA_val + 5, xB_val + 5),
            bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7))

ax.set_title('생산계획 LP — 실행 가능 영역 및 최적해 (배송)')
ax.set_xlabel('노선 A 배송 건수'); ax.set_ylabel('노선 B 배송 건수')
ax.legend(); ax.grid(True, alpha=0.3)
plt.show()

# [7. 민감도 분석]
# (1) 계약량 증감에 따른 비용 변화 (70% ~ 150%)
ratios = np.linspace(0.7, 1.5, 9)
costs = []
for r in ratios:
    s_solver = pywraplp.Solver.CreateSolver('GLOP')
    sxA = s_solver.NumVar(D['A'] * r, solver.infinity(), 'sxA')
    sxB = s_solver.NumVar(D['B'] * r, solver.infinity(), 'sxB')
    s_solver.Add(h['A'] * sxA + h['B'] * sxB <= CAP)
    s_solver.Add(f['A'] * sxA + f['B'] * sxB <= FUEL)
    s_solver.Minimize(unit_cost['A'] * sxA + unit_cost['B'] * sxB)
    costs.append(s_solver.Objective().Value() if s_solver.Solve() == pywraplp.Solver.OPTIMAL else None)

plt.figure(figsize=(8, 5))
plt.plot(ratios * 100, costs, 'go-', lw=2)
plt.title('계약량 변화에 따른 총 비용 민감도')
plt.xlabel('계약량 비율 (%)'); plt.ylabel('총 비용 (원)')
plt.grid(True, alpha=0.3); plt.show()

# (2) 수요 2배 시 부족 자원 분석
D2 = {k: v * 2 for k, v in D.items()}
req_h = h['A'] * D2['A'] + h['B'] * D2['B']
req_f = f['A'] * D2['A'] + f['B'] * D2['B']
print(f"\n--- 수요 2배 분석 ---")
print(f"추가 필요 시간: {max(0, req_h - CAP):.1f}h")
print(f"추가 필요 연료: {max(0, req_f - FUEL):.1f}L")