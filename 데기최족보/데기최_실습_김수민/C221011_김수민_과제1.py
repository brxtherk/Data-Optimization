#문제1
print('문제1')
#사우디산 원유 1배럴 > 0.3 가솔린 + 0.4 제트유 + 0.2 윤활유
#베네수엘라 원유 1 배럴 > 0.4 가솔린 +0.2 제트유 + 0.3 윤활유
#제약조건1: 사우디산 하루 최대 9000 배럴
#제약조건2: 베네수엘라 하루 최대 6000 배럴
#제약조건3: 2000가솔린 이상
#제약조건4: 1500 제트유 이상
#제약조건5: 500 윤활류 이상
#목적함수 60*사우디산+55*베네수엘라 의 최소화
#x=사우디산, y=베네수엘라산
from ortools.linear_solver import pywraplp
solver= pywraplp.Solver.CreateSolver('SCIP')

#의사결정 변수
x= solver.NumVar(0,9000,'사우디산 원유')
#x 범위 제약조건 설정
y= solver.NumVar(0,6000,'베네수엘라산 원유')
#y 범위 제약조건 설정

#제약조건
#가솔린
solver.Add(0.3*x+0.4*y>=2000)
#제트유
solver.Add(0.4*x+0.2*y>=1500)
#윤활류
solver.Add(0.2*x+0.3*y>=500)

#목적함수
solver.Minimize(60*x+55*y)

#해 출력
status=solver.Solve()
if status==pywraplp.Solver.OPTIMAL:
    print('Total cost : ${:.1f}'.format(solver.Objective().Value()))
    print('{} : {:.1f}배럴'.format(x.name(),x.solution_value()))
    print('{} : {:.1f}배럴'.format(y.name(),y.solution_value()))
else:
    print('The problem does not have an optimal solution.')
    
    
#문제 2
print('\n문제2')
#원석1 1톤> 0.2가돌리늄+0.15홀룸+0.2톨륨
#원석2 1톤> 0.3가돌리늄+0.25홀륨+0.1톨륨
#제약조건1: 가돌리늄 8톤 이상
#제약조건2: 홀륨 6톤 이상
#제약조건3: 툴륨 4톤 이상
#목적함수: 10*원석1+15*원석2 최소화
from ortools.linear_solver import pywraplp
solver=pywraplp.Solver.CreateSolver('SCIP')
#의사결정 변수 생성
x=solver.NumVar(0,solver.infinity(),'원석 1')
y=solver.NumVar(0,solver.infinity(), '원석 2')
#제약조건
#1톤의 0.nn%이므로 단위 변환 시 0.00nn으로 변경해주어야 함
#가돌리늄
solver.Add(0.002*x+0.003*y>=8)
#홀룸
solver.Add(0.0015*x+0.0025*y>=6)
#툴륨
solver.Add(0.002*x+0.001*y>=4)
#목적함수
solver.Minimize(10*x+15*y)

status=solver.Solve()
if status==pywraplp.Solver.OPTIMAL:
    print('Total cost : $%.1f'%solver.Objective().Value())
    print('{} :{:.1f}톤'.format(x.name(),x.solution_value()))
    print('{} :{:.1f}톤'.format(y.name(),y.solution_value()))
    
#문제3
print('\n문제3')
#첫번째 풀이
#의사결정 변수를 세개만 설정한 풀이
from ortools.linear_solver import pywraplp
solver=pywraplp.Solver.CreateSolver('SCIP')
print('(1) 생산 품목의 양만 변수로 잡은 풀이')
#팔 수 있는 물건: 유모차, 보행기, 자전거
#기계 1,3 대여 가능
x1=solver.IntVar(0,solver.infinity(),'유모차')
x2=solver.IntVar(0,solver.infinity(),'보행기')
x3=solver.IntVar(0,solver.infinity(),'자전거')
#유모차 1대 : [8,4,4]
#보행기 1대 : [3,4,0]
#자전거 1대 : [3,0,2]
#대여 가능한 시간 [240-8*x1-3*x2-2*x3,0,100-4*x1-2*x3]
#목적함수: 30*x1+20*x2+16*x3+3.5*(240-8*x1-3*x2-2*x3)+3*(100-4*x1-2*x3) 최대화
solver.Add(8*x1+3*x2+3*x3<=240)
solver.Add(4*x1+4*x2<=200)
solver.Add(4*x1+2*x3<=100)
solver.Maximize(30*x1+20*x2+16*x3+3.5*(240-8*x1-3*x2-2*x3)+3*(100-4*x1-2*x3))

