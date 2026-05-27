# 문제 1. 정수 모형 (계속)

## Obj.      Maximize  Z = 9x[0]+5x[1]+7x[2]+6x[3]+4x[4]+5x[5]
## subject to          6x[0]+3x[1]+4x[2]+5x[3]+2x[4]+3x[5] <= 10
##                                          x[3]+x[4]+x[5] <= 2
##                     -x[0]              +x[3]            <= 0
##                            -x[1]              +x[4]     <= 0
##                                  -x[2]            +x[5] <= 0
##                     0 <= x[j] <= 1
##                     x[j] is integer,  for j=0,1,2,3,4,5
##                     x[j] is binary,   for j=0,1,2,3,4,5

from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('SCIP')

# 변수 선언 (이진 변수)
x = [solver.IntVar(0, 1, f'x[{i}]') for i in range(6)]

# 목적 함수
solver.Maximize(9*x[0] + 5*x[1] + 7*x[2] + 6*x[3] + 4*x[4] + 5*x[5])

# 제약 조건
solver.Add(6*x[0] + 3*x[1] + 4*x[2] + 5*x[3] + 2*x[4] + 3*x[5] <= 10)
solver.Add(x[3] + x[4] + x[5] <= 2)
solver.Add(-x[0] + x[3] <= 0)
solver.Add(-x[1] + x[4] <= 0)
solver.Add(-x[2] + x[5] <= 0)

# 풀이 및 출력
status = solver.Solve()
print('-----문제 1-----')
if status == pywraplp.Solver.OPTIMAL:
    print('Maximize Z =', solver.Objective().Value())
    for i in range(6):
        print(f'x[{i}] = {int(x[i].solution_value())}')
else:
    print('최적해를 찾을 수 없습니다.')

# 문제 2. 정수 모형

## Obj.      Maximize  Z = x00-x02+3x10+2x11+2x12+3x20+3x21+4x22
## subject to          x00+x01+x02+2x10+2x11+2x12+3x20+3x21+3x22 <= 5
##                0 <= x00        +x10         +x20        <= 1
##                0 <=     x01         +x11       +x21     <= 1
##                0 <=         x02         +x12       +x22 <= 1
##                     0 <= x[i][j] <= 1
##                     x[i][j] is integer,  for i=0,1,2 / j=0,1,2
##                     x[i][j] is binary,   for i=0,1,2 / j=0,1,2

from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('SAT')

# 1. 변수 선언 (0 또는 1)
x = {}
for i in range(3):
    for j in range(3):
        x[i, j] = solver.IntVar(0, 1, f'x{i}{j}')

# 2. 목적 함수
solver.Maximize(
    x[0,0] - x[0,2] + 
    3*x[1,0] + 2*x[1,1] + 2*x[1,2] + 
    3*x[2,0] + 3*x[2,1] + 4*x[2,2]
)

# 3. 제약 조건

# 총 광고 슬롯 5개 이하 제약
solver.Add(
    x[0,0] + x[0,1] + x[0,2] + 
    2*(x[1,0] + x[1,1] + x[1,2]) + 
    3*(x[2,0] + x[2,1] + x[2,2]) <= 5
)

# 각 제품당 최대 1개 옵션만 선택 (<= 1)
solver.Add(x[0,0] + x[1,0] + x[2,0] <= 1) # 제품 1
solver.Add(x[0,1] + x[1,1] + x[2,1] <= 1) # 제품 2
solver.Add(x[0,2] + x[1,2] + x[2,2] <= 1) # 제품 3

# 4. 풀이 및 결과 출력
status = solver.Solve()
print('-----문제 2-----')

if status == pywraplp.Solver.OPTIMAL:
    print('Maximize Z =', solver.Objective().Value())
    for i in range(3):
        for j in range(3):
            print(f'{x[i, j].name()} = {int(x[i, j].solution_value())}')
else:
    print('최적해를 찾을 수 없습니다.')\
    
# 문제 3. 용량제약 입지선정 문제

## Obj.         Minimize     W = 1675x00+400x01+685x02+1630x03+1160x04+2800x05
##                               +1460x10+1940x11+970x12+100x13+495x14+1200x15
##                               +1925x20+2400x21+1425x22+500x23+950x24+800x25
##                               +380x30+1355x31+543x32+1045x33+664x34+2321x35
##                               +922x40+1646x41+700x42+508x43+311x44+1797x45
##                               +7650