# 예제 1

from ortools.linear_solver import pywraplp

nCity = 6

DIST = [ [0, 702, 454, 842, 2396, 1196],
[702, 0, 324, 1093, 2136, 764],
[454, 324, 0, 1137, 2180, 798],
[842, 1093, 1137, 0, 1616, 1857],
[2396, 2136, 2180, 1616, 0, 2900],
[1196, 764, 798, 1857, 2900, 0]
]

solver = pywraplp.Solver.CreateSolver("SAT")

X = {}
for i in range(nCity):
    for j in range(nCity):
        if i != j:
            X[i, j] = solver.IntVar(0, 1, "X"+str(i)+str(j))
        
U = {}
for i in range(1, nCity):
    U[i] = solver.IntVar(1, nCity-1, "U[%i]" %i)

# 제약조건
# 도시 j로 한 번은 들어와야 한다.
for j in range(nCity):
    solver.Add(solver.Sum([X[i, j] for i in range(nCity) if i != j]) == 1, 'in_'+str(i))

# 도시 j로 부터 한 번은 나와야 한다.
for i in range(nCity):
    solver.Add(solver.Sum([X[i, j] for j in range(nCity) if i != j]) == 1, 'out_'+str(i))

# 방문 순서 제약
for i in range(1, nCity):
    for j in range(1, nCity):
        if i != j:
            solver.Add(U[i] - U[j] + 1 - (nCity-1)*(1-X[i,j]) <= 0, 'U_'+str(i)+str(j))

# Objective
objective_terms = []
for i in range(nCity):
    for j in range(nCity):
        if i != j:
            objective_terms.append(DIST[i][j] * X[i, j])
solver.Minimize(solver.Sum(objective_terms))

if 1:
    with open('or7-1.lp', "w") as out_f:
        lp_text = solver.ExportModelAsLpFormat(False)
        out_f.write(lp_text)

# Solve
status = solver.Solve()

# Print solution.
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print(f"Total cost = {solver.Objective().Value():.1f}\n", )
    for i in range(nCity):
        for j in range(nCity):
            if i != j:
                if X[i, j].solution_value() > 0.5:
                    print(f"X{i} --> X{j}")
    for i in range(1, nCity):
        print(f"{i} 도시 방문순서: ", U[i].solution_value())
else:
    print("No solution found.")

# 실습 1
from ortools.linear_solver import pywraplp
import pandas as pd
import math
import matplotlib.pyplot as plt

nCity = 12

df = pd.read_excel('./tsp_ex_data1.xlsx', index_col = 'Unnamed: 0')
DIST = df.values.tolist()

solver = pywraplp.Solver.CreateSolver("SAT")

X = {}
for i in range(nCity):
    for j in range(nCity):
        if i!= j:
            X[i,j] = solver.IntVar(0, 1, "X"+str(i)+str(j))

U = {}
for i in range(1, nCity):
    U[i] = solver.IntVar(1, nCity-1, "U[%i]"%i)

# 제약조건
for j in range(nCity):
    solver.Add(solver.Sum([X[i,j] for i in range(nCity) if i != j]) == 1, 'in_'+str(i))

for i in range(nCity):
    solver.Add(solver.Sum([X[i,j] for j in range(nCity) if i != j]) == 1, 'out_'+str(i))

for i in range(1, nCity):
    for j in range(1, nCity):
        if i != j:
            solver.Add(U[i] - U[j] + 1 - (nCity-1)*(1-X[i,j]) <= 0, 'U_'+str(i)+str(j))

# 목적함수
objective_terms = []
for i in range(nCity):
    for j in range(nCity):
        if i != j:
            objective_terms.append(DIST[i][j]*X[i,j])
solver.Minimize(solver.Sum(objective_terms))

if 1:
    with open('or7-2.lp', "w") as out_f:
        lp_text = solver.ExportModelAsLpFormat(False)
        out_f.write(lp_text)

# Solve
status = solver.Solve()

# Print solution
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print(f"Total cost = {solver.Objective().Value():.1f}\n",)
    for i in range(nCity):
        for j in range(nCity):
            if i!= j:
                if X[i,j].solution_value() > 0.5:
                    print(f"X{i} --> X{j}")
    for i in range(1, nCity):
        print(f"{i}도시 방문 순서: ",U[i].solution_value())
else:
    print("No solution found.")

# 실습 2
from ortools.linear_solver import pywraplp
import pandas as pd
import math
import matplotlib.pyplot as plt




def calDist(x1, y1, x2, y2):

    dist = math.sqrt((x1-x2)**2 + (y1-y2)**2)

    return dist

def makeDIST(nP):

    DIST = list()
    nCity = len(nP)

    for i in range(nCity):
        DIST.append([])
        for j in range(nCity):
            if j != i:
                temp = calDist(nP['xc'][i], nP['yc'][i], nP['xc'][j], nP['yc'][j])
                DIST[i].append(temp)
            else:
                DIST[i].append(0)

    return DIST

#AIN FLOW
nPos = pd.DataFrame(columns=['xc', 'yc'])
f = open(".\\Tsp_data\\bays29.tsp", 'r')
#f = open(".\\Tsp_data\\berlin52.tsp", 'r')

