#문제1
#새로운 공장 설립 L or S or Both
#최대 하나의 warehouse < 새로운 공장이 있는 데에만 설립 가능
present=[9,5,6,4]
required=[6,3,5,2]
from ortools.linear_solver import pywraplp
solver=pywraplp.Solver.CreateSolver('SAT')
#설립:1, 설립x:0
x={}
for i in  range(4):
    x[i]=solver.IntVar(0,1,'x[%i]'%i)

#어디에 공장을 세울 것인가(최소 한 지역 이상)
solver.Add(x[0]+x[1]>=1)

#L에 공장 설립 시만 L에 warehouse에서 설립 가능
solver.Add(x[0]>=x[2])
#S
solver.Add(x[1]>=x[3])
#warehouse는 최대 한개 설립 가능
solver.Add(x[2]+x[3]<=1)
#자원 10million
solver.Add(sum([x[i]*required[i] for i in range(4)])<=10)
#목적함수 이익 최대화
#목적함수는 사용한 비용 고려 안 한 total net Present value라고 문제에서 주어진다.
value=sum([x[i]*present[i] for i in range(4)])
#투자 비용을 빼는 것 x
solver.Maximize(value)

status=solver.Solve()
if status==pywraplp.Solver.OPTIMAL:
    print('문제 1')
    print('objective value = ',solver.Objective().Value())
    for i in range(4):
        print(x[i].name(),':',x[i].solution_value())
 
#문제1-1       
#NEW! SanDiego 한개의 공장을 세우기/ 창고 설립여부
present=[9,5,6,4,7,5]
required=[6,3,5,2,4,3]
from ortools.linear_solver import pywraplp
solver=pywraplp.Solver.CreateSolver('SAT')
#설립:1, 설립x:0
x={}
for i in  range(6):
    x[i]=solver.IntVar(0,1,'x[%i]'%i)

#어디에 공장을 세울 것인가(최소 한 지역 이상)
solver.Add(x[0]+x[1]+x[4]>=1)

#L에 공장 설립 시만 L에 창고 설립 가능
solver.Add(x[0]>=x[2])
#S
solver.Add(x[1]>=x[3])
#SanD
solver.Add(x[4]>=x[5])
#warehouse는 최대 한개 설립 가능
solver.Add(x[2]+x[3]+x[5]<=1)
#자원 10million
solver.Add(sum([x[i]*required[i] for i in range(6)])<=10)
#목적함수 이익 최대화
value=sum([x[i]*present[i] for i in range(6)])
solver.Maximize(value)

with open('과제3_문제1','w') as out_f:
    lp_text=solver.ExportModelAsLpFormat(False)
    out_f.write(lp_text)

status=solver.Solve()
if status==pywraplp.Solver.OPTIMAL:
    print('\n문제1-1')
    print('objective value = ',solver.Objective().Value())
    for i in range(6):
        print(x[i].name(),':',x[i].solution_value())

#문제2
print('\n문제2')
from ortools.linear_solver import pywraplp
solver=pywraplp.Solver.CreateSolver('SAT')
profit=[[0,0,0],
        [1,0,-1],
        [3,2,2],
        [3,3,4]]
#5개의 x[i,j]만 1, 나머지는 0
#i는 TV spot,j는 product
x={}
for  i in range(4):
    for j in range(3):
        x[i,j]=solver.IntVar(0,1,f'x[{i},{j}]')
#Number of TV spots: 0~3개까지 가능, 
for j in range(3):
    solver.Add(sum([x[i,j] for i in range(4)])==1)
#모든 광고 총 개수는 5개
spot=[0,1,2,3]
con=[]
for i in range(4):
    for j in range(3):
        a=x[i,j]*spot[i]
        con.append(a)
solver.Add(sum(con)<=5)

obj=solver.Objective()
for i in range(4):
    for j in range(3):
        obj.SetCoefficient(x[i,j],profit[i][j])
obj.SetMaximization()

with open ('과제3_문제2','w') as out_f:
    lp_text=solver.ExportModelAsLpFormat(False)
    out_f.write(lp_text)

status=solver.Solve()
if status==pywraplp.Solver.OPTIMAL:
    print('objective value = ',obj.Value())
    for i in range(4):
        for j in range(3):
            print(x[i,j].name(),':',x[i,j].solution_value())
            
#문제3
print('\n문제3')
require=[10,8,12,6,7,11]
supply=[18,24,27,22,31]
fixed=[7650,3500,3500,4100,2200]
cost=[[1675,400,685,1630,1160,2800],
       [1460,1940,970,100,495,1200],
       [1925,2400,1425,500,950,800],
       [380,1355,543,1045,665,2321],
       [922,1646,700,508,311,1797]
       ]
from ortools.linear_solver import pywraplp
solver=pywraplp.Solver.CreateSolver('SAT')
x={}
for i in range(5):
    for j in range(6):
        x[i,j]=solver.IntVar(0,solver.infinity(),f'x[{i},{j}]')
#월 공급량 제약조건
con_S=[]
for i in range(5):
    con_S.append(solver.Constraint(0,supply[i]))
    for j in range(6):
        con_S[i].SetCoefficient(x[i,j],1)
#월 수요 만족
con_R=[]
for j in range(6):
    con_R.append(solver.Constraint(require[j],solver.infinity()))
    for i in range(5):
        con_R[j].SetCoefficient(x[i,j],1)
#고정 비용 발생 여부
#y값이 1이면 발생, 0이면 발생x
cost_f=[]
y={}
M=1000000
for i in range(5):
    y[i]=solver.IntVar(0,1,'y[%i]'%i)
    a=y[i]*fixed[i]
    cost_f.append(a)
for i in range(5):
    solver.Add(sum([x[i,j] for j in range(6)])<=y[i]*M)
obj=[]
for i in range(5):
    for j in range(6):
        a=x[i,j]*cost[i][j]
        obj.append(a)
solver.Minimize(sum(obj)+sum(cost_f))

with open('과제3_문제3','w') as out_f:
    lp_text=solver.ExportModelAsLpFormat(False)
    out_f.write(lp_text)

status=solver.Solve()
if status==pywraplp.Solver.OPTIMAL:
    print('objective value =', solver.Objective().Value())
    for i in range(5):
        for j in range(6):
            print(x[i,j].name(),':',x[i,j].solution_value())
    for i in range(5):
        print(y[i].name(),':',y[i].solution_value())

    