#문제1

from ortools.linear_solver import pywraplp
solver=pywraplp.Solver.CreateSolver('SCIP')
#변수 12개
p_names=['Small','Medium','Large','ExLarge']
m_names=['A','B','C']
o_costs=[30,50,80]
demands=[10000,8000,6000,6000]
p_rates=[[300,600,800],
      [250,400,700],
      [200,350,600],
      [100,200,300]
      ]
infinity=solver.infinity()
x={}
#x[product,machine]
for i in range(len(p_names)):
    for j in range(len(m_names)):
        x[i,j]=solver.NumVar(0,infinity,'X'+str(i)+str(j))
        #'X'+str(i)+str(j) 처럼 문자열끼리의 합산을 만들 수 있다
#각 기계 주당 50시간 사용 가능 조건

#i=0(small),1(Medium),2(Large),3(ExLarge), j=0(A),1(B),3(C)
const_expr =[]     
for i in range(len(m_names)):
    const_expr=[x[j,i] for j in range(len(p_names))]
    solver.Add(sum(const_expr)<=50,p_names[i]+'_capa')
#생산요구량 조건
#Small 생산량 최소 demands
constraint=[]
for i in range(len(p_names)):
    constraint.append(solver.Constraint(demands[i],infinity))
    for j in range(len(m_names)):
        constraint[i].SetCoefficient(x[i,j],p_rates[i][j])
objective=solver.Objective()
for i in range(len(p_names)):
    for j in range(len(m_names)):
        objective.SetCoefficient(x[i,j],o_costs[j])
objective.SetMinimization()

#모델 파일 생성
with open('or3-1.lp','w') as out_f:
    lp_text=solver.ExportModelAsLpFormat(False)
    out_f.write(lp_text)

status=solver.Solve()
if status==pywraplp.Solver.OPTIMAL:
    print(solver.Objective().Value())
    for i in range(len(p_names)):
        for j in range(len(m_names)):
            print(p_names[i],'/',m_names[j],':',x[i,j].name(),'=%.1f'%x[i,j].solution_value())
            
#문제2
#i년 초
#year1:x[0]+y[0]+s[0]=2200
#year2:x[1]+y[1]+z+s[1]=s[0]+1.08*x[0]
#year3:x[2]+y[2]+s[2]=s[1]+1.08*x[1]+1.17*y[0]
#year4:x[3]+y[3]+s[3]=s[2]+1.08*x[2]+1.17*y[1]+1.27*z
#year5:x[4]+s[4]=s[3]+1.08*x[3]+1.17*y[2]
#목적함수: 1.08*x[4]+1.17*y[3]+s[4] 최대화
from ortools.linear_solver import pywraplp
solver=pywraplp.Solver.CreateSolver('SCIP')

x={}
s={}
infinity=solver.infinity()
for i in range(5):
    x[i]=solver.NumVar(0,infinity,'x[%i]'%i)
    s[i]=solver.NumVar(0,infinity,'s[%i]'%i)
y={}
for i in range(4):
    y[i]=solver.NumVar(0,infinity,'y[%i]'%i)
z=solver.NumVar(0,infinity,'z')

solver.Add(x[0]+y[0]+s[0]==2200,'year1')
solver.Add(x[1]+y[1]+z+s[1]==s[0]+1.08*x[0],'year2')
solver.Add(x[2]+y[2]+s[2]==s[1]+1.08*x[1]+1.17*y[0],'year3')
solver.Add(x[3]+y[3]+s[3]==s[2]+1.08*x[2]+1.17*y[1]+1.27*z,'year4')
solver.Add(x[4]+s[4]==s[3]+1.08*x[3]+1.17*y[2],'year5')


objective=solver.Objective()
solver.Maximize(1.08*x[4]+1.17*y[3]+s[4])
with open('or3-2.lp', "w") as out_f:
 lp_text = solver.ExportModelAsLpFormat(False)
 out_f.write(lp_text)

status=solver.Solve()
if status==pywraplp.Solver.OPTIMAL:
    print('Objective value=%.1f'%objective.Value())
    for i in range(5):
        print(x[i].name(),'=',x[i].solution_value())
    for i in range(4):
        print(y[i].name(),'=',y[i].solution_value())
    print(z.name(),'=',z.solution_value())
    for i in range(5):
        print(s[i].name(),'=',s[i].solution_value())
else:
    print('The problem does not have an optimal solution.')