flag = 0

while True:
    line = f.readline().strip()
    
    if not line: break

    if line == "DISPLAY_DATA_SECTION":
        flag = 1
        continue

    if line == "EOF":
        continue

    if flag:
        ss = line.split()
        nPos.loc[len(nPos)] = [float(ss[1]), float((ss[2]))]

DIST = makeDIST(nPos)
final_sol = []

print(DIST)

f.close()


plt.scatter(nPos['xc'], nPos['yc'])
plt.show()

# 실습 3  - 옵션 방문 TSP
from ortools.linear_solver import pywraplp
import pandas as pd
import math
import matplotlib.pyplot as plt

nCity = 12
profits = [35000, 13000, 58000, 41000, 13000, 54000,
           65000, 48000, 69000, 56000, 34000, 67000]

df = pd.read_excel('./tsp_ex_data1.xlsx', index_col = 'Unnamed: 0')
DIST = df.values.tolist()


solver = pywraplp.Solver.CreateSolver("SAT")

X = {}
for i in range(nCity):
    for j in range(nCity):
        if i!= j:
            X[i,j] = solver.IntVar(0, 1, "X"+str(i)+str(j))

Y = {}
for i in range(nCity):
    Y[i] = solver.IntVar(0, 1, "Y"+str(i))

U = {}
for i in range(1, nCity):
    U[i] = solver.IntVar(1, nCity-1, "U[%i]"%i)

# 제약조건
# 신시내티 무조건 방문
solver.Add(Y[2] == 1)

# 반드시 6개 도시를 방문해야 함
solver.Add(solver.Sum([Y[i] for i in range(nCity)]) == 6)

for j in range(nCity):
    solver.Add(solver.Sum([X[i,j] for i in range(nCity) if i != j]) == Y[j], 'in_'+str(i))

for i in range(nCity):
    solver.Add(solver.Sum([X[i,j] for j in range(nCity) if i != j]) == Y[i], 'out_'+str(i))

for i in range(1, nCity):
    for j in range(1, nCity):
        if i != j:
            solver.Add(U[i] - U[j] + 1 - (nCity-1)*(1-X[i,j]) <= 0, 'U_'+str(i)+str(j))

# 목적함수
objective_terms = []
for i in range(nCity):
    for j in range(nCity):
        if i != j:
            objective_terms.append(DIST[i][j]*X[i,j])

for i in range(nCity):
    objective_terms.append(-profits[i]*Y[i])

solver.Minimize(solver.Sum(objective_terms))

if 1:
    with open('or7-3.lp', "w") as out_f:
        lp_text = solver.ExportModelAsLpFormat(False)
        out_f.write(lp_text)

# Solve
status = solver.Solve()

# Print solution
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print(f"Total cost = {solver.Objective().Value():.1f}\n",)
    for i in range(nCity):
        for j in range(nCity):
            if i!= j:
                if X[i,j].solution_value() > 0.5:
                    print(f"X{i} --> X{j}")
    for i in range(1, nCity):
        print(f"{i}도시 방문 순서: ",U[i].solution_value())
else:
    print("No solution found.")
    
# 모델링

from ortools.linear_solver import pywraplp

nCity = 4

DIST = [ [0, 13, 25, 15],
         [13, 0, 9999, 21],
         [25, 26, 0, 11],
         [15, 9999, 11, 0],
        ]

solver = pywraplp.Solver.CreateSolver("SCIP")

X = {}
for i in range(nCity):
    for j in range(nCity):
        if i != j:
            X[i, j] = solver.IntVar(0, 1, "X"+str(i)+str(j))
        
U = {}
for i in range(1, nCity):
    U[i] = solver.IntVar(1, nCity-1, "U[%i]" %i)

# 제약조건
# 도시 j로 한 번은 들어와야 한다.
for j in range(nCity):
    solver.Add(solver.Sum([X[i, j] for i in range(nCity) if i != j]) == 1, 'in_'+str(i))

# 도시 j로 부터 한 번은 나와야 한다.
for i in range(nCity):
    solver.Add(solver.Sum([X[i, j] for j in range(nCity) if i != j]) == 1, 'out_'+str(i))

# 방문 순서 제약
for i in range(1, nCity):
    for j in range(1, nCity):
        if i != j:
            solver.Add(U[i] - U[j] + 1 - (nCity-1)*(1-X[i,j]) <= 0, 'U_'+str(i)+str(j))

# Objective
objective_terms = []
for i in range(nCity):
    for j in range(nCity):
        if i != j:
            objective_terms.append(DIST[i][j] * X[i, j])
solver.Minimize(solver.Sum(objective_terms))

if 1:
    with open('or7-1.lp', "w") as out_f:
        lp_text = solver.ExportModelAsLpFormat(False)
        out_f.write(lp_text)

# Solve
status = solver.Solve()

# Print solution.
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print(f"Total cost = {solver.Objective().Value():.1f}\n", )
    for i in range(nCity):
        for j in range(nCity):
            if i != j:
                if X[i, j].solution_value() > 0.5:
                    print(f"X{i} --> X{j}")
    for i in range(1, nCity):
        print(f"{i} 도시 방문순서: ", U[i].solution_value())
else:
    print("No solution found.")