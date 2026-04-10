# -*- coding: utf-8 -*-
"""
Created on Tue Mar 11 11:17:35 2025

@author: paint
""" 
#예제1
from ortools.linear_solver import pywraplp

def LinearProgrammingExample():
    solver=pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        return
    x= solver.NumVar(0,solver.infinity(),'x')
    y= solver.NumVar(0,solver.infinity(),'y')
    #각 변수를 정수로 지정하려면 .IntVar 사용 가능
    
    #Q: 최대 이익을 내기 위해서는 각각 몇 개의 주스를 만들어야 할까?
    #A: 500x+400y의 최댓값. 새콤주스 x개, 달콤주스 y개
    #제약조건: 딸기와 키위의 개수 한정
    solver.Add(4*x+2*y<= 30)
    #키위 총 소비량: 4x+2y
    solver.Add(2*x+6*y<= 45)
    #딸기 총 소비량: 2x+6y
    
    solver.Maximize(500*x+400*y)
    #목표함수 최대화조건
    
    status=solver.Solve()
    #.Solve는 목표함수와 제약 조건을 기반으로 최적의 해를 반환함
    
    if status == pywraplp.Solver.OPTIMAL:
        """
        .Solve()가 반환할 수 있는 값의 예시로는
        pywraplp.Solver.OPTIMAL : 최적해
        pywraplp.Solver.FEASIBLE : 실행 가능한 해를 찾았지만 최적해인 지 보장할 수 없음
        pywraplp.Solver.INFEASIBLE: 제약 조건을 만족하는 값이 없음
        pywraplp.Solver.ABNORMAL : 솔버가 비정상적으로 종료됨
        pywraplp.Solver.NOT_SOLVED : 솔버가 해결하지 못함
        등이 있음
        """
        """
        print(f'총 이익 : {solver.Objective().Value():.1f}원')
        print(f'총 주스의 개수: {x.solution_value()+y.solution_value():.1f}잔')
        print(f'새콤 주스 : {x.solution_value() :.1f}잔')
        print(f'달콤 주스 : {y.solution_value():.1f}잔')
        #나올 수 있는 잔의 수를 정수로 표현하고 싶다면 1
        """
        print('OPTIMAL')
        print('목적함수값=%.1f'%(solver.Objective().Value()))
        print('x=%.1f'%(x.solution_value()))
        print('y=%.1f'%(y.solution_value()))
        
    else:
        print('The problem does not have an optimal solution.')

LinearProgrammingExample()

#예제2
#목적함수: 최소 비용
#식품 1~6 [x1,x2,x3,x4,x5,x6]
#가격 [350,300,500,340,270,400]
#총 비용: 350*x1+300*x2+500*x3+340*x4+270*x5+400*x6 >목적함수
#비타민A 함유량: 10*x1+20*x3+20*x4+10*x5+20*x6 -> 제약조건1
#비타민C 함유량: 10*x2+30*x3+10*x4+30*x5+20*x6 -> 제약조건2
from ortools.linear_solver import pywraplp

data={}
#제약조건 좌변값
data['contraints_coeffs']=[
    [10,0,20,20,10,20],
    [0,10,30,10,30,20]]
#제약조건 우변값
data['bounds']=[50,60]
data['obj_coeffs']=[350,300,500,340,270,400]
data['num_var']=6
data['num_con']=2

solver=pywraplp.Solver.CreateSolver('SCIP')
x={}
#x라는 변수 리스트 생성
for j in range(data['num_var']):
    x[j]=solver.IntVar(0,solver.infinity(),'x[%i]'%j)
    #변수 리스트에 변수 저장
for k in range(data['num_con']):
    #range 안에는 정수만 가능. 실수, 문자열 불가
    con=[data['contraints_coeffs'][k][l]*x[l] for l in range(data['num_var'])]
    solver.Add(sum(con)>=data['bounds'][k])
