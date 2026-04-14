# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 00:26:23 2026

@author: redti
"""

from ortools.linear_solver import pywraplp

def LinearProgrammingExample():
    solver = pywraplp.Solver.CreateSolver("SCIP")
    if not solver:
        return
    
    x = solver.NumVar(0, solver.infinity(), "x")
    y = solver.NumVar(0, solver.infinity(), "y")
    print("Number of variables =", solver.NumVariables())
    
    solver.Add(x + 2 * y <= 14.0)
    solver.Add(3 * x - y >= 0.0)
    solver.Add(x - y <= 2.0)
    print("Number of Constraints =", solver.NumConstraints())
    
    solver.Maximize(3 * x + 4 * y)
    
    print("Solving with {solver.SolverVersion()}")
    status = solver.Solve()
    
    if status == pywraplp.Solver.OPTIMAL:
        print("Solution")
        print(f"Objective value = {solver.Objective().Value():0.1f}")
        print(f"x = {x.solution_value():0.1f}")
        print(f"y = {y.solution_value():0.1f}")
    else:
        print("The problem does not have an optimal solution.")
        
    # 계산 정보
    print(f"Problem solved in {solver.wall_time():d} milliseconds")
    print(f"Problem solved in {solver.iterations():d} iterations")
    
LinearProgrammingExample()

# 실습 1

from ortools.linear_solver import pywraplp

def LinearProgrammingExample():
    solver = pywraplp.Solver.CreateSolver("SCIP")
    if not solver:
        return
    
    # 변수
    
    x = solver.IntVar(0, solver.infinity(), "x")
    y = solver.IntVar(0, solver.infinity(), "y")
    
    # 제약조건
    
    solver.Add(x + 2 * y <= 13.0)
    solver.Add(3 * x - y >= 0.0)
    solver.Add(x - y <= 2.0)
    
    # 목적함수
    
    solver.Maximize(3 * x + 4 * y)
    
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

# 실습 2

from ortools.linear_solver import pywraplp

def LinearProgrammingExample():
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        return
    
    # 변수
    
    x = solver.IntVar(0, solver.infinity(), "x")
    y = solver.IntVar(0, solver.infinity(), "y")
    k = solver.IntVar(0, solver.Infinity(), "k")
    
    # 제약조건
    
    solver.Add(x + 2 * y <= 13.0)
    solver.Add(3 * x - y >= 0.0)
    solver.Add(x - y <= 2.0)
    solver.Add(x == 2 * k)
    
    # 목적함수
    
    solver.Maximize(3 * x + 4 * y)
    
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

# 실습 3

from ortools.linear_solver import pywraplp

data={}
data["constraint_coeffs"] = [
    [5, 7, 9, 2, 1],
    [18, 4, -9, 10, 12],
    [4, 7, 3, 8, 5],
    [5, 13, 16, 3, -7]
]
data["bounds"] = [250, 285, 211, 315]
data["obj_coeffs"] = [7, 8, 2, 9, 6]
data["num_vars"] = 5
data["num_constraints"] = 4

# Create the mip solver with the SCIP backend
solver = pywraplp.Solver.CreateSolver("SCIP")

infinity = solver.infinity()

x={}
for j in range(data["num_vars"]):
    x[j] = solver.IntVar(0, infinity, "x[%i]"%j)
    
# 제약조건
for i in range(data['num_constraints']):
    constraint_expr = [data['constraint_coeffs'][i][j] * x[j] for j in range(data['num_vars'])]
    solver.Add(sum(constraint_expr) <= data['bounds'][i])
    
# 목적함수
objective = solver.Objective()
obj_expr = [data['obj_coeffs'][j] * x[j] for j in range(data['num_vars'])]
solver.Maximize(solver.Sum(obj_expr))

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
                  

#1
from ortools.linear_solver import pywraplp

# 솔버 생성
def LinearProgrammingExample():
    solver = pywraplp.Solver.CreateSolver("GLOP")
    if not solver:
        return
    
    # 의사결정 변수
    x = solver.NumVar(0.0, solver.infinity(), "x")
    y = solver.NumVar(0.0, solver.infinity(), "y")
    print("Number of Variables =", solver.NumVariables())

    # 제약조건
    solver.Add(x + 3*y <= 14.0)
    solver.Add(3*x - y >= 0.0)
    solver.Add(x - y <= 2.0)
    print("Number of constraints =", solver.NumConstraints())

    # 목적함수
    solver.Maximize(3*x + 4*y)

    # 실행
    status = solver.Solve()

    # 출력
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

#2
from ortools.linear_solver import pywraplp

# 솔버 생성
def LinearProgrammingExample():
    solver = pywraplp.Solver.CreateSolver("SCIP")
    if not solver:
        return
    
    # 의사결정 변수
    x = solver.IntVar(0.0, solver.infinity(), "x")
    y = solver.IntVar(0.0, solver.infinity(), "y")
    k = solver.IntVar(0.0, solver.infinity(), "k")
    print("Number of Variables =", solver.NumVariables())

    # 제약조건
    solver.Add(x + 3*y <= 13.0)
    solver.Add(3*x - y >= 0.0)
    solver.Add(x - y <= 2.0)
    solver.Add(x == 2*k)
    print("Number of constraints =", solver.NumConstraints())

    # 목적함수
    solver.Maximize(3*x + 4*y)

    # 실행
    status = solver.Solve()

    # 출력
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

# 3
from ortools.linear_solver import pywraplp

data = {}
data['constraint_coeffs'] = [
    [5, 7, 9, 2, 1],
    [18, 4, -9, 10, 12],
    [4, 7, 3, 8, 5],
    [5, 13, 16, 3, -7]
]
data['bounds'] = [250, 285, 211, 315]
data['obj_coeffs'] = [7, 8, 2, 9, 6]
data['num_vars'] = 5
data['num_constraints'] = 4

# 솔버 생성
solver = pywraplp.Solver.CreateSolver("SCIP")
infinity = solver.infinity()

# 의사결정 변수
x = {}
for j in range(data['num_vars']):
    x[j] = solver.IntVar(0.0, infinity, "x[%i]"%j)
    print("Number of variables", solver.NumVariables())

# 제약조건
for i in range(data['num_constraints']):
    constraint_expr = [data['constraint_coeffs'][i][j] * x[j] for j in range(data['num_vars'])]
    solver.Add(sum(constraint_expr) <= data['bounds'][i])
    print("Number of constraints =", solver.NumConstraints())

# 목적함수
objective = solver.Objective()
obj_expr = [data['obj_coeffs'][j] * x[j] for j in range(data['num_vars'])]
solver.Maximize(solver.Sum(obj_expr))

# 풀이
status = solver.Solve()

# 출력
if status == pywraplp.Solver.OPTIMAL:
    print("Solution")
    print(f"Objective value = {objective.Value():0.0f}")
    for j in range(data['num_vars']):
        print(f"{x[j].name()} = {x[j].solution_value()}")
else:
    print("The problem does not have an optimal solution.")



























