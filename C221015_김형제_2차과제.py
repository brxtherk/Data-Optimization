# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

# 과제 2-1

# 3개 공장의 목재 수요는 주당 500, 600, 700 톤
# 목재는 3개 회사로부터 목재를 구매
# 공급 제약: 첫 2개 공장은 공급량 제한 없고 3번째 공장은 주당 500톤
# 수송 제약: 첫 번째 목재 회사는 철도수송으로 제한이 없음
#           나머지 2회사는 트럭 수송으로 200톤까지 수송가능
# 우측은 각 목재회사에서 공장으로의 톤당 수송비용

# Obj : +2x00 + 3x01 + 5x02 + 2.5x10 + 4x11 + 4.8x12 + 3x20 + 3.6x21 + 3.2x22 (minimize)
# subject to    demand x00 + x10 + x20 >= 500
#                      x01 + x11 + x21 >= 700
#                      x02 + x12 + x22 >= 600

#               supply 0 <= x00 + x01 + x02
#                      0 <= x10 + x11 + x12
#                      0 <= x20 + x21 + x22 <= 500

#               transport 0 <= x00, x01, x02       
#                         0 <= x10, x11, x12 <= 200
#                         0 <= x20, x21, x22 <= 200

from ortools.linear_solver import pywraplp
solver = pywraplp.Solver.CreateSolver('SCIP')

data = {}

# 수송 비용
data['costs'] = [
    [2, 3, 5],
    [2.5, 4, 4.8],
    [3, 3.6, 3.2]
    ]
data['demands'] = [500, 700, 600]
data['supply'] = [solver.infinity(), solver.infinity(), 500]
data['trans'] = [solver.infinity(), 200, 200]
num_c = 3
num_p = 3

# 의사결정 변수(i: company, j: plants)

X = {}

for i in range (num_c):
    for j in range (num_p):
        X[i, j] = solver.NumVar(0, data['trans'][i], "X"+str(i)+str(j))
        
# 제약 조건

for j in range (num_p):
    solver.Add(sum(X[i, j] for i in range (num_c)) >= data['demands'][j])
    
for i in range (num_c):
    solver.Add(sum(X[i, j] for j in range (num_p)) <= data['supply'][i])
    
# 목적 함수

obj_expr = []
for i in range (num_c):
    for j in range (num_p):
        obj_expr.append(data['costs'][i][j] * X[i, j])
        
solver.Minimize(solver.Sum(obj_expr))

status = solver.Solve()

print("과제 2-1")

if status==pywraplp.Solver.OPTIMAL:
    print(f'총 비용 : ${solver.Objective().Value():.1f}')
    for i in range (num_c):
        for j in range (num_p):
            print(f'{X[i,j].name()} : {X[i,j].solution_value()}t')
            
else:
    print('This problem does not have an optimal solution')

# 과제 2-2

# 총 저소득 주택 수 = X, 총 중간소득 주택 수 = Y
# 에이커 당 주택 건설 수: 저소득=20, 중간소득=15 -> X/20 + Y/15 <= 10
# 주택 건설 총 비용: 13000*X + 18000*Y <= 2000000
# 건설 guideline: 60 <= X <= 100, 30 <= Y <= 70
# 결합 시장 수요: X + Y <= 150
# 건축가 제안: X >= Y/2 + 50
# 비용 최소화, 주택수 최대화

from ortools.linear_solver import pywraplp
solver = pywraplp.Solver.CreateSolver('SCIP')

# 의사결정 변수

X = solver.NumVar(60, 100, "총 저소득 주택 수")
Y = solver.NumVar(30, 70, "총 중간소득 주택 수")

# 제약 조건

solver.Add(X/20 + Y/15 <= 10)
solver.Add(13000*X + 18000*Y <= 2000000)
solver.Add(X + Y <= 150)
solver.Add(X >= 0.5*Y + 50)

# 2-2(1) 비용 최소화

solver.Minimize(13000*X + 18000*Y)

status = solver.Solve()

print("\n과제 2-2(1)")

if status == pywraplp.Solver.OPTIMAL:
    print('비용 최소화')
    print(f'총 비용 = ${solver.Objective().Value():.1f}')
    print(f'총 주택 수 = {X.solution_value() + Y.solution_value():.0f}개')
    print(f'총 저소득 주택 수 = {X.solution_value():.0f}개, 총 중간소득 주택 수 = {Y.solution_value():.0f}개')
else:
    print('This problem does not have an optimal solution')

# 2-2(2) 주택 수 최대화

solver.Maximize(X + Y)

status = solver.Solve()

print("\n과제 2-2(2)")

if status == pywraplp.Solver.OPTIMAL:
    print('주택 수 최대화')
    print(f'총 주택 수 = {X.solution_value() + Y.solution_value():.0f}개')
    print(f'총 비용 = ${solver.Objective().Value():.1f}')
    print(f'총 저소득 주택 수 = {X.solution_value():.0f}개, 총 중간소득 주택 수 = {Y.solution_value():.0f}개')

else:
    print('This problem does not have an optimal solution')

































    

