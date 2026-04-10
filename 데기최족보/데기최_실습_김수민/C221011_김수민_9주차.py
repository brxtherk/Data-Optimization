#예제1
nCity = 6
DIST = [    
        [0, 702, 454, 842, 2396, 1196],
        [702, 0, 324, 1093, 2136, 764],
        [454, 324, 0, 1137, 2180, 798],
        [842, 1093, 1137, 0, 1616, 1857],
        [2396, 2136, 2180, 1616, 0, 2900],
        [1196, 764, 798, 1857, 2900, 0]
        ]
from ortools.linear_solver import pywraplp
solver=pywraplp.Solver.CreateSolver("SAT")

x={}
for i in range(nCity):
    for j in range(nCity):
        if i!=j:
            x[i,j]=solver.BoolVar('X'+str(i)+str(j))
            
u={}
#2<=ui<=N 
for i in range(1,nCity):
    #1번부터 순서 부여하기 위해 1,nCity-1을 범위로 사용
    u[i]=solver.IntVar(1,nCity-1,'U[%i]'%i)

#도시 j 로 한번은 들어와야 한다는 제약조건
for j in range(nCity):
    solver.Add(solver.Sum(x[i,j] for i in range(nCity) if i!=j)==1,'in_'+str(j))

#도시 j 로부터 한번은 나와야 한다는 제약조건
for j in range(nCity):
    solver.Add(solver.Sum(x[j,i] for i in range(nCity)if i!=j)==1,'in_'+str(i))

#방문순서제약
for i in range(1,nCity):
    for j in range(1, nCity):
        if i !=j:
            #i나 j가 0일 때는 제약을 안 건다. 시작도시는 무조건 첫번째 순서가 돼서 
            solver.Add(u[i]-u[j]+nCity*(x[i,j])<=nCity-1)
            
#목적함수
obj=[]
for i in range(nCity):
    for j in range(nCity):
        if i != j:
            obj.append(DIST[i][j]*x[i,j])
solver.Minimize(solver.Sum(obj))

with open('or9-1.lp','w') as out_f:
    lp_text=solver.ExportModelAsLpFormat(False)
    out_f.write(lp_text)
status=solver.Solve()
if status==pywraplp.Solver.OPTIMAL or status==pywraplp.Solver.FEASIBLE:
    print(f'Total cost = { solver.Objective().Value():.1f}\n')
    for i in range(nCity):
        for j in range(nCity):
            if i!=j:
                if x[i,j].solution_value()>0.5:
                    print(f'X{i} --> X{j}')
    for i in range(1,nCity):
        print(f'{i}방문순서: {u[i].solution_value():.0f}')
else:
    print('No solution found')

#실습1
from ortools.linear_solver import pywraplp
import pandas as pd
#index_col='Unnamed:0': 첫번째 열은 인덱스 값으로 쓴다
df=pd.read_excel(r"C:\Users\paint\OneDrive\Desktop\강의록3학년\데기최\9주차\tsp_ex_data1.xlsx",index_col='Unnamed: 0')
DIST=df.values.tolist()

solver=pywraplp.Solver.CreateSolver("SAT")
nCity=12
x={}
for i in range(nCity):
    for j in range(nCity):
        if i!=j:
            x[i,j]= solver.BoolVar('X'+str(i)+str(j))
u={}
for i in range(1,nCity):
    u[i]=solver.IntVar(1,nCity-1,'U[%i]'%i)

#도시 j로 들어오는 값 1
for j in range(nCity):
    solver.Add(sum(x[i,j] for i in range(nCity) if i!=j)==1)
#도시 j에서 나오는 값 1
for j in range(nCity):
    solver.Add(sum(x[j,i] for i in range(nCity) if i!=j)==1)
#순서 제약
for i in range(1,nCity):
    for j in range(1,nCity):
        if i!=j:
            solver.Add(u[i]-u[j]+nCity*x[i,j]<=nCity-1)
obj=[]
for i in range(nCity):
    for j in range(nCity):
        if i!=j:
            obj.append(DIST[i][j]*x[i,j])