obj=[data['obj_coeffs'][l]*x[l] for l in range(data['num_var'])]
solver.Minimize(sum(obj))
status= solver.Solve()
if status==pywraplp.Solver.OPTIMAL:
    print(solver.Objective().Value())
    for j in range(data['num_var']):
        print(x[j].solution_value())
        
#예제3
"""
상품 종류: X1~X4
총 이익: 2*X1+3*X2+4*X3+5*X4 Maximize
땅콩 제약조건 15*X1+10*X2+6*X3+2*X4 <= 750*16 (1파운드*16=1온즈 **단위 잘 확인하기)
캐슈 제약조건: 1*X1+6*X2+10*X3+14*X4<=250*16
X1,X2,X3,X4 > 0
"""
from ortools.linear_solver import pywraplp
solver=pywraplp.Solver.CreateSolver('SCIP')
data={}
#data={} 코드 통해서 빈 리스트 만들기
data['constraint_coeff']=[[15,10,6,2],
                          [1,6,10,14]]
data['bounds']=[750*16,250*16]
data['obj_coeff']=[2,3,4,5]
data['n_var']= 4
data['n_con']= 2
#변수  x1~x4 생성
x={}
for i in range(data['n_var']):
    x[i]=solver.NumVar(0,solver.infinity(),'x[%i]'%i)
#제약조건 생성
for i in range(data['n_con']):
    con_f= [data['constraint_coeff'][i][j]*x[j] for j in range(data['n_var'])]
    solver.Add(sum(con_f)<=data['bounds'][i])

#목적함수 생성
obj_f= [data['obj_coeff'][i]*x[i] for i in range(data['n_var'])]
solver.Maximize(sum(obj_f))

status= solver.Solve()
if status == pywraplp.Solver.OPTIMAL:
    print(f'총 이익 : {solver.Objective().Value()}')
    for i in range(data['n_var']):
        print(f'{x[i]} : {x[i].solution_value()}')
        
        
#실습1:스티글러 식단
from ortools.linear_solver import pywraplp
from or2_4_data import *
solver=pywraplp.Solver.CreateSolver('SCIP')
#의사결정 변수 지정 #data의 첫번째 열(음식이름)
foods = [solver.NumVar(0.0,solver.infinity(),item[0]) for item in data]
print('Number of variables = ',solver.NumVariables())

constraints=[]
#enumerate 활용해 각 데이터 행에 인덱스 부여. 첫번째 변수에는 숫자가, 두번째 변수에는 데이터 열이 부여됨
#변수의 개수=nutrients의 행 개수
for i, nutrient in enumerate(nutrients):
    #최소값을 권장 섭취량으로, 최대를 무한대로 범위 설정. 이를 통해 제약조건 부등호 생성
    #.Constraint를 활용해 부등호와 우변을 생성(>= 우변값) solver.Add의 역할
    constraints.append(solver.Constraint(nutrient[1],solver.infinity()))
    for j, item in enumerate(data):
        #제약 조건의 우변값을 순서대로 불러온 후 좌변 식을 생성하는 과정
        #data 값의 세로열을 합하는 식 생성
        constraints[i].SetCoefficient(foods[j],item[i+3])
print('Number of constraints = ',solver.NumConstraints())

# 목적함수: 가격으로 정규화된 제품 개수의 합을 최소화
objective = solver.Objective()
for food in foods:
    objective.SetCoefficient(food, 1)

objective.SetMinimization()

status = solver.Solve()

# 해 출력: 각 음식별 구매량 출력
nutrients_result = [0] * len(nutrients)
print("\nAnnual Foods:")
for i, food in enumerate(foods):
    if food.solution_value() > 0.0:
        print("{}: ${}".format(data[i][0], 365.0 * food.solution_value()))
        for j, _ in enumerate(nutrients):
            nutrients_result[j] += data[i][j + 3] * food.solution_value()
print("\nOptimal annual price: ${:.4f}".format(365.0 * objective.Value()))

print("\nNutrients per day:")
for i, nutrient in enumerate(nutrients):
    print(
        "{}: {:.2f} (min {})".format(nutrient[0], nutrients_result[i], nutrient[1])
)