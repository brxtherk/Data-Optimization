# 1
from ortools.linear_solver import pywraplp

def LinearProgrammingExample():
    solver = pywraplp.Solver.CreateSolver("SCIP")
    if not solver:
        return
    
    # 변수 선언
    INF = solver.infinity()
    x = solver.NumVar(0, INF, 'x')  # 만든 새콤주스 개수
    y = solver.NumVar(0, INF, 'y')  # 만든 달콤주스 개수

    print("Number of variables =", solver.NumVariables())
    
    # 제약조건
    solver.Add(4*x + 2*y <= 30)     # 남은 키위 개수: 30
    solver.Add(2*x + 6*y <= 45)     # 남은 딸기 개수: 40

    print("Number of constraints =", solver.NumConstraints())

    # 목적함수
    solver.Maximize(400*x + 500*y)  # 한 잔당 가격 (새콤주스: 500원, 달콤주스: 400원)

    # 풀이
    print(f"Solving with {solver.SolverVersion()}")
    status = solver.Solve()

    # 출력
    if status == pywraplp.Solver.OPTIMAL:
        print("\n===== Solution =====")
        print(f"Objective value = {solver.Objective().Value():0.0f}원")
        print(f"x = {x.solution_value():0.0f}잔")
        print(f"y = {y.solution_value():0.0f}잔")
    else:
        print("The problem does not have an optimal solution.")

    print("\nAdvanced usage")
    print(f"Problem solved in {solver.wall_time} milliseconds")
    print(f"Problem solved with {solver.iterations()} iterations")

LinearProgrammingExample()

# 2
from ortools.linear_solver import pywraplp
solver = pywraplp.Solver.CreateSolver("SCIP")

data = {}
data['vitamin_coeffs'] = [
    [10, 0, 20, 20, 10, 20],
    [0, 10, 30, 10, 30, 20]
]
data['req'] = [50, 60]
data['cost_coeffs'] = [350, 300, 500, 340, 270, 400]
data['num_vars'] = 5
data['num_constraints'] = 2

# 변수 선언
x = {}
INF = solver.infinity()
for j in range(data['num_vars']):
    x[j] = solver.NumVar(0, INF, "x[%i]"%(j+1))
print("Number of variables =", solver.NumVariables())

# 제약조건
for i in range(data['num_constraints']):
    constraints_expr = [data['vitamin_coeffs'][i][j] * x[j] for j in range(data['num_vars'])]
    solver.Add(sum(constraints_expr) >= data['req'][i])

print("Number of constraints =", solver.NumConstraints())

# 목적함수
obj_expr = [data['cost_coeffs'][j] * x[j] for j in range(data['num_vars'])]
solver.Minimize(solver.Sum(obj_expr))

# 풀이
print(f"Solving with {solver.SolverVersion()}")
status = solver.Solve()

# 출력
if status == pywraplp.Solver.OPTIMAL:
    print("\n=====Solution=====")
    print(f'Objective value = {solver.Objective().Value():0.1f}(원/100g)')
    for j in range(data['num_vars']):
        print(f'{x[j].name()} = {x[j].solution_value():0.1f}개')
else:
    print("The problem does not have an optimal solution")

# 3
from ortools.linear_solver import pywraplp
solver = pywraplp.Solver.CreateSolver("SCIP")
data = {}
data['nuts_coeffs'] = [
    [15, 10, 6, 2],
    [1, 6, 10, 14]
]
data['supply'] = [12000, 4000]      # 공급량 단위 파운드 -> 온즈
data['profit_coeffs'] = [2, 3, 4, 5]
data['num_vars'] = 4
data['num_constraints'] = 2
data['names'] = ['Pawn', 'Knight', 'Bishop', 'King']

# 변수 선언
INF = solver.infinity()
for j in range(data['num_vars']):
    x[j] = solver.NumVar(0.0, INF, data['names'][j] )

print("Number of variables =", solver.NumVariables())

# 제약조건
for i in range(data['num_constraints']):
    constraints_expr = [data['nuts_coeffs'][i][j] * x[j] for j in range(data['num_vars'])]
    solver.Add(sum(constraints_expr) <= data['supply'][i])

# 목적함수
obj_expr = [data['profit_coeffs'][j] * x[j] for j in range(data['num_vars'])]
solver.Maximize(solver.Sum(obj_expr))

# 풀이
print(f"Solving with {solver.SolverVersion()}")
status = solver.Solve()

# 출력
if status == pywraplp.Solver.OPTIMAL:
    print('\n===== Solution =====')
    print(f'Objective value = {solver.Objective().Value():0.1f}')
    for j in range(data['num_vars']):
        print(f'{x[j].name()} = {x[j].solution_value():0.1f}')
else:
    print("The problem does not have an optimal solution.")