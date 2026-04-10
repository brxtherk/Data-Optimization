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
    constraint_expr = [data['constraint_coeffs'][i][j] * x[j] for j in range(data['num_vars'])]
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





























