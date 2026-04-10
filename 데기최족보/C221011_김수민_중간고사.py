#문제1
from ortools.linear_solver import pywraplp
solver=pywraplp.Solver.CreateSolver('SCIP')

x={}
for i in range(2):
    x[i]=solver.IntVar(2,solver.infinity(),'x[%i]'%i)
y={}
for i in range(4):
    y[i]=solver.IntVar(0,solver.infinity(),'y[%i]'%i)
limit=[4,8,10,6]
for  i in range(2):
    for j in range(4):
        solver.Add(x[i]+y[j]>=limit[j])
with open('1','w') as f:
    lp=solver.ExportModelAsLpFormat(False)
    f.write(lp)
solver.Minimize(4*15000*(x[0]+x[1])+2*13000*(y[0]+y[1]+y[2]+y[3]))

status=solver.Solve()
if status==pywraplp.Solver.OPTIMAL:
    print(solver.Objective().Value())
    for i in range(2):
        print(x[i].name(),':',x[i].solution_value())
    for i in range(2):
        print(y[i].name(),':',y[i].solution_value())

#문제2
from ortools.linear_solver import pywraplp
solver=pywraplp.Solver.CreateSolver('SCIP')

x={}
for i in range(2):
    for j in range(3):
        x[i,j]=solver.IntVar(0,solver.infinity(),f'x[{i},{j}]')
y=solver.BoolVar('y')
M=1000000
z={}
for i in range(3):
    z[i]=solver.BoolVar('z[%i]'%i)
data=[[3,4,2],
      [4,6,2]]
cost=[5,7,3]
limit=[30,40]
demand=[7,5,9]
#생산시간 제약
for i in range(2):
    solver.Add(sum(data[i][j]*x[i,j] for j in range(3))<=limit[i])
#공장선택 제약약
solver.Add(sum(x[0,j] for j in range(3))<=M*y)
solver.Add(sum(x[1,j] for j in range(3))<=M*(1-y))
#제품 제약
for j in range(3):
    solver.Add(sum(x[i,j] for i in range(2))<=M*z[j]+demand[j])
solver.Add(sum(z[i] for i in range(3))<=2)

solver.Maximize(sum(cost[j]*(x[0,j]+x[1,j])for j in range(3)))

status=solver.Solve()
if status==pywraplp.Solver.OPTIMAL:
    print(f'{solver.Objective().Value():.1f}')
    for i in range(2):
        for j in range(3):
            print(x[i,j].name(),':',x[i,j].solution_value())

#문제3
from ortools.linear_solver import pywraplp
solver=pywraplp.Solver.CreateSolver('SCIP')

data=[[0,3,6],
      [1,5,8],
      [2,4,7],
      [1,2,4,8],
      [0,5,7],
      [1,3,4],
      [2,6,8],
      [3,6],
      [0,1,2],
      [1,6,7]]
time=[6,4,7,5,4,6,5,3,7,6]
x={}
for i in range(10):
    for j in range(9):
        x[i,j]=solver.BoolVar(f'x[{i},{j}]')
M=1000000
y={}
for i in range(10):
    y[i]=solver.BoolVar('y[%i]'%i)
#모든 배달 장소 제약조건
const={}
for j in range(9):
    con=[]
    for i in range(10):
        if j in data[i]:
            con.append(x[i,j])
    const[j]=con
for i in range(9):
    solver.Add(sum(const[i])>=1)
#경로 3개 선택
for i in range(10):
    solver.Add(sum(x[i,j] for j in range(9))<=M*y[i])
solver.Add(sum(y[i] for i in range(9))==3)
solver.Minimize(sum(sum(x[i,j] for j in range(9))*time[i] for i in range(10)))

status=solver.Solve()
if status==pywraplp.Solver.OPTIMAL:
    print(solver.Objective().Value())
    for i in range(10):
        for j in range(9):
            if x[i,j].solution_value()!=0:
                print(x[i,j].name(),':',x[i,j].solution_value())
    

#문제4
data=[[0,7,12,10,9],
      [6,0,10,14,11],
      [10,11,0,12,10],
      [7,8,15,0,7],
      [12,9,8,16,0],
      [4,5,8,9,4]]
from ortools.linear_solver import pywraplp
solver=pywraplp.Solver.CreateSolver('SCIP')
x={}
for i in range(6):
    for j in range(5):
        x[i,j]=solver.BoolVar(f'x[{i},{j}]')
for i in range(5):
    solver.Add(sum(x[i,j] for j in range(5))+sum(x[k,i] for k in range(6) if i!=k)==1)

solver.Maximize(sum(x[i,j]*data[i][j] for i in range(6) for j in range(5)))

status=solver.Solve()
if status==pywraplp.Solver.OPTIMAL:
    print(f'{solver.Objective().Value():.1f}')
    for i in range(6):
        for j in range(5):
            if x[i,j].solution_value()!=0:
                print(x[i,j].name(),':',x[i,j].solution_value())

#문제5
M=1000000
data=[[0.002,0.01,M,0.01,0.007],
      [M,0.01,0.002,M,0.004],
      [M,M,M,0.007,M],
      [0.003,M,M,0.006,0.008],
      [M,M,0.004,0.001,M],
      [M,0.006,0.001,M,M],
      [0.002,M,M,0.003,0.009],
      [0.004,0.008,0.005,M,M],
      [0.003,M,0.003,0.002,M]
]
demand=[2,2,2,4,2,1,1,4,1]
cost=[24,20,36,28,39]
weight=[2,3,1.5,1,4]

#문제5
from ortools.linear_solver import pywraplp
solver=pywraplp.Solver.CreateSolver('SCIP')
x={}
for i in range(9):
    for j in range(5):
        x[i,j]=solver.IntVar(0,solver.infinity(),f'x[{i},{j}]')
for i in range(9):
    solver.Add(sum(x[i,j] for j in range(5))>= demand[i])
y={}
for i in range(5):
    y[i]=solver.BoolVar('y[%i]'%i)
for j in range(5):
    solver.Add(sum(x[i,j]for i in range(9))<=M*y[j])
solver.Add(sum(y[i] for i in range(5))<=3)
con=[]
con1=[]
for j in range(5):
    con.append(weight[j]*(sum(x[i,j] for i in range(9))))
    con1.append(cost[j]*(sum(x[i,j]for i in range(9))))
solver.Add(sum(con)<=36)
solver.Add(sum(con1)<=585)
solver.Add(sum(x[i,j]for i in range(9) for j in range(5))<=24)

solver.Minimize(sum(x[i,j]*data[i][j]for i in range(9) for j in range(5)))
with open('5','w') as f:
    lp=solver.ExportModelAsLpFormat(False)
    f.write(lp)

status=solver.Solve()
if status==pywraplp.Solver.OPTIMAL:
    print(solver.Objective().Value())
    for i in range(9):
        for j in range(5):
            if x[i,j].solution_value()!=0:
                print(x[i,j].name(),':',x[i,j].solution_value())