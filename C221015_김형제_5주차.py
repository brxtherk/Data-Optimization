# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 11:34:09 2026

@author: redti
"""

# 예제 1

from ortools.linear_solver import pywraplp
solver = pywraplp.Solver.CreateSolver("SAT")

# X[i]: i 요일에 일을 시작하는 스태프의 수
# Minimize Obj: +1*x[0] +1*x[1] +1*x[2] +1*x[3] +1*x[4] +1*x[5] +1*x[6]

# Subject to
# MON: +1*x[0] + 1*x[3] + 1*x[4] + 1*x[5] + 1*x[6]  >= 20
# TUE: +1*x[0] + 1*x[1] + 1*x[4] + 1*x[5] + 1*x[6]  >= 16
# WED: +1*x[0] + 1*x[1] + 1*x[2] + 1*x[5] + 1*x[6]  >= 13
# THU: +1*x[0] + 1*x[1] + 1*x[2] + 1*x[3] + 1*x[6]  >= 16
# FRI: +1*x[0] + 1*x[1] + 1*x[2] + 1*x[3] + 1*x[4]  >= 19
# SAT: +1*x[1] + 1*x[2] + 1*x[3] + 1*x[4] + 1*x[5]  >= 14
# SUN: +1*x[2] + 1*x[3] + 1*x[4] + 1*x[5] + 1*x[6]  >= 12

REQ = [20,16,13,16,19,14,12]
names = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']
infinity = solver.infinity()

x = {}
for i in range(7):
    x[i] = solver.IntVar(0, infinity, "x[%i]" % i)
    
for i in range(7):
    constraint_expr = [x[(i-j) % 7] for j in range(5)]
    solver.Add(sum(constraint_expr) >= REQ[i], names[i])
    
objective = solver.Objective()
solver.Minimize(solver.Sum([x[i] for i in range(7)]))

# 모델 파일 생성

with open('or4-2.lp', "w") as out_f:
    lp_text = solver.ExportModelAsLpFormat(False)
    out_f.write(lp_text)

status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL:
    print("Objective value =", solver.Objective().Value())
    for i in range(7):
        print(x[i].name(), " = ", x[i].solution_value())
else:
    print("The problem does not have an optimal solution.")

# 예제 2

from ortools.linear_solver import pywraplp
solver = pywraplp.Solver.CreateSolver("SAT")

# Maximize
# Obj: +9 X01 +3 X02 +4 X03 +2 X04 +1 X05 +5 X06 +6 X07 +1 X12 +7 X13 +3 X14 +5 X15 +2 X16 +1 X17 +4 X23 +4 X24 +2 X25 +9 X26 +2 
# X27 +1 X34 +5 X35 +5 X36 +2 X37 +8 X45 +7 X46 +6 X47 +2 X56 +3 X57 +4 X67 
# Subject to
# consultant_0: +1 X01 +1 X02 +1 X03 +1 X04 +1 X05 +1 X06 +1 X07  = 1
# consultant_1: +1 X10 +1 X12 +1 X13 +1 X14 +1 X15 +1 X16 +1 X17  = 1
# consultant_2: +1 X20 +1 X21 +1 X23 +1 X24 +1 X25 +1 X26 +1 X27  = 1
# consultant_3: +1 X30 +1 X31 +1 X32 +1 X34 +1 X35 +1 X36 +1 X37  = 1
# consultant_4: +1 X40 +1 X41 +1 X42 +1 X43 +1 X45 +1 X46 +1 X47  = 1
# consultant_5: +1 X50 +1 X51 +1 X52 +1 X53 +1 X54 +1 X56 +1 X57  = 1
# consultant_6: +1 X60 +1 X61 +1 X62 +1 X63 +1 X64 +1 X65 +1 X67  = 1
# consultant_7: +1 X70 +1 X71 +1 X72 +1 X73 +1 X74 +1 X75 +1 X76  = 1
# x_0_1: +1 X01 -1 X10  = 0,  x_0_2: +1 X02 -1 X20  = 0,  x_0_3: +1 X03 -1 X30  = 0,  x_0_4: +1 X04 -1 X40  = 0,  x_0_5: +1 X05 -1 X50  = 0,  x_0_6: +1 X06 -1 X60  = 0,  
# x_0_7: +1 X07 -1 X70  = 0
# x_1_2: +1 X12 -1 X21  = 0,  x_1_3: +1 X13 -1 X31  = 0,  x_1_4: +1 X14 -1 X41  = 0,  x_1_5: +1 X15 -1 X51  = 0,  x_1_6: +1 X16 -1 X61  = 0,  x_1_7: +1 X17 -1 X71  = 0
# x_2_3: +1 X23 -1 X32  = 0,  x_2_4: +1 X24 -1 X42  = 0,  x_2_5: +1 X25 -1 X52  = 0,  x_2_6: +1 X26 -1 X62  = 0,  x_2_7: +1 X27 -1 X72  = 0
# x_3_4: +1 X34 -1 X43  = 0,  x_3_5: +1 X35 -1 X53  = 0,  x_3_6: +1 X36 -1 X63  = 0,  x_3_7: +1 X37 -1 X73  = 0
# x_4_5: +1 X45 -1 X54  = 0,  x_4_6: +1 X46 -1 X64  = 0,  x_4_7: +1 X47 -1 X74  = 0
# x_5_6: +1 X56 -1 X65  = 0,  x_5_7: +1 X57 -1 X75  = 0
# x_6_7: +1 X67 -1 X76  = 0

Ratings = [
[None,9,3,4,2,1,5,6],
[None,None,1,7,3,5,2,1],
[None,None,None,4,4,2,9,2],
[None,None,None,None,1,5,5,2],
[None,None,None,None,None,8,7,6],
[None,None,None,None,None,None,2,3],
[None,None,None,None,None,None,None,4]
]

nC = len(Ratings[0])

# 의사결정변수

X = {}
for i in range(nC):
    for j in range(nC):
        if i != j:
            X[i, j] = solver.IntVar(0, 1, "X"+str(i)+str(j))

# 제약조건

const_expr = []

# 컨설턴트당 1명만 배정

for i in range(nC):
    const_expr = [X[i,j] for j in range(nC) if i != j]
    solver.Add(sum(const_expr) == 1, 'consultant_' + str(i))
    
# xij = xji 제약

for i in range(nC):
    for j in range(nC):
        if i < j:
            solver.Add(X[i, j] == X[j, i], 'x_'+str(i)+'_'+str(j))

# 목적함수

obj_expr = []
for i in range(nC-1):
    for j in range(nC):
        if Ratings[i][j] != None:
            obj_expr.append(Ratings[i][j]*X[i, j])
            
solver.Maximize(solver.Sum(obj_expr))

# 모델파일생성

with open('or4-4.lp', "w") as out_f:
    lp_text = solver.ExportModelAsLpFormat(False)
    out_f.write(lp_text)
    
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL:
    print("Objective value = %.1f" % solver.Objective().Value())
    for i in range(nC):
        for j in range(nC):
            if i != j and X[i, j].solution_value() != 0:
                print('Consultant [%i]' %i, '--> Consultant [%i]' %j)
else:
    print("The problem does not have an optimal solution.")

# 예제 3

from ortools.linear_solver import pywraplp
solver = pywraplp.Solver.CreateSolver("SCIP")

# • 의사결정 변수 xj -> 1 (의사결정 j가 예이면)
#                xj -> 0 (의사결정 j가 아니오이면)
#                (j = 1, 2, 3, 4)
               
# • 목적함수
# Z = 투자의 현재 가치의 합
# Z = 9x1+5x2+6x3+4x4

# • 제약조건
# 6x1+3x2+5x3+2x4 ≤ 11
# x3+x4 ≤ 1
# x3 ≤ x1
# x4 ≤ x2
# xj is binary for j = 1, 2, 3, 4

nVars = 4
values = [9, 5, 6, 4]
reqs = [6, 3, 5, 2]

# 의사결정변수

x = {}
for i in range(nVars):
    x[i] = solver.IntVar(0, 1, "x[%i]" % i)

# 제약조건

solver.Add(sum([reqs[i]*x[i] for i in range(nVars)]) <= 11, 'const 0')
solver.Add(x[2] + x[3] <= 1, 'const 1')
solver.Add(x[2] <= x[0], 'const 2')
solver.Add(x[3] <= x[1], 'const 3')

# 목적함수

solver.Maximize(sum([values[i]*x[i] for i in range(nVars)]))

with open('or5-1.lp', "w") as out_f:
    lp_text = solver.ExportModelAsLpFormat(False)
    out_f.write(lp_text)
    
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL:
    print("OPTIMAL")
    print("목적함수값 = ", solver.Objective().Value())
    for i in range(nVars):
        print(x[i].name(), " = ", x[i].solution_value())
else:
    print("The problem does not have an optimal solution.")

# 예제 4

from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver("SCIP")
infinity = solver.infinity()
BIGM = 1000000

# (의사결정변수)
# • x0, x1는 장난감 1, 2의 생산량
# • y0는 0이면 공장1 제 약활성화, 1이면 제약2 활성화를 위한 이진변수
# • y1과 y2은 장난감1과 2의 고정비에 대한 이진변수

# (제약조건)
# • 𝑥0/50 + x1/40 <= 500 + M*y0      # 공장 0 생산 제약
# • x0/40 + x1/25 <= 700 + M*(1-y0)  # 공장 1 생산 제약
# • x0 <= BIGM*y1
# • x1 <- BIGM*y2

# (목적함수)
# Maximize 10𝑥0 + 15𝑥1 −50,000𝑦1 −80,000𝑦2

# 의사결정변수

x = {}
for i in range(2):
    x[i] = solver.IntVar(0, infinity, "x[%i]" % i)
    
y = {}

for i in range(3):
    y[i] = solver.IntVar(0, 1, "y[%i]" % i)
    
# 제약조건

solver.Add(x[0]/50 + x[1]/40 <= 500 + BIGM * y[0], 'const 0')
solver.Add(x[0]/40 + x[1]/25 <= 700 + BIGM * (1-y[0]), 'const 1')
solver.Add(x[0] <= BIGM * y[1], 'const 2')
solver.Add(x[1] <= BIGM * y[2], 'const 3')

# 목적함수

solver.Maximize(10 * x[0] + 15 * x[1] - 50000 * y[1] - 80000 * y[2])

with open('or5-1.lp', "w") as out_f:
    lp_text = solver.ExportModelAsLpFormat(False)
    out_f.write(lp_text)
    
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL:
    print("OPTIMAL")
    print("목적함수값 = ", solver.Objective().Value())
    for i in range(2):
        print(x[i].name(), " = ", x[i].solution_value())
    for i in range(3):
        print(y[i].name(), " = ", y[i].solution_value())
else:
    print("The problem does not have an optimal solution.")

# 실습 1 (스태프 결정 문제2)

from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver("SAT")

REQ = [2,2,2,2,2,2,8,8,8,8,4,4,3,3,3,3,6,6,5,5,5,5,3,3]

infinity = solver.infinity()

x = {}
for i in range(24):
    x[i] = solver.IntVar(0, infinity, "x[{}]".format(i))

const = []
for i in range(24):
    const = [x[(i-j) % 24] for j in range(9) if j != 4]
    solver.Add(sum(const) >= REQ[i])
    
objective = solver.Objective()
solver.Minimize(solver.Sum([x[i] for i in range(24)]))

with open("5주차실습1.lp", "w") as out_f:
    lp_text = solver.ExportModelAsLpFormat(False)
    out_f.write(lp_text)

status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL:
    print("Objective value = {}".format(solver.Objective().Value()))
    for i in range(24):
        print("{} = {}".format(x[i].name(), x[i].solution_value()))
else:
    print("The problem does not have an optimal solution.")

# 실습 2 (컨설턴스 배정 최적화)

from ortools.linear_solver import pywraplp
solver = pywraplp.Solver.CreateSolver('SCIP')

# 1. 비용 데이터
Costs = [
    [15, 18, 21, 12, 25, 19, 14, 22], # 컨설턴트 1
    [20, 14, 17, 23, 16, 21, 18, 13], # 컨설턴트 2
    [11, 22, 19, 16, 20, 15, 23, 17], # 컨설턴트 3
    [24, 16, 13, 20, 18, 22, 11, 19], # 컨설턴트 4
    [17, 20, 22, 14, 13, 17, 20, 16], # 컨설턴트 5
    [19, 13, 16, 21, 22, 14, 17, 20], # 컨설턴트 6
    [22, 17, 20, 18, 15, 20, 16, 21]  # 컨설턴트 7
]

nC = len(Costs)       # 컨설턴트 수 (7)
nP = len(Costs[0])    # 프로젝트 수 (8)

# 2. 의사결정변수 설정
X = {}
for i in range(nC):
    for j in range(nP):
        # x_ij: 컨설턴트 i가 프로젝트 j에 배정되면 1, 아니면 0
        X[i, j] = solver.IntVar(0, 1, "X_" + str(i) + "_" + str(j))

# 3. 제약조건 설정

# (1) 각 컨설턴트는 정확히 1개의 프로젝트에 배정 (= 1)
for i in range(nC):
    const_expr = [X[i, j] for j in range(nP)]
    solver.Add(sum(const_expr) == 1, 'consultant_' + str(i))

# (2) 각 프로젝트는 최대 1명의 컨설턴트가 담당 (<= 1)
for j in range(nP):
    const_expr = [X[i, j] for i in range(nC)]
    solver.Add(sum(const_expr) <= 1, 'project_' + str(j))

obj_expr = []
for i in range(nC):
    for j in range(nP):
        obj_expr.append(Costs[i][j] * X[i, j])

solver.Minimize(solver.Sum(obj_expr))

with open('5주차실습2.lp', "w") as out_f:
    lp_text = solver.ExportModelAsLpFormat(False)
    out_f.write(lp_text)

status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL:
    print("목적함수 값 : %.1f" % solver.Objective().Value())
    
    for i in range(nC):
        for j in range(nP):
            if X[i, j].solution_value() != 0:
                print('Consultant [%i]' % i, '--> Project [%i]' % j)
else:
    print("The problem does not have an optimal solution.")


# 실습 3 (생산계획 문제 1)

from ortools.linear_solver import pywraplp
solver=pywraplp.Solver.CreateSolver('SAT')

#고객 1,2,3 의 주문량=변수
x={}
limit=[3,2,5]
for i in range(3):
    x[i]=solver.IntVar(0,limit[i],'x[%i]'%i)
    
# 고객 1,2,3 요청 수락(y=1) or 거절(y=0)

M=1000000
y={}

for i in range(3):
    y[i]=solver.IntVar(0,1,'y[%i]'%i)
    solver.Add(x[i]<=M*y[i])
    
#가용한 생산용량 제약조건
solver.Add(0.2*x[0]+0.4*x[1]+0.2*x[2]<=1)
solver.Maximize(2*x[0]+3*x[1]+0.8*x[2]-3*y[0]-2*y[1])
 
with open('5주차실습3','w') as out_f:
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
    
# 실습 4 (생산계획 문제 2)

from ortools.linear_solver import pywraplp
solver=pywraplp.Solver.CreateSolver('SAT')

# 의사결정 변수: 제품 1,2,3,4의 생산 수준
x={}

for i in range(4):
    x[i]=solver.IntVar(0,solver.infinity(),'x[%i]'%i)
    
# 각 제품을 생산 여부 결정 y=0(생산x),y=1(생산0)
M=1000000
y={}

for i in range(4):
    y[i]=solver.IntVar(0,1,'y[%i]'%i)
    solver.Add(x[i]<=y[i]*M)
    
# 2개의 신제품만 출시한다는 제약조건
solver.Add(y[0]+y[1]+y[2]+y[3]<=2)

# 제품 1 또는 2가 생산되어야 제품 3또는 4가 생산될 수 있음
# M을 곱하지 않으면 제품 1,2 중 하나만 생산 될 때 3또는 4 중 하나만 생산될 수 있다.
solver.Add(M*(y[0]+y[1])>=y[2]+y[3])
#제품 생산을 위한 공통재료 6000
#제품별 사용량 케이스는 두가지 중 하나
#z=0일 때 1번 제약식, z=1일 때 2번 제약식 활성화 
z=solver.IntVar(0,1,'z')
solver.Add(5*x[0]+3*x[1]+6*x[2]+4*x[3]<=6000+M*z)
solver.Add(4*x[0]+6*x[1]+3*x[2]+5*x[3]<=6000+M*(1-z))

solver.Maximize(70*x[0]+60*x[1]+90*x[2]+80*x[3]-50000*y[0]-40000*y[1]-70000*y[2]-60000*y[3])

with open('5주차실습4','w') as out_f:
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
    
# 실습 5 (할당문제)

time=[[5,12,30,20,12],
      [20,4,15,10,25],
      [15,20,6,15,12],
      [25,15,15,4,10],
      [10,25,15,12,5]]
count=[2,1,3,1,3]

from ortools.linear_solver import pywraplp
solver=pywraplp.Solver.CreateSolver('SAT')

# 의사결정 변수: 구역에 할당 이진변수
# i=구역 번호,  j= 대응할 구역 , j=0(담당x),j=1(담당)
x={}

for i in range(5):
    for j in range(5):
        x[i,j]=solver.IntVar(0,1,f'x[0{i},{j}]')
        
# 두개의 소방서를 배치
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