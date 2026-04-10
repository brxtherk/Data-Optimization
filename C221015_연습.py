# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

# 예제

"""Linear optimization example."""
from ortools.linear_solver import pywraplp

def LinearProgrammingExample():
    """Linear programming sample."""
    solver = pywraplp.Solver.CreateSolver("SCIP")
    if not solver:
        return
    
    #variables
    x=solver.NumVar(0,solver.infinity(),'x')
    y=solver.NumVar(0,solver.infinity(),'y')
    print("Number of variables =", solver.NumVariables())
    
    #constraints
    solver.Add(x + 2*y <= 14.0)
    solver.Add(3*x - y >= 0.0)
    solver.Add(x - y <= 2.0)
    print("Number of constraints =", solver.NumConstraints())

    # objective function
    solver.Maximize(3*x + 4*y)
    
    #Solve the system.
    print(f'solving with {solver.SolverVersion()}')
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print("Solution:")
        print(f"Objective value = {solver.Objective().Value():0.1f}")
        print(f"x = {x.solution_value():0.1f}")
        print(f"y = {y.solution_value():0.1f}")
    else:
        print("The problem does not have an optimal solution.")
    print("\nAdvanced usage:")
    print(f"Problem solved in {solver.wall_time():d} milliseconds")
    print(f"Problem solved in {solver.iterations():d} iterations")
    
LinearProgrammingExample()

# 실습 1

def LinearProgrammingExample():
    """Linear programming sample."""
    solver = pywraplp.Solver.CreateSolver("SCIP")
    if not solver:
        return
    
    #variables
    x=solver.IntVar(0,solver.infinity(),'x')
    y=solver.IntVar(0,solver.infinity(),'y')
    print("Number of variables =", solver.NumVariables())
    
    #constraints
    solver.Add(x + 2*y <= 13.0)
    solver.Add(3*x - y >= 0.0)
    solver.Add(x - y <= 2.0)
    print("Number of constraints =", solver.NumConstraints())

    # objective function
    solver.Maximize(3*x + 4*y)
    
    #Solve the system.
    print(f'solving with {solver.SolverVersion()}')
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print("Solution:")
        print(f"Objective value = {solver.Objective().Value():0.1f}")
        print(f"x = {x.solution_value():0.1f}")
        print(f"y = {y.solution_value():0.1f}")
    else:
        print("The problem does not have an optimal solution.")
    print("\nAdvanced usage:")
    print(f"Problem solved in {solver.wall_time():d} milliseconds")
    print(f"Problem solved in {solver.iterations():d} iterations")
    
LinearProgrammingExample()

# 실습 2

def LinearProgrammingExample():
    """Linear programming sample."""
    solver = pywraplp.Solver.CreateSolver("SCIP")
    if not solver:
        return
    
    #variables
    x=solver.IntVar(0,solver.infinity(),'x')
    y=solver.IntVar(0,solver.infinity(),'y')
    
    #새로운 정수 변수 추가
    b=solver.IntVar(0,solver.infinity(),'b')
    print("Number of variables =", solver.NumVariables())
    
    #constraints
    solver.Add(x + 2*y <= 13.0)
    solver.Add(3*x - y >= 0.0)
    solver.Add(x - y <= 2.0)
    solver.Add(x == 2*b)
    #x%2==0 조건 추가했지만 선형 프로그래밍 솔버에서 모듈로 연산(%)을 지원하지 않음
    #새로운 변수 b 추가하여 짝수 조건을 추가함
    print("Number of constraints =", solver.NumConstraints())

    # objective function
    solver.Maximize(3*x + 4*y)
    
    #Solve the system.
    print(f'solving with {solver.SolverVersion()}')
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print("Solution:")
        print(f"Objective value = {solver.Objective().Value():0.1f}")
        print(f"x = {x.solution_value():0.1f}")
        print(f"y = {y.solution_value():0.1f}")
    else:
        print("The problem does not have an optimal solution.")
    print("\nAdvanced usage:")
    print(f"Problem solved in {solver.wall_time():d} milliseconds")
    print(f"Problem solved in {solver.iterations():d} iterations")
    
LinearProgrammingExample()

# 실습 3

data={}

# 제약 조건의 계수 목록
data['constraint_coeffs']=[
    [5,7,9,2,1],
    [18,4,-9,10,12],
    [4,7,3,8,5],
    [5,13,16,3,-7],
    ]

# 제약 조건의 우변 값
data['bounds']=[250,285,211,315]

# 목적 함수의 계수 목록
data['obj_coeffs'] = [7,8,2,9,6]

# 변수 개수
data['num_vars']=5

# 제약조건 개수
data['num_constraints']=4

# 최적화모형 solver을 SCIP로 지정
solver= pywraplp.Solver.CreateSolver('SCIP')

infinity=solver.infinity()

#x1~x5 변수에 0보다 크거나 같은 정수 대입 과정, 이름x[j]
x={}
for j in range(data['num_vars']):
    x[j]=solver.IntVar(0,infinity,'x[%i]'%j)
    
#제약조건도 for문을 활용해 solver.Add에 넣기
#제약 조건 개수만큼 반복
for i in range(data['num_constraints']):
    #계수와 변수를 합치는 과정
    constraint_expr=[data['constraint_coeffs'][i][j]*x[j] for j in range(data['num_vars'])]
    #제약조건의 좌변과 우변을 합쳐 solver.Add에 완전한 제약 조건을 넣는 과정
    solver.Add(sum(constraint_expr)<=data['bounds'][i])

#목적함수
objective=solver.Objective()
#목적함수는 하나이므로 변수에 대한 for 문만 작성함
obj_expr=[data['obj_coeffs'][j]*x[j] for j in range(data['num_vars'])]
#목적함수 최대화
solver.Maximize(solver.Sum(obj_expr))
#solver 유형 프린트(SCIP)
print(f"Solving with {solver.SolverVersion()}")

status = solver.Solve()
#값이 최적화 값이랑 같으면 목적함수 값 프린트
if status==pywraplp.Solver.OPTIMAL:
    print('Objective value = ',solver.Objective().Value())
    for j in range(data['num_vars']):
        print(x[j].name(),'=',x[j].solution_value())
else:
    print('The problem does not have an optimal solution.')
