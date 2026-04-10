# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 20:24:44 2026

@author: redti
"""

# 문제1
print("문제 1")
# 사우디산 원유 1 배럴 -> 0.3 가솔린 + 0.4 제트유 + 0.2 윤활유
# 베네수엘라 원유 1 배럴 -> 0.4 가솔린 + 0.2 제트유 + 0.3 윤활유
# 제약조건1 : 사우디산 원유 구매량 하루 최대 9000 배럴
# 제약조건2 : 베네수엘라 원유 구매량 하루 최대 6000 배럴
# 제약조건3 : 매일 가솔린 >= 2000
# 제약조건4 : 매일 제트유 >= 1500
# 제약조건5 : 매일 윤활유 >= 500
# 제약조건6 : 각 구매량 >= 0
# 목적함수 $60*사우디 + $55*베네수엘라의 최소비용

from ortools.linear_solver import pywraplp

solver= pywraplp.Solver.CreateSolver('SCIP')

data={}
data['constraint_coeffs'] = [[0.3,0.4],
                             [0.4,0.2],
                             [0.2,0.3]]
data['limit'] = [2000,1500,500]
data['prices'] = [60,55]
data['max'] = [9000,6000]
data['num_vars'] = 2
data['num_constraints']= 3
data['name_vars'] = ['사우디산 원유 구매량','베네수엘라산 원유 구매량']

# 의사결정 변수
x = {}
for j in range(data["num_vars"]):
    x[j] = solver.NumVar(0,data['max'][j],'x[%i]'%j)

# 제약조건
for i in range(data['num_constraints']):
    constraint_expr = [data['constraint_coeffs'][i][j]*x[j] for j in range(data['num_vars'])]
    solver.Add(sum(constraint_expr) >= data['limit'][i])

# 목적함수
obj_expr = [data['prices'][i]*x[i] for i in range(data['num_vars'])]
solver.Minimize(solver.Sum(obj_expr))

status = solver.Solve()

if status==pywraplp.Solver.OPTIMAL:
    print(f'총 비용 = ${solver.Objective().Value():.1f}')
    for j in range(data['num_vars']):
        print(f"{data['name_vars'][j]} = {x[j].solution_value():.1f} 배럴")
else:
    print('The problem does not have an optimal solution.')
    
    
# 문제 2
print("\n문제 2")
# 원석1 1톤 -> 0.2% 가돌리늄 + 0.15% 홀륨 + 0.2% 툴륨
# 원석2 1톤 -> 0.3% 가돌리늄 + 0.25% 홀륨 + 0.1% 툴륨
# 제약조건1 : 가돌리늄 추출 >= 8톤
# 제약조건2 : 홀륨 추출 >= 6톤
# 제약조건3 : 툴륨 추출 >= 4톤
# 제약조건4 : 각 구입량 >= 0
# 목적함수: 10*원석1 + 15*원석2의 최소비용

from ortools.linear_solver import pywraplp

solver= pywraplp.Solver.CreateSolver('SCIP')

data={}
data['constraint_coeffs'] = [[0.2,0.3],
                             [0.15,0.25],
                             [0.2,0.1]]
data['limit'] = [8,6,4]
data['prices'] = [10,15]
data['num_vars'] = 2
data['num_constraints'] = 3
data['name'] = ['원석1 구입량', '원석2 구입량']

infinity = solver.infinity()

# 의사결정 변수
x = {}
for j in range(data["num_vars"]):
    x[j] = solver.NumVar(0,infinity,'x[%i]'%j)

# 제약조건
for i in range(data['num_constraints']):
    constraint_expr = [data['constraint_coeffs'][i][j]*x[j] for j in range(data['num_vars'])]
    solver.Add(sum(constraint_expr) >= data['limit'][i])

# 목적함수
obj_expr = [data['prices'][i]*x[i] for i in range(data['num_vars'])]
solver.Minimize(solver.Sum(obj_expr))

status = solver.Solve()

if status==pywraplp.Solver.OPTIMAL:
    print(f'총 비용 = {solver.Objective().Value():.1f}만원')
    for j in range(data['num_vars']):
        print(f"{data['name'][j]} = {x[j].solution_value():.1f}톤")
else:
    print('The problem does not have an optimal solution.')
    
    
# 문제 3
print("\n문제 3")
# 유모차 1대 -> 기계1 8시간, 기계2 4시간, 기계3 4시간
# 보행기 1대 -> 기계1 3시간, 기계2 4시간, 기계3 0시간
# 자전거 1대 -> 기계1 3시간, 기계2 0시간, 기계3 2시간
# 제약조건1 : 기계1 활용시간 <= 240
# 제약조건2 : 기계2 활용시간 <= 200
# 제약조건3 : 기계3 활용시간 <= 100
# 제약조건4 : 각 생산량 >= 0
# 목적함수 30*유모차 + 20*보행기 + 16*자전거 + 3.5(240-8x-3y-3z) + 3(100-4x-2z)
#           => -10x+9.5y-0.5z+1140

from ortools.linear_solver import pywraplp

solver= pywraplp.Solver.CreateSolver('SCIP')

data={}
data['constraint_coeffs'] = [[8,3,3],
                             [4,4,0],
                             [4,0,2]]
data['limit'] = [240,200,100]
data['prices'] = [-10,9.5,-0.5]
data['num_vars'] = 3
data['num_constraints'] = 3
data['name_1'] = ['유모차 생산량', '보행기 생산량', '자전거 생산량']
data['name_2'] = ['기계1 임대시간', '기계2(임대x)', '기계3 임대시간']

infinity = solver.infinity()

# 의사결정 변수 -> 생산량은 정수(IntVar)
x = {}
for j in range(data["num_vars"]):
    x[j] = solver.IntVar(0,infinity,'x[%i]'%j)

# 제약조건
for i in range(data['num_constraints']):
    constraint_expr = [data['constraint_coeffs'][i][j]*x[j] for j in range(data['num_vars'])]
    solver.Add(sum(constraint_expr) <= data['limit'][i])

# 목적함수 : (-10x + 9.5y - 0.5z + 1140)의 최대
obj_expr = [data['prices'][i]*x[i] for i in range(data['num_vars'])]
solver.Maximize(solver.Sum(obj_expr)+1140)

status = solver.Solve()

if status==pywraplp.Solver.OPTIMAL:
    print(f'총 수익 = {solver.Objective().Value():.1f}만원')
    for j in range(data['num_vars']):
        print(f"{data['name_1'][j]} = {x[j].solution_value():.1f}대")
    # 기계1과 기계3의 임대 시간만 계산하여 출력    
    for l in [0,2]:
        time = sum(data['constraint_coeffs'][l][j]*x[j].solution_value() for j in range(data['num_vars']))
        print(f"{data['name_2'][l]} = {data['limit'][l] - time:.1f}시간")
else:
    print('The problem does not have an optimal solution.')
