#과제2

#문제 1
from ortools.linear_solver import pywraplp
solver=pywraplp.Solver.CreateSolver('SCIP')
c_names=['c1','c2','c3']
p_names=['plant1','plant2','plant3']
a=[[2,3,5],
   [2.5,4,4.8],
   [3,3.6,3.2]]
needs=[500,700,600]
x={}
#i:company1,2,3 j:plant1,2,3
#의사결정 변수 x[i,j]: 수송량
for i in range(len(c_names)):
    for j in range(len(p_names)):
        x[i,j]=solver.NumVar(0,solver.infinity(), str(c_names[i])+'.'+str(p_names[j]))

#공급제약조건
#c3_con1=[x[2,j] for j in range(len(p_names))]
#solver.Add(sum(c3_con1)<=500)
#로 만들어줄 수 있지만 수송 제약 조건에 포함되는 조건이므로 주석처리함
#수송제약조건
c2_con=[x[1,j] for j in range(len(p_names))]
solver.Add(sum(c2_con)<=200)
c3_con=[x[2,j] for j in range(len(p_names))]
solver.Add(sum(c3_con)<=200)
#목재 수요 조건
con=[]
for i in range(len(p_names)):
    con.append(solver.Constraint(needs[i],solver.infinity()))
    for j in range(len(c_names)):
        con[i].SetCoefficient(x[j,i],1)
#목적함수
#비용 최소화
objective=solver.Objective()
for i in range(len(c_names)):
    for j in range(len(p_names)):
        objective.SetCoefficient(x[i,j],a[i][j])
objective.SetMinimization()

with open('과제2-1 조건','w') as out_f:
    lp_text=solver.ExportModelAsLpFormat(False)
    out_f.write(lp_text)

status=solver.Solve()
if status==pywraplp.Solver.OPTIMAL:
    print(f'Total cost : ${objective.Value():.1f}')
    for i in range(len(c_names)):
        for j in range(len(p_names)):
            print(f'{x[i,j].name()} : {x[i,j].solution_value()}t')
            
else:
    print('This problem does not have an optimal solution')

#과제2-2 
from ortools.linear_solver import pywraplp
solver=pywraplp.Solver.CreateSolver('SCIP')
#의사결정 변수
#x:에어커 별 저소득 주택 수, y=에어커 별 중간소득 주택 수
x={}
y={}
for i in range(10):
    x[i]=solver.IntVar(0,20,'저소득')
    y[i]=solver.IntVar(0,15,'중간소득')
#sum(x)를 하니까 리스트 0~9까지 더한 45의 값이 나옴. 딕셔너리의 키 값이 더해진다. 변수의 합으로 설정하는 방법?
#print(sum(x[i] for i in range(10)))일 때 변수의 합이 됨.
x_sum=sum(x[i] for i in range(10))
y_sum=sum(y[i] for i in range(10))
#solver.Add(60<=x_sum<=100) 으로 작성하면 x_sum<=100 만 조건으로 입력됨
solver.Add(60<=x_sum)
solver.Add(x_sum<=100)
solver.Add(30<=y_sum)
solver.Add(y_sum<=70)
solver.Add(x_sum+y_sum<=150)
x_cost=[]
y_cost=[]
for i in range(10):
    x_cost.append(13000*x[i])
    y_cost.append(18000*y[i])
solver.Add(sum(x_cost)+sum(y_cost)<=2000000)
solver.Add(50+y_sum*0.5<=x_sum)

#문제2-1. 비용 최소화
objective=solver.Objective()
solver.Minimize(solver.Sum(x_cost)+solver.Sum(y_cost))


with open ("과제2-2조건(1).lp", "w") as out_f:
    lp_text = solver.ExportModelAsLpFormat(False)
    out_f.write(lp_text)
    

status=solver.Solve()
if status==pywraplp.Solver.OPTIMAL:
    print('비용 최소화')
    print(f'Total cost = ${objective.Value():.1f}')
    print(f'Total houses = {x_sum.solution_value()+y_sum.solution_value():.0f}개')
    for i in range(10):
        print(f'acre{i}: {x[i].name()} {x[i].solution_value():.0f}개/{y[i].name()} {y[i].solution_value():.0f}개')
else:
    print('This problem does not have an optimal solution')
    
#문제2-2. 주택 최대화
solver.Maximize(x_sum+y_sum)
status1=solver.Solve()
with open ("과제2-2조건(2).lp", "w") as out_f:
    lp_text = solver.ExportModelAsLpFormat(False)
    out_f.write(lp_text)
if status1==pywraplp.Solver.OPTIMAL:
    print('\n가구 최대화')
    print(f'Total cost = ${13000*x_sum.solution_value()+18000*y_sum.solution_value()}')
    print(f'Total houses = {objective.Value():.0f}개')
    for i in range(10):
        print(f'acre{i}: {x[i].name()} {x[i].solution_value():.0f}개/{y[i].name()} {y[i].solution_value():.0f}개')
else:
    print('This problem does not have an optimal solution')
    