solver.Minimize(sum(obj))
status=solver.Solve()
if status==pywraplp.Solver.OPTIMAL or status==pywraplp.Solver.FEASIBLE:
    print(f'Total cost = {solver.Objective().Value():.1f}\n')
    for i in range(nCity):
        for j in range(nCity):
            if i!=j:
                if x[i,j].solution_value()>0.5:
                    print(f'X{i} --> X{j}')
    for i in range(1,nCity):
        print(f'{i}방문순서: {u[i].solution_value():.0f}')
else:
    print('No solution found')

#실습2
from ortools.linear_solver import pywraplp
import pandas as pd
import math
import matplotlib.pyplot as plt
solver=pywraplp.Solver.CreateSolver('SAT')

def calDist(x1, y1, x2, y2):
    
    dist = math.sqrt((x1-x2)**2+(y1-y2)**2)
    
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

nPos = pd.DataFrame(columns=[ 'xc', 'yc'])

#f = open(".\\Tsp_data\\bays29.tsp", 'r')
#f = open(".\\Tsp_data\\berlin52.tsp", 'r')
#f = open(".\\Tsp_data\\att48.tsp", 'r') # 기판
f = open(r"C:\Users\paint\OneDrive\Desktop\강의록3학년\데기최\9주차\TSP_data\TSP_data\bays29.tsp", 'r') 


flag = 0

while True:  
    line = f.readline().strip()
    
    #print(line)
    if not line: break
    
    if line == "DISPLAY_DATA_SECTION":
    #if line == "NODE_COORD_SECTION":
        flag = 1
        continue
    
    if line == "EOF":
        continue
        
    if flag:
        ss = line.split()
        nPos.loc[len(nPos)] = [float(ss[1]), float((ss[2]))]
             
DIST = makeDIST(nPos)
f.close()

plt.scatter(nPos['xc'], nPos['yc'])
plt.show()

nCity = len(nPos)
x={}
for i in range(nCity):
    for j in range(nCity):
        if i!=j:
            x[i,j]= solver.BoolVar('X'+str(i)+str(j))
u={}
for i in range(1,nCity):
    u[i]=solver.IntVar(1,nCity-1,'U[%i]'%i)

#도시 j로 들어오는 값 1
for j in range(nCity):
    solver.Add(sum(x[i,j] for i in range(nCity) if i!=j)==1)
#도시 j에서 나오는 값 1
for j in range(nCity):
    solver.Add(sum(x[j,i] for i in range(nCity) if i!=j)==1)
#순서 제약
for i in range(1,nCity):
    for j in range(1,nCity):
        if i!=j:
            solver.Add(u[i]-u[j]+nCity*x[i,j]<=nCity-1)
obj=[]
for i in range(nCity):
    for j in range(nCity):
        if i!=j:
            obj.append(DIST[i][j]*x[i,j])
solver.Minimize(sum(obj))
status=solver.Solve()
if status==pywraplp.Solver.OPTIMAL or status==pywraplp.Solver.FEASIBLE:
    print(f'Total cost = {solver.Objective().Value():.1f}\n')
    for i in range(nCity):
        for j in range(nCity):
            if i!=j:
                if x[i,j].solution_value()>0.5:
                    print(f'X{i} --> X{j}')
    for i in range(1,nCity):
        print(f'{i}방문순서: {u[i].solution_value():.0f}')
else:
    print('No solution found')

#실습3(실습1번에 제약조건 추가)
from ortools.linear_solver import pywraplp
import pandas as pd
#index_col='Unnamed:0': 첫번째 열은 인덱스 값으로 쓴다
df=pd.read_excel(r"C:\Users\paint\OneDrive\Desktop\강의록3학년\데기최\9주차\tsp_ex_data1.xlsx",index_col='Unnamed: 0')
DIST=df.values.tolist()
profits = [35000, 13000, 
58000, 41000, 13000, 54000, 
65000, 48000, 69000, 56000, 
34000, 67000 ]

solver=pywraplp.Solver.CreateSolver("SAT")
nCity=12
x={}
for i in range(nCity):
    for j in range(nCity):
        if i!=j:
            x[i,j]= solver.BoolVar('X'+str(i)+str(j))
u={}
for i in range(1,nCity):
    u[i]=solver.IntVar(1,nCity-1,'U[%i]'%i)
y={}
for i in range(nCity):
    y[i]=solver.BoolVar('y[%i]'%i)

#도시 j로 들어오는 값 1 or 0
for j in range(nCity):
    solver.Add(sum(x[i,j] for i in range(nCity) if i!=j)==y[j])
#도시 j에서 나오는 값 1 or 0
for j in range(nCity):
    solver.Add(sum(x[j,i] for i in range(nCity) if i!=j)==y[j])
#도시 6개 선택
solver.Add(sum(y[i] for i in range(nCity))==6)
#신시내티는 포함된다는 조건
solver.Add(y[2]==1)
#순서 제약
i=1
for i in range(1,nCity):
    for j in range(1,nCity):
        if i!=j:
            solver.Add(u[i]-u[j]+6*x[i,j]<=5)
#목적함수
obj=[]
for i in range(nCity):
    for j in range(nCity):
        if i!=j:
            obj.append(DIST[i][j]*x[i,j])
profit=[]
for i in range(nCity):
    for j in range(nCity):
        if i!=j:
            profit.append(profits[j]*x[i,j])
solver.Minimize(sum(obj)-sum(profit))
status=solver.Solve()
if status==pywraplp.Solver.OPTIMAL or status==pywraplp.Solver.FEASIBLE:
    print(f'Total cost = {(-1)*solver.Objective().Value():.1f}\n')
    for i in range(nCity):
        for j in range(nCity):
            if i!=j:
                if x[i,j].solution_value()>0.5:
                    print(f'X{i} --> X{j}')
    for i in range(1,nCity):
        if y[i].solution_value()>0.5:
            print(f'{i}방문순서: {u[i].solution_value():.0f}')
else:
    print('No solution found')

#실습_berlin52
from ortools.linear_solver import pywraplp
import pandas as pd
import math
import matplotlib.pyplot as plt
solver=pywraplp.Solver.CreateSolver('SAT')

def calDist(x1, y1, x2, y2):
    
    dist = math.sqrt((x1-x2)**2+(y1-y2)**2)
    
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

nPos = pd.DataFrame(columns=[ 'xc', 'yc'])

#f = open(".\\Tsp_data\\bays29.tsp", 'r')
#f = open(".\\Tsp_data\\berlin52.tsp", 'r')
#f = open(".\\Tsp_data\\att48.tsp", 'r') # 기판
f = open(r"C:\Users\paint\OneDrive\Desktop\강의록3학년\데기최\9주차\TSP_data\TSP_data\berlin52.tsp", 'r') 


flag = 0

while True:  
    line = f.readline().strip()
    
    #print(line)
    if not line: break
    
    #if line == "DISPLAY_DATA_SECTION":
    if line == "NODE_COORD_SECTION":
        flag = 1
        continue
    
    if line == "EOF":
        continue
        
    if flag:
        ss = line.split()
        nPos.loc[len(nPos)] = [float(ss[1]), float((ss[2]))]
             
DIST = makeDIST(nPos)
f.close()

plt.scatter(nPos['xc'], nPos['yc'])
plt.show()

nCity = len(nPos)
x={}
for i in range(nCity):
    for j in range(nCity):
        if i!=j:
            x[i,j]= solver.BoolVar('X'+str(i)+str(j))
u={}
for i in range(1,nCity):
    u[i]=solver.IntVar(1,nCity-1,'U[%i]'%i)

#도시 j로 들어오는 값 1
for j in range(nCity):
    solver.Add(sum(x[i,j] for i in range(nCity) if i!=j)==1)
#도시 j에서 나오는 값 1
for j in range(nCity):
    solver.Add(sum(x[j,i] for i in range(nCity) if i!=j)==1)
#순서 제약
for i in range(1,nCity):
    for j in range(1,nCity):
        if i!=j:
            solver.Add(u[i]-u[j]+nCity*x[i,j]<=nCity-1)
obj=[]
for i in range(nCity):
    for j in range(nCity):
        if i!=j:
            obj.append(DIST[i][j]*x[i,j])
solver.Minimize(sum(obj))
status=solver.Solve()
if status==pywraplp.Solver.OPTIMAL or status==pywraplp.Solver.FEASIBLE:
    print(f'Total cost = {solver.Objective().Value():.1f}\n')
    for i in range(nCity):
        for j in range(nCity):
            if i!=j:
                if x[i,j].solution_value()>0.5:
                    print(f'X{i} --> X{j}')
    for i in range(1,nCity):
        print(f'{i}방문순서: {u[i].solution_value():.0f}')
else:
    print('No solution found')