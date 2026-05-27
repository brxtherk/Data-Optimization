# 정수계획 모형

from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver("SAT")

INF = solver.infinity()

# 변수 선언
x = solver.IntVar(0, 3.5, 'x')
y = solver.IntVar(0, INF, 'y')

# 제약조건
solver.Add(x + 7*y <= 17.5)

# 목적함수
solver.Maximize(x + 10*y)

# 풀이
status = solver.Solve()

# 출력
if status == pywraplp.Solver.OPTIMAL:
    print("solution")
    print(f"Objective value = {solver.Objective().Value():.0f}")
    print(f"x = {x.solution_value():.0f}")
    print(f"y = {y.solution_value():.0f}")
else:
    print("The problem does not have an optimal solution.")

# 예제 1. 스태프 결정 문제

from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver("SAT")
data = {}

REQ = [19, 14, 12, 20, 16, 13, 16]
names = ['FRI', 'SAT', 'SUN', 'MON', 'TUE', 'WED', 'THU']
data['num_vars'] = 7
data['num_constraints'] = 7

# 변수 선언
x = {}
for j in range(data['num_vars']):
    x[j] = solver.IntVar(0, solver.infinity(), names[j])

# 제약조건
for i in range(data['num_vars']):
    constraint_expr = [x[(i-j) % 7] for j in range(5)]
    solver.Add(sum(constraint_expr) >= REQ[i], names[i])

# 목적함수
objective = solver.Objective()
solver.Minimize(solver.Sum(x[i] for i in range(data['num_vars'])))

# 모델 파일 생성
with open('or4-2.lp', "w") as out_f:
    lp_text = solver.ExportModelAsLpFormat(False)
    out_f.write(lp_text)

# 풀이
status = solver.Solve()

# 출력
if status == pywraplp.Solver.OPTIMAL:
    print(f"Objective value = {objective.Value():.0f}")
    for i in range(data['num_constraints']):
        print(f"{x[i].name()} = {x[i].solution_value():.0f}")
else:
    print("The problem does not have an optimal solution.")

# 예제 2 - 팀배정 문제
from ortools.linear_solver import pywraplp

Ratings = [
    [None, 9, 3, 4, 2, 1, 5, 6],
    [None, None, 1, 7, 3, 5, 2, 1],
    [None, None, None, 4, 4, 2, 9, 2],
    [None, None, None, None, 1, 5, 5, 2],
    [None, None, None, None, None, 8, 7, 6],
    [None, None, None, None, None ,None, 2, 3],
    [None, None, None, None, None, None, None, 4]
]
data['num_vars'] = 8
data['num_constraints'] = 7

solver = pywraplp.Solver.CreateSolver("SCIP")

nC = len(Ratings[0])

# 변수 선언
X = {}
for j in range(nC):
    for i in range(nC):
        if i != j:
            X[i, j] = solver.IntVar(0, 1, "X"+str(i)+str(j))

# 제약조건
const_expr = []
for i in range(nC):
    const_expr = [X[i, j] for j in range(nC) if i != j]
    solver.Add(sum(const_expr) == 1, 'consultant_'+str(i))

# xij = xji 제약
for i in range(nC):
    for j in range(nC):
        if i < j:
            solver.Add(X[i,j] ==  X[j,i], 'x_'+str(i)+'_'+str(j))

# 목적함수
obj_expr = []
for i in range(nC-1):
    for j in range(nC):
        if Ratings[i][j] != None:
            obj_expr.append(Ratings[i][j]*X[i,j])

solver.Maximize(solver.Sum(obj_expr))

# 모델 파일 생성
with open('or4-4-lp', "w") as out_f:
    lp_text = solver.ExportModelAsLpFormat(False)
    out_f.write(lp_text)

status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL:
    print(f"Objective value = {solver.Objective().Value():.1f}")
    for i in range(nC):
        for j in range(nC):
            if i != j and X[i, j].solution_value() != 0:
                print('Consultant [%i]'%i, '--> Consultant [%i]'%i)
else:
    print("The problem does not have an optimal solution.")

# 예제3. 정수 계획 문제
from ortools.linear_solver import pywraplp
solver = pywraplp.Solver.CreateSolver("SAT")

nVARS = 4
values = [9, 5, 6, 4]
reqs = [6, 3, 5, 2]

# 의사결정변수
x = {}
for i in range(nVARS):
    x[i] = solver.IntVar(0, 1, "x[%i]"%i)

# 제약조건
solver.Add(sum([reqs[i]*x[i] for i in range(nVARS)]) <= 11, 'const 0')
solver.Add(x[2] + x[3] <= 1, 'const 1')
solver.Add(x[2] <= x[0], 'const 2')
solver.Add(x[3] <= x[1], 'const 3')

# 목적함수
solver.Maximize(sum([values[i]*x[i] for i in range(nVARS)]))

with open('or5-1,lp', "w") as out_f:
    lp_text = solver.ExportModelAsLpFormat(False)
    out_f.write(lp_text)

status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL:
    print("OPTIMAL")
    print("목적함수값 = ", solver.Objective().Value())
    for i in range(nVARS):
        print(x[i].name(), "=", x[i].solution_value())
else:
    print("The problem does not have an optimal solution.")

 