#예제1
#BIP, 변수들이 0 또는 1 값만 갖음
from ortools.linear_solver import pywraplp
solver=pywraplp.Solver.CreateSolver('SAT')

invest=[60,30,50,20]
Pvalue=[90,50,60,40]
#x[0,1]>공장, x[2,3]>창고
x={}
for i in range (4):
    x[i]=solver.IntVar(0,1,'x[%i]'%i)
#solver.Add(x[0]+x[1]>=1)
#if x[0]==1 and x[1]==0:
#    solver.Add(x[2]==1)
#if x[1]==1 and x[0]==0:
#    solver.Add(x[3]==1)
#if x[0] and x[1]==1:
#    solver.Add(x[2]+x[3]==1)

#위의 세가지 제약 조건을 더 간단하게 작성하는 법
#창고를 짓는 변수 두개의 합이 1과 같거나 작다
solver.Add(x[2]+x[3]<=1)
#공장과 창고의 인과관계 표현
solver.Add(x[2]<=x[0])
solver.Add(x[3]<=x[1])

#con=[]
#for i in range(4):
#    con.append(x[i]*invest[i])
#solver.Add(sum(con)<=110)
#위의 조건을 한 줄로 쓰는 법
solver.Add(sum([x[i]*invest[i] for i in range(4)])<=110)

#obj=[]
#for i in range(4):
#    obj.append(x[i]*Pvalue[i])
#solver.Maximize(sum(obj))
#위의 목적함수 한 줄로 작성하는 법
solver.Maximize(sum([x[i]*Pvalue[i] for i in range(4)]))

#제약 조건 및 목적함수 확인 위해 파일 생성
with open ('5주차 예제 1','w') as out_f:
    lp_text=solver.ExportModelAsLpFormat(False)
    out_f.write(lp_text)
    
status=solver.Solve()
if status==pywraplp.Solver.OPTIMAL:
    print('목적함수 값 = ', solver.Objective().Value(),'억원')
    for i in range(4):
        print(x[i].name(), ':', x[i].solution_value())
        
else:
    print('The problem does not have an optimal solution.')
    
#예제2
#고정비용 50000,80000
#profit 10,15
#공장 1이나 2 하나만 가동
#공장 1 가동 시 시간당 장난감1 50, 장난감2 40
#공장2 가동 시 시간 당 장남감1 40, 장난감2 25

#장난감1 생산량 x[0,0],x[0,1] 가동시간: x00/50,x01/40
#공장 2  생산량 x[1,0],x[1,1] 가동시간: x10/40,x11/25

from ortools.linear_solver import pywraplp
solver=pywraplp.Solver.CreateSolver('SAT')
#x[0,n]이랑 x[1,n] 중 하나만 어짜피 활성화 되므로 변수를 네개가 아닌 두개만 만들어서 코드를 짜도 된다 
x={}
for i in range (2):
    for j in range(2):
        x[i,j]=solver.IntVar(0,solver.infinity(),f'x[{i},{j}]')

#공장 1 생산량
z=solver.IntVar(0,1,'z')
M=1000000
#가동시간 제약
#z가 0이면 공장 1 제약조건 활성화, z=1이면 공장 2 제약 조건 활성화
solver.Add(x[0,0]/50+x[0,1]/40<=500+M*z)
solver.Add(x[1,0]/40+x[1,1]/25<=700+M*(1-z))
#z값에 따라 x[0,n] or x[1,n]을 0으로 설정함
#z가 0이면 공장 1 제약조건 활성화 z가 1이면 공장2 제약조건 활성화
solver.Add(x[0,0]+x[0,1]<=M*(1-z))
solver.Add(x[1,0]+x[1,1]<=M*z)
#셋업비용
y={}
for i in range(2):
    y[i]=solver.IntVar(0,1,'y[%i]'%i)
#장난감1 생산량이 0이면 y0=0
solver.Add(x[0,0]+x[1,0]<=M*y[0])
#장난감2 생산량이 0이면 y1=0
solver.Add(x[0,1]+x[1,1]<=M*y[1])
solver.Maximize(10*(x[0,0]+x[1,0])+15*(x[0,1]+x[1,1])-50000*y[0]-80000*y[1])

with open('5주차 예제2(2)','w') as out_f:
    lp_text=solver.ExportModelAsLpFormat(False)
    out_f.write(lp_text)

status=solver.Solve()

if status==pywraplp.Solver.OPTIMAL:
    print('목적함수 : ', solver.Objective().Value())
    for i in range(2):
        for j in range(2):
            print(x[i,j].name(),':',x[i,j].solution_value())
    for i in range(2):
        print(y[i].name(),':',y[i].solution_value())
    print(z.name(),':', z.solution_value())
else:
    print('The problem does not have an optimal solution.')

#실습1
from ortools.linear_solver import pywraplp
solver=pywraplp.Solver.CreateSolver('SAT')

#고객 1,2,3 의 주문량=변수
x={}
limit=[3,2,5]
for i in range(3):
    x[i]=solver.IntVar(0,limit[i],'x[%i]'%i)
