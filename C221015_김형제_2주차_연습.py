# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 01:59:28 2026

@author: redti
"""
# 예제 1: 주영이의 과일가게
# (1)
from ortools.linear_solver import pywraplp

def LinearProgrammingExample():
    solver = pywraplp.Solver.CreateSolver("GLOP")
    if not solver:
        return
    
    infinity = solver.infinity()
    
    # 변수
    x = solver.NumVar(0, infinity, "새콤주스 잔 수")
    y = solver.NumVar(0, infinity, "달콤주스 잔 수")
    print("Number of variables =", solver.NumVariables())
    
    # 제약조건
    solver.Add(4 * x + 2 * y <= 30)
    solver.Add(2 * x + 6 * y <= 40)
    print("Number of constraints =", solver.NumConstraints())
    
    # 목적함수
    solver.Maximize(500 * x + 400 * y)
    
    status = solver.Solve()
    
    if status == pywraplp.Solver.OPTIMAL:
        print("Solution")
        print(f"Objective value = {solver.Objective().Value():0.1f}")
        print(f"x = {x.solution_value():0.1f}")
        print(f"y = {y.solution_value():0.1f}")
    else:
        print("The problem does not have an optimal solution.")
        
    print(f"Problem solved in {solver.wall_time():d} milliseconds")
    print(f"Problem solved in {solver.iterations():d} iterations")
    
LinearProgrammingExample()

# (2)
from ortools.linear_solver import pywraplp

def LinearProgrammingExample():
    solver = pywraplp.Solver.CreateSolver("GLOP")
    if not solver:
        return
    
    infinity = solver.infinity()
    
    # 변수
    x = solver.NumVar(0, infinity, "새콤주스 잔 수")
    y = solver.NumVar(0, infinity, "달콤주스 잔 수")
    print("Number of variables =", solver.NumVariables())
    
    # 제약조건
    solver.Add(4 * x + 2 * y <= 30)
    solver.Add(2 * x + 6 * y <= 45)
    print("Number of constraints =", solver.NumConstraints())
    
    # 목적함수
    solver.Maximize(500 * x + 400 * y)
    
    status = solver.Solve()
    
    if status == pywraplp.Solver.OPTIMAL:
        print("Solution")
        print(f"Objective value = {solver.Objective().Value():0.1f}")
        print(f"x = {x.solution_value():0.1f}")
        print(f"y = {y.solution_value():0.1f}")
    else:
        print("The problem does not have an optimal solution.")
        
    print(f"Problem solved in {solver.wall_time():d} milliseconds")
    print(f"Problem solved in {solver.iterations():d} iterations")
    
LinearProgrammingExample()

# 예제 2 (박씨의 식단 문제)

from ortools.linear_solver import pywraplp

data = {}
data['constraint_coeffs'] = [
    [10, 0, 20, 20, 10, 20],
    [0, 10, 30, 10, 30, 20]
    ]
data['bounds'] = [50, 60]
data['obj_coeffs'] = [350, 300, 500, 340, 270, 400]
data['num_vars'] = 6
data['num_constraints'] = 2

solver = pywraplp.Solver.CreateSolver("SCIP")

infinity = solver.infinity()

# 의사결정 변수
x={}
for j in range(data['num_vars']):
    x[j] = solver.NumVar(0, infinity, "x[%i]"%j)
    
# 제약조건
for i in range(data['num_constraints']):
    constraint_expr = [data['constraint_coeffs'][i][j] * x[j] for j in range(data['num_vars'])]
    solver.Add(sum(constraint_expr) >= data['bounds'][i])
    
# 목적함수
objective = solver.Objective()
obj_expr = [data['obj_coeffs'][j] * x[j] for j in range(data['num_vars'])]
solver.Minimize(solver.Sum(obj_expr))

# 문제풀이 시작
print(f"Solving with {solver.SolverVersion()}")
status = solver.Solve()

# 결과 출력
if status == pywraplp.Solver.OPTIMAL:
    print("Objective value =", solver.Objective().Value())
    for j in range(data["num_vars"]):
        print(x[j].name(), "=", x[j].solution_value())
else:
    print("The problem does not have an optimal solution.")
                       
# 예제 3 (Chess Snackfoods Co.)

from ortools.linear_solver import pywraplp

data={}
data['constraint_coeffs'] = [
    [15, 10, 6, 2,],
    [1, 6, 10, 14]
    ]
data['supply'] = [750, 250]
data['prices'] = [2, 3, 4, 5]
data['num_vars'] = 4
data['num_constraints'] = 2

solver = pywraplp.Solver.CreateSolver("SCIP")

infinity = solver.infinity()

# 의사결정 변수
x={}
for j in range(data['num_vars']):
    x[j] = solver.NumVar(0, infinity, "x[%i]"%j)
    
# 제약조건
for i in range(data['num_constraints']):
    constraint_expr = [data['constraint_coeffs'][i][j] * x[j]/16 for j in range(data['num_vars'])]
    solver.Add(sum(constraint_expr) <= data['supply'][i])
    
# 목적함수
objective = solver.Objective()
obj_expr = [data['prices'][j] * x[j] for j in range(data['num_vars'])]
solver.Maximize(solver.Sum(obj_expr))

# 문제풀이 시작
print(f"Solving with {solver.SolverVersion()}")
status = solver.Solve()

# 결과 출력
if status == pywraplp.Solver.OPTIMAL:
    print("Solution")
    print(f"Objective value = {objective.Value():0.1f}")
    for j in range(data['num_vars']):
        print(f"{x[j]} = {x[j].solution_value()}")
else:
    print("The problem does not have an optimal solution.")
    
# 실습 1(스티글러 식단)

from ortools.linear_solver import pywraplp
from or2_4_data import *

# 솔버 객체 생성
solver = pywraplp.Solver.CreateSolver("SCIP")

# 의사결정 변수
foods = [solver.NumVar(0.0, solver.infinity(), item[0]) for item in data]

# foods = []
# for item in data:
#     food = solver.NumVar(0, solver.infinity(), item[0])
#     foods.append(food)

# 솔버 객체에 저장된 변수 개수 출력
print("Number of variables =", solver.NumVariables())

# 제약조건
constraints = []
for i, nutrient in enumerate(nutrients):
    constraints.append(solver.Constraint(nutrient[1], solver.infinity()))
    for j, item in enumerate(data):
        constraints[i].SetCoefficient(foods[j], item[i + 3])

print("Number of constraints =", solver.NumConstraints())

# 목적함수
objective = solver.Objective()
for j, food in enumerate(foods):
    objective.SetCoefficient(food, data[j][2])
objective.SetMinimization()

status = solver.Solve()

# 해 출력: 각 음식별 구매량 출력
nutrients_result=[0]*len(nutrients)
print("\nAnnual Foods:")
for i, food in enumerate(foods):
    if food.solution_value() > 0.0:
        print("{}: ${}".format(data[i][0], 365.0 * food.solution_value()))
        for j, _ in enumerate(nutrients):
            nutrients_result[j] += data[i][j + 3] * food.solution_value()
print("\nOptimal annual price: ${:.4f}".format(365.0 * objective.Value()))

print("\nNutrients per day:")
for i, nutrient in enumerate(nutrients):
    print(
        "{}: {:.2f} (min {})".format(nutrient[0], nutrients_result[i], nutrient[1])
    )


# 1
from ortools.linear_solver import pywraplp

# 솔버 생성
solver = pywraplp.Solver.CreateSolver("SCIP")

infinity = solver.infinity()
# 의사결정 변수
# x: 새콤 주스의 개수, y: 달콤 주스의 개수

x = solver.NumVar(0.0, infinity, "새콤 주스의 개수")
y = solver.NumVar(0.0, infinity, "달콤 주스의 개수")
print("Number of variables =", solver.NumVariables())

# 제약조건
# 남은 키위: 30개, 남은 딸기: 40개

solver.Add(4*x + 2*y <= 30)
solver.Add(2*x + 6*y <= 40)
print("Number of constraints =", solver.NumConstraints())

# 목적함수
# 최대이익: 500*x + 400*y 원
solver.Maximize(500*x + 400*y)

# 풀이
print(f"Solving with {solver.SolverVersion()}")
status = solver.Solve()

# 출력
if status == pywraplp.Solver.OPTIMAL:
    print("Solution")
    print(f"Objective value = {solver.Objective().Value():0.1f}")
    print(f"x = {x.solution_value():0.1f}")
    print(f"y = {y.solution_value():0.1f}")
else:
    print("The problem does not have an optimal solution.")

print(f"Problem solved in {solver.wall_time()} milliseconds")
print(f"Problem solved with {solver.iterations()} iterations")

#2

from ortools.linear_solver import pywraplp

data = {}
data['nutrient_contents'] = [
    [10, 0, 20, 20, 10, 20],
    [0, 10, 30, 10, 30, 20]
]
data['min_requirements'] = [50, 60]
data['unit_costs'] = [350, 300, 500, 340, 270, 400]
data['num_foods'] = 6
data['num_nutrients'] = 2

# 솔버 생성
solver = pywraplp.Solver.CreateSolver("SCIP")

infinity = solver.infinity()

# 의사결정 변수
# x[i] = 비타민 식단에 포함되는 식품 i의 포함량 (100g단위) i=1,2,3,4,5,6
# x[i] >= 0 (i=1,2,3,4,5,6)
x = {}
for j in range(data['num_foods']):
    x[j] = solver.NumVar(0.0, infinity, "x[%i]"%j)
print("Number of variables =", solver.NumVariables())

# 제약조건
# 1일 필수 요구량 50(비타민A), 60(비타민B)
for i in range(data['num_nutrients']):
    constraint_expr = [data['nutrient_contents'][i][j] * x[j] for j in range(data['num_foods'])]
    solver.Add(sum(constraint_expr) >= data['min_requirements'][i])
print("Number of constraints =", solver.NumConstraints())

# 목적함수
# 구입비용 최소화: 350*x1 + 300*x2 + 500*x3 + 340*x4 + 270*x5 + 400*x6 (minimize)
objective = solver.Objective()
obj_expr = [data['unit_costs'][j] * x[j] for j in range(data['num_foods'])]
solver.Minimize(solver.Sum(obj_expr))

# 풀이
print(f"Solving with {solver.SolverVersion()}")
status = solver.Solve()

# 출력
if status == pywraplp.Solver.OPTIMAL:
    print("\n==========Solution==========")
    print(f"Objective value = {objective.Value():0.1f}")
    for j in range(data['num_foods']):
        print(f"{x[j].name()} = {x[j].solution_value()}")
else:
    print("The problem does not have an optimal solution.")

print(f"Problem solved in {solver.wall_time()} milliseconds")
print(f"Problem solved with {solver.iterations()} iterations")

# 3

from ortools.linear_solver import pywraplp

# 솔버 생성
solver = pywraplp.Solver.CreateSolver("SCIP")

data = {}
data['nut_amounts'] = [  # 단위: 온즈
    [15, 10, 6, 2],
    [1, 6, 10, 14]
]
data['prices'] = [2, 3, 4, 5]
data['supply'] = [750, 250]  # 단위: 파운드
data['num_products'] = 4
data['num_nuts'] = 2
data['products_name'] = ["Pawn", "Knight", "Bishop", "King"]

infinity = solver.infinity()

# 의사결정 변수
# x[i] = 매일 생산해야 하는 제품의 파운드 양(x[i] >= 0 / i=1,2,3,4)
# x[1] = Pawn, x[2] = Knight, x[3] = Bishop, x[4] = King
x = {}
for j in range(data['num_products']):
    x[j] = solver.NumVar(0.0, infinity, data['products_name'][j])
print("Number of variables =", solver.NumVariables())

# 제약조건
# 하루 최대 공급 견과 양: 땅콩 750파운드, 캐슈 250파운드
for i in range(data['num_nuts']):
    constraint_expr = [data['nut_amounts'][i][j] * x[j] for j in range(data['num_products'])]
    solver.Add(sum(constraint_expr) <= data['supply'][i]*16)  # 단위 통일(1파운드 = 16온즈)
print("Number of constraints =", solver.NumConstraints())

# 목적함수
# 총 이익 최대화: $2*x[1] + $3*x[2] + $4*x[3] + $5*x[5] (Maximize)
obj_expr = [data['prices'][j] * x[j] for j in range(data['num_products'])]
solver.Maximize(solver.Sum(obj_expr))

# 풀이
print(f"Solving with {solver.SolverVersion()}")
status = solver.Solve()

# 출력
if status == pywraplp.Solver.OPTIMAL:
    print("\n----------Solution----------")
    print(f"Objective value = {solver.Objective().Value():0.2f}")
    for j in range(data['num_products']):
        print(f"{x[j].name()} = {x[j].solution_value()}파운드")
else:
    print("The problem does not have an optimal solution.")

print(f"Problem solved in {solver.wall_time()} milliseconds")
print(f"Problem solved with {solver.iterations()} iterations")

# 스티글러 식단

from ortools.linear_solver import pywraplp
from or2_4_data import *

# 솔버 객체 생성
solver = pywraplp.Solver.CreateSolver("SCIP")

# 의사결정 변수
foods = [solver.NumVar(0.0, solver.infinity(), item[0]) for item in data]
print("Number of variables =", solver.NumVariables())

# 제약조건
constraints = []
for i, nutrient in enumerate(nutrients):
    constraints.append(solver.Constraint(nutrient[1], solver.infinity()))
    for j, item in enumerate(data):
        constraints[i].SetCoefficient(foods[j], item[i+3])
print("Number of constraints =", solver.NumConstraints())

# 목적함수 
# objective = solver.Objective()
# for j in range(len(foods)):
#     objective.SetCoefficient(foods[j], data[j][2])
# objective.SetMinimization()

objective = solver.Objective()
for j, food in enumerate(foods):
    objective.SetCoefficient(foods[j],data[j][2])
objective.SetMinimization()

# 풀이
print(f"Solving with {solver.SolverVersion()}")
status = solver.Solve()

# 출력
if status == pywraplp.Solver.OPTIMAL:
    print("\n==========Solution==========")
    print(f"Objective value = {objective.Value():.4f} cents")
    for j, food in enumerate(foods):
        if foods[j].solution_value() > 0.0:
            print(f"{foods[j].name()} = {foods[j].solution_value():0.4f}")
else:
    print("The problem does not have an optimal solution.")

print(f"Problem solved in {solver.wall_time()} milliseconds")
print(f"Problem solved with {solver.iterations()} iterations")           