status=solver.Solve()
Y0=solver.Objective().Value()

if status==pywraplp.Solver.OPTIMAL:
    print(x1.name(),':', x1.solution_value(),'대')
    print(x2.name(),':', x2.solution_value(),'대')
    print(x3.name(), ':', x3.solution_value(),'대')
    print('총 수익 :',solver.Objective().Value(),'만원')

#두번째 풀이    
#의사결정 변수를 5개로 설정한 풀이
#대여시간을 직접 설정하는 방식vs변수로 설정하는 방식에 따라 결과값이 다르게 나옴
from ortools.linear_solver import pywraplp
solver=pywraplp.Solver.CreateSolver('SCIP')
print('\n(2) 기계1,3의 대여 시간도 변수로 설정한 풀이')
#팔 수 있는 물건: 유모차, 보행기, 자전거
#기계 1,3 대여 가능
x1=solver.IntVar(0,solver.infinity(),'유모차')
x2=solver.IntVar(0,solver.infinity(),'보행기')
x3=solver.IntVar(0,solver.infinity(),'자전거')
y1=solver.NumVar(0,240,'기계1 대여')
y2=solver.NumVar(0,100,'기계3 대여')

solver.Add(8*x1+3*x2+3*x3+y1<=240)
solver.Add(4*x1+4*x2<=200)
solver.Add(4*x1+2*x3+y2<=100)
solver.Maximize(30*x1+20*x2+16*x3+3.5*y1+3*y2)

status=solver.Solve()
Y1=solver.Objective().Value()

if status==pywraplp.Solver.OPTIMAL:
    print(f'{x1.name()}: {x1.solution_value():.1f}대')
    print(f'{x2.name()}: {x2.solution_value():.1f}대')
    print(f'{x3.name()}: {x3.solution_value():.1f}대')
    print(f'{y1.name()}: {y1.solution_value():.1f}시간')
    print(f'{y2.name()}: {y2.solution_value():.1f}시간')
    print('총 수익 : %.1f만원'%(solver.Objective().Value()))

if Y0 > Y1:
    print('\n첫번째 풀이가 더 최적화된 해를 찾았다.')
elif Y0 == Y1:
    print('\n두 풀이 방식이 같은 최적해를 찾았다.')
else:
    print('\n두번째 풀이가 더 최적화된 해를 찾았다.')
    
#두 풀이가 답이 다르게 나오는 이유는??
#소수점의 연산 차이 때문에 같은 문제여도 Solver가 다른 근사해를 찾을 수 있음.

#세번째 풀이
#for  문을 사용한 방식
print('\n(3) for문을 이용한 풀이')
from ortools.linear_solver import pywraplp
solver=pywraplp.Solver.CreateSolver('SCIP')
con_coeffs=[[8,3,3,1,0],
            [4,4,0,0,0],
            [4,0,2,0,1]]
con_2=[240,200,100]
obj_coeffs=[30,20,16,3.5,3]
X=['유모차(대)','보행기(대)','자전거(대)','기계1(시간)','기계3(시간)']
x={}
for i in range (0,5):
    x[i]=solver.NumVar(0,solver.infinity(),'x%.0f'%i)
for j in range(0,3):
    constraint=[con_coeffs[j][i]*x[i] for i in range (0,5)]
    solver.Add(sum(constraint)<= con_2[j])
obj=[obj_coeffs[i]*x[i] for i in range(0,5)]
solver.Maximize(sum(obj))

status=solver.Solve()
if status==pywraplp.Solver.OPTIMAL:
    for i in range(0,5):
        print(f'{X[i]} : {x[i].solution_value():.1f}')
print(f'총 수익(만원): {solver.Objective().Value():.1f}')

