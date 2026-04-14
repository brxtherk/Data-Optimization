# 1
from ortools.linear_solver import pywraplp

def LinearProgrammingExample():                           # 함수 생성 방법
    
    # 솔버 생성
    solver = pywraplp.Solver.CreateSolver("GLOP")
    if not solver:
        return
    
    # 변수 선언
    x = solver.NumVar(0.0, solver.infinity(), 'x')
    y = solver.NumVar(0.0, solver.infinity(), 'y')
    print(f"Number of variables = {solver.NumVariables()}")

    # 제약조건
    solver.Add(x + 2*y <= 14)
    solver.Add(3*x - y >= 0)
    solver.Add(x - y <= 2)
    print(f"Number of constraints = {solver.NumConstraints()}")
    
    # 목적함수
    solver.Maximize(3*x + 4*y)

    # 솔버 실행
    print(f"Solving with {solver.SolverVersion()}")
    status = solver.Solve()

    # 결과 출력
    if status == pywraplp.Solver.OPTIMAL:
        print("\n===== Solution =====")
        print(f'Objective value = {solver.Objective().Value():0.1f}')
        print(f'x = {x.solution_value():0.1f}')
        print(f'y = {y.solution_value():0.1f}')
    else:
        print("The problem does not have an optimal solution.")

    # 계산 정보
    print("\nAdvanced usage.")
    print(f"Problem solved in {solver.wall_time()} milliseconds")
    print(f"Problem solved in {solver.iterations()} iterations")

LinearProgrammingExample()

# 2
from ortools.linear_solver import pywraplp

def LinearProgrammingExample():                           # 함수 생성 방법
    
    # 솔버 생성
    solver = pywraplp.Solver.CreateSolver("SCIP")
    if not solver:
        return
    
    # 변수 선언
    x = solver.IntVar(0.0, solver.infinity(), 'x')
    y = solver.IntVar(0.0, solver.infinity(), 'y')
    print(f"Number of variables = {solver.NumVariables()}")

    # 제약조건
    solver.Add(x + 2*y <= 13.0)
    solver.Add(3*x - y >= 0.0)
    solver.Add(x - y <= 2.0)
    print(f"Number of constraints = {solver.NumConstraints()}")
    
    # 목적함수
    solver.Maximize(3*x + 4*y)

    # 솔버 실행
    print(f"Solving with {solver.SolverVersion()}")
    status = solver.Solve()

    # 결과 출력
    if status == pywraplp.Solver.OPTIMAL:
        print("\n===== Solution =====")
        print(f'Objective value = {solver.Objective().Value():0.1f}')
        print(f'x = {x.solution_value():0.1f}')
        print(f'y = {y.solution_value():0.1f}')
    else:
        print("The problem does not have an optimal solution.")

    # 계산 정보
    print("\nAdvanced usage.")
    print(f"Problem solved in {solver.wall_time()} milliseconds")
    print(f"Problem solved in {solver.iterations()} iterations")

LinearProgrammingExample()

# 3
from ortools.linear_solver import pywraplp

def LinearProgrammingExample():                           # 함수 생성 방법
    
    # 솔버 생성
    solver = pywraplp.Solver.CreateSolver("SCIP")
    if not solver:
        return
    
    # 변수 선언
    x = solver.IntVar(0.0, solver.infinity(), 'x')
    y = solver.IntVar(0.0, solver.infinity(), 'y')
    b = solver.IntVar(0.0, solver.infinity(), 'b')
    print(f"Number of variables = {solver.NumVariables()}")

    # 제약조건
    solver.Add(x + 2*y <= 13.0)
    solver.Add(3*x - y >= 0.0)
    solver.Add(x - y <= 2.0)
    solver.Add(x == 2*b)
    print(f"Number of constraints = {solver.NumConstraints()}")
    
    # 목적함수
    solver.Maximize(3*x + 4*y)

    # 솔버 실행
    print(f"Solving with {solver.SolverVersion()}")
    status = solver.Solve()

    # 결과 출력
    if status == pywraplp.Solver.OPTIMAL:
        print("\n===== Solution =====")
        print(f'Objective value = {solver.Objective().Value():0.1f}')
        print(f'x = {x.solution_value():0.1f}')
        print(f'y = {y.solution_value():0.1f}')
    else:
        print("The problem does not have an optimal solution.")

    # 계산 정보
    print("\nAdvanced usage.")
    print(f"Problem solved in {solver.wall_time()} milliseconds")
    print(f"Problem solved in {solver.iterations()} iterations")

LinearProgrammingExample()

# 4
from ortools.linear_solver import pywraplp
data = {}
data['constraint_coeffs'] = [
    [5, 7, 9, 2, 1],
    [18, 4, -9, 10, 12],
    [4, 7, 3, 8, 5],
    [5, 13, 16, 3, -7]
]
data['obj_coeffs'] = [7, 8, 2, 9, 6]
data['bounds'] = [250, 285, 211, 315]
data['num_vars'] = 5
data['num_constraints'] = 4

# 솔버 생성
solver = pywraplp.Solver.CreateSolver("SCIP")
infinity = solver.infinity()

# 변수 선언
x = {}
for j in range(data['num_vars']):
    x[j] = solver.IntVar(0, infinity, "x[%i]" %(j+1))

print("Number of variables =", solver.NumVariables())

# 제약 조건
for i in range(data['num_constraints']):
    constraints_expr = [data['constraint_coeffs'][i][j] * x[j] for j in range(data['num_vars'])]
    solver.Add(sum(constraints_expr) <= data['bounds'][i])

print("Number of constraints =", solver.NumConstraints())

# 목적 함수
obj_expr = [data['obj_coeffs'][j] * x[j] for j in range(data['num_vars'])]
solver.Maximize(solver.Sum(obj_expr))

# 풀이
status = solver.Solve()
print(f'Solving with {solver.SolverVersion()}')

# 출력
if status == pywraplp.Solver.OPTIMAL:
    print("\n===== Solution =====")
    print(f'Objective value = {solver.Objective().Value():.0f}')
    for j in range(data['num_vars']):
        print(f'{x[j].name()} = {x[j].solution_value():.0f}')
else:
    print("The problem does not have an optimal solution.")

 # 계산 정보
print("\nAdvanced usage.")
print(f"Problem solved in {solver.wall_time()} milliseconds")
print(f"Problem solved in {solver.iterations()} iterations")