#고객 1,2,3 요청 수락(y=1) or 거절(y=0)
#y값이 0또는 1로 먼저 결정되면 x값을 제한할 수 있음
M=1000000
y={}
for i in range(3):
    y[i]=solver.IntVar(0,1,'y[%i]'%i)
    solver.Add(x[i]<=M*y[i])
    #solver.Add(x[i]<=limit[i]*y[i])처럼 큰 수를 설정하지 않아도 변수의 범위보다만 넓으면 제약조건 설정 가능하다
#가용한 생산용량 제약조건
solver.Add(0.2*x[0]+0.4*x[1]+0.2*x[2]<=1)
solver.Maximize(2*x[0]+3*x[1]+0.8*x[2]-3*y[0]-2*y[1])
 
with open('5주차실습1','w') as out_f:
    lp_text=solver.ExportModelAsLpFormat(False)
    out_f.write(lp_text)
status=solver.Solve()
if status==pywraplp.Solver.OPTIMAL:
    print('목적함수 값: ',solver.Objective().Value())
    for i in range(3):
        print(x[i].name(),':',x[i].solution_value())
    for i in range(3):
        print(y[i].name(),':',y[i].solution_value())
else:
    print('The problem does not have an optimal solution.')
    
#실습2
from ortools.linear_solver import pywraplp
solver=pywraplp.Solver.CreateSolver('SAT')
#의사결정 변수: 제품 1,2,3,4의 생산 수준
x={}
for i in range(4):
    x[i]=solver.IntVar(0,solver.infinity(),'x[%i]'%i)
#각 제품을 생산 여부 결정 y=0(생산x),y=1(생산0)
M=1000000
y={}
for i in range(4):
    y[i]=solver.IntVar(0,1,'y[%i]'%i)
    solver.Add(x[i]<=y[i]*M)
#2개의 신제품만 출시한다는 제약조건
solver.Add(y[0]+y[1]+y[2]+y[3]<=2)
#제품 1 또는 2가 생산되어야 제품 3또는 4가 생산될 수 있다
#M을 곱하지 않으면 제품 1,2 중 하나만 생산 될 때 3또는 4 중 하나만 생산될 수 있다.
solver.Add(M*(y[0]+y[1])>=y[2]+y[3])
#제품 생산을 위한 공통재료 6000
#제품별 사용량 케이스는 두가지 중 하나
#z=0일 때 1번 제약식, z=1일 때 2번 제약식 활성화 
z=solver.IntVar(0,1,'z')
solver.Add(5*x[0]+3*x[1]+6*x[2]+4*x[3]<=6000+M*z)
solver.Add(4*x[0]+6*x[1]+3*x[2]+5*x[3]<=6000+M*(1-z))

solver.Maximize(70*x[0]+60*x[1]+90*x[2]+80*x[3]-50000*y[0]-40000*y[1]-70000*y[2]-60000*y[3])

with open('5주차실습2','w') as out_f:
    lp_text=solver.ExportModelAsLpFormat(False)
    out_f.write(lp_text)

status=solver.Solve()

if status==pywraplp.Solver.OPTIMAL:
    print('목적함수 : ', solver.Objective().Value())
    for i in range(4):
            print(x[i].name(),':',x[i].solution_value())
    for i in range(4):
        print(y[i].name(),':',y[i].solution_value())
    print(z.name(),':', z.solution_value())
else:
    print('The problem does not have an optimal solution.')
    
#실습3
time=[[5,12,30,20,12],
      [20,4,15,10,25],
      [15,20,6,15,12],
      [25,15,15,4,10],
      [10,25,15,12,5]]
count=[2,1,3,1,3]

from ortools.linear_solver import pywraplp
solver=pywraplp.Solver.CreateSolver('SAT')
#의사결정 변수: 구역에 할당 이진변수
#i=구역 번호,  j= 대응할 구역 , j=0(담당x),j=1(담당)
x={}
for i in range(5):
    for j in range(5):
        x[i,j]=solver.IntVar(0,1,f'x[0{i},{j}]')
#두개의 소방서를 배치
M=100000
y={}
for i in range(5):
    y[i]=solver.IntVar(0,1,'y[%i]'%i)
    solver.Add(sum([x[i,j] for j in range(5)])<=M*y[i])
solver.Add(sum([y[i] for i in range(5)])==2)
#z는 열로 봤을 때 배정이 되었는지 아닌지
#x[i,(0,1,2,3,4,)]가 1개여야 함
for i in range(5):
    solver.Add(sum([x[j,i] for j in range(5)])==1)

obj=solver.Objective()
for i in range(5):
    for j in range(5):
        #시간*횟수
        obj.SetCoefficient(x[i,j],time[i][j]*count[j])       
obj.SetMinimization()
status=solver.Solve()
if status==pywraplp.Solver.OPTIMAL:
    print(obj.Value())
    for i in range(5):
        for j in range(2):
            print(x[i,j].name(),':',x[i,j].solution_value())
else:
    print('The problem does not have an optimal solution.')