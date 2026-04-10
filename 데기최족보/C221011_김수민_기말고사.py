#1
from ortools.linear_solver import pywraplp
solver=pywraplp.Solver.CreateSolver('SCIP')
cost=[[23,9,23,29,33],
      [19,15,21,26,36],
      [31,11,40,40,20]]
need=[15000,40000,13000,12000,19000]
low_cost=[18000000,17500000,24500000]
low_capa=40000
high_cost=[23400000,22750000,31850000]
high_capa=60000
bigM=1000000
x={}
for i in range(3):
    for j in range(5):
        x[i,j]=solver.NumVar(0,solver.infinity(),'x[%i,%i]'%(i,j))
y={}
for i in range(3):
    y[i]=solver.BoolVar('y[%i]'%i)

for i in range(3):
    solver.Add(sum(x[i,j] for j in range(5))<=low_capa*y[i]+high_capa*(1-y[i]))
for j in range(5):
    solver.Add(sum(x[i,j] for i in range(3))>=need[j])

obj=[]
for i in range(3):
    obj.append(low_cost[i]*y[i])
    obj.append(high_cost[i]*(1-y[i]))
    for j in range(5):
        obj.append(cost[i][j]*x[i,j])
solver.Minimize(sum(obj))
status=solver.Solve()
if status==pywraplp.Solver.OPTIMAL:
    print(solver.Objective().Value())
else:
    print('a')
#2
from ortools.linear_solver import pywraplp
solver=pywraplp.Solver.CreateSolver('SCIP')
Dist=[[0,125,225,155,215],
      [125,0,85,115,135],
      [225,85,0,165,165,190],
      [155,115,165,0,195],
      [215,135,190,195,0]]
x={}
for i in range(5):
    for j in range(5):
            x[i,j]=solver.BoolVar('x[%i,%i]'%(i,j))
u={}
for i in range(1,5):
    u[i]=solver.IntVar(0,solver.infinity(),'u[%i]'%i)
for i in range(5):
    solver.Add(sum(x[i,j] for j in range(5))==1)
    solver.Add(sum(x[j,i] for j in range(5))==1)

for i in range(1,5):
    for j in range(1,5):
        solver.Add(u[i]-u[j]+x[i,j]*len(Dist)<=(len(Dist)-1))
obj=[]
for i in range(5):
    for j in range(5):
        obj.append(Dist[i][j]*x[i,j])
solver.Minimize(sum(obj))
status=solver.Solve()
if status==pywraplp.Solver.OPTIMAL:
    print(solver.Objective().Value())
    for i in range(1,5):
        print(u[i].name(),':',u[i].solution_value())

#3
from ortools.linear_solver import pywraplp
solver=pywraplp.Solver.CreateSolver('SCIP')
Cost={(0,1): 4.6, (0,2):4.7,(0,3):4.2,
      (1,4):3.5,(1,5):3.4,
      (2,4):3.6,(2,5):3.2,(2,6):3.3,
      (3,5):3.5,(3,6):3.4,
      (4,7):3.4,(5,7):3.6,(6,7):3.8}

flow=[1,0,0,0,0,0,0,-1]
x={}
for i in range(8):
    for j in range(8):
        x[i,j]=solver.BoolVar('x[%i,%i]'%(i,j))
for i in range(7):
    const=[]
    const1=[]
    for key in Cost.keys():
        if key[0]==i:
            const.append(x[key[0],key[1]])
        if key[1]==i:
            const1.append(x[key[0],key[1]])
        else:
            continue
    solver.Add(sum(const)-sum(const1)==flow[i])
obj=[]
for i in range(7):
    for j in range(7):
        if (i,j) in Cost.keys():
            obj.append(Cost[i,j]*x[i,j])
solver.Minimize(sum(obj))
status=solver.Solve()
if status==pywraplp.Solver.OPTIMAL:
    print(solver.Objective().Value())
else:
    print('a')


#4
from ortools.linear_solver import pywraplp
solver= pywraplp.Solver.CreateSolver('SCIP')
setup=[3000,2000,1000]
timecost=[700,800,900]
cost=[5,4,7]
capa=[2100,1800,3000]
needs=[2900,3900]
x={}
for i in range(3):
    for j in range(2):
        x[i,j]=solver.NumVar(0,solver.infinity(),'x[%i,%i'%(i,j))
#셋업시간 발생 여부
y={}
for i in range(3):
    y[i]=solver.BoolVar('y%i'%i)
#가동여부
z={}
for i in range(3):
    for j in range(2):
        z[i,j]=solver.BoolVar('z[%i,%i]'%(i,j))
for i in range(3):
    a=capa[i]
    for j in range(2):
        solver.Add(x[i,j]<=a*z[i,j])
for j in range(2):
    a=needs[j]
    solver.Add(sum(x[i,j] for i in range(3))>=a)
for i in range(3):
    solver.Add(z[i,1]-z[i,0]<=y[i])
obj=[]
for i in range(3):
    obj.append(setup[i]*y[i])
    for j in range(2):
        obj.append(timecost[i]*z[i,j])
        obj.append(cost[i]*x[i,j])
solver.Minimize(sum(obj))
status=solver.Solve()
if status==pywraplp.Solver.OPTIMAL:
    print(solver.Objective().Value())
else:
    print('a')

#5
from ortools.linear_solver import pywraplp
solver=pywraplp.Solver.CreateSolver('SCIP')
data=[[1,0,1,1,0],
      [1,1,1,0,1],
      [0,0,1,1,0],
      [0,1,1,1,0],
      [1,1,0,1,1],
      [1,0,0,1,0],
      [1,0,0,0,1]]
N=3
x={}
for i in range(5):
    x[i]=solver.BoolVar('x[%i]'%i)
y={}
for i in range(len(data)):
    y[i]=solver.BoolVar('y[%i]'%i)
bigM=100000
for i in range(7):
    solver.Add(sum(data[i][j]*x[j] for j in range(5))+y[i]*bigM>=sum(data[i]))

solver.Add(len(data)-sum(y[i] for i in range(7))==N)

solver.Minimize(sum(x[i] for i in range(5)))
status=solver.Solve()
if status==pywraplp.Solver.OPTIMAL:
    print(solver.Objective().Value())
else:
    print('a')

