#실습1
#할당 문제
#열당 하나, 행당 하나, 이진변수 20개 생성
cost=[[90,80,75,70],
      [35,85,55,65],
      [125,95,90,95],
      [45,110,95,115],
      [50,100,90,100]]
from ortools.linear_solver import pywraplp
solver=pywraplp.Solver.CreateSolver('SAT')

x={}
for i in range(5):
    for j in range(4):
        x[i,j]=solver.IntVar(0,1,f'x[{i},{j}]')
for i in range(5):
    solver.Add(sum([x[i,j] for j in range(4)])<=1)
for j in range(4):
    solver.Add(sum([x[i,j] for i in range(5)])==1)
obj=solver.Objective()
for i in range(5):
    for j in range(4):
        obj.SetCoefficient(x[i,j],cost[i][j])
obj.SetMinimization()

status=solver.Solve()
if status==pywraplp.Solver.OPTIMAL:
    print('objective value = ',obj.Value())
    for i in range(5):
        for j in range(4):
            if x[i,j].solution_value()==1:
                print(x[i,j].name(),':',x[i,j].solution_value())
else:
    print('a')

#실습2
cost=[[90,76,75,70],
      [35,85,55,65],
      [125,95,90,105],
      [45,110,95,115],
      [60,105,80,75],
      [45,65,110,95]
      ]
from ortools.linear_solver import pywraplp
solver=pywraplp.Solver.CreateSolver('SAT')
#의사결정 1차 변수 설정
team1=[]
team2=[]
x={}
for i in range(6):
    for j in range(4):
        x[i,j]=solver.IntVar(0,1,f'x[{i},{j}]')
        if i%2==0:
            team1.append(x[i,j])
        else:
            team2.append(x[i,j])
#모든 작업자가 하나 이하의 일을 한다는 조건은 어디서 나온거지?
for i in range(6):
    solver.Add(sum([x[i,j] for j in range(4)])<=1)
for j in range(4):
    solver.Add(sum([x[i,j] for i in range(6)])==1)
solver.Add(sum(team1)<=2)
solver.Add(sum(team2)<=2)

obj=solver.Objective()
for i in range(6):
    for j in range(4):
        obj.SetCoefficient(x[i,j],cost[i][j])
obj.SetMinimization()
status=solver.Solve()
if status==pywraplp.Solver.OPTIMAL:
    print(obj.Value())
    
#실습3
#+작업자별 최대 작업 시간은 15시간
costs = [
    [90, 76, 75, 70, 50, 74, 12, 68],
    [35, 85, 55, 65, 48, 101, 70, 83],
    [125, 95, 90, 105, 59, 120, 36, 73],
    [45, 110, 95, 115, 104, 83, 37, 71],
    [60, 105, 80, 75, 59, 62, 93, 88],
    [45, 65, 110, 95, 47, 31, 81, 34],
    [38, 51, 107, 41, 69, 99, 115, 48],
    [47, 85, 57, 71, 92, 77, 109, 36],
    [39, 63, 97, 49, 118, 56, 92, 61],
    [47, 101, 71, 60, 88, 109, 52, 90],
    ]
size=[10,7,3,12,15,4,11,5]
from ortools.linear_solver import pywraplp
solver=pywraplp.Solver.CreateSolver('SAT')

x={}
for i in range(10):
    for j in range(8):
        x[i,j]=solver.IntVar(0,1,f'x[{i},{j}]')
#작업자 최대 작업 시간 15
#작업 크기란? 작업 하는 데 들어가는 량
for i in range(10):
    solver.Add(sum([x[i,j]*size[j] for j in range(8)])<=15)
#모든 작업은 수행되어야 한다
for j in range(8):
    solver.Add(sum([x[i,j] for i in range(10)])==1)
obj=solver.Objective()
for i in range(10):
    for j in range(8):
        obj.SetCoefficient(x[i,j],costs[i][j])
obj.SetMinimization()
status=solver.Solve()
if status==pywraplp.Solver.OPTIMAL:
    print(obj.Value())
#실습4
from ortools.linear_solver import pywraplp
solver = pywraplp.Solver.CreateSolver("SCIP")
costs = [50, 40, 60, 47.5, 55, 30, 57.5, 57.2]
sa = [
 [1, 0, 0, 1, 0, 0],
 [0, 1, 1, 0, 0, 0],
 [0, 1, 0, 0, 0, 1],
 [1, 0, 0, 0, 0, 1],
 [0, 0, 0, 1, 0, 1],
 [0, 0, 1, 0, 0, 0],
 [0, 1, 1, 0, 1, 0],
 [1, 0, 0, 0, 1, 0]
 ]

x={}
for i in range(8):
    for j in range(6):
        x[i,j]=solver.IntVar(0,1,f'x[{i},{j}')
for j in range(6):
    solver.Add(sum([x[i,j]*sa[i][j] for i in range(8)])>=1)
y={}
M=1000000
for i in range(8):
    y[i]=solver.IntVar(0,1,'y[%i]')
    solver.Add(sum([x[i,j] for j in range(6)])<=y[i]*M)
solver.Minimize(sum([y[i]*costs[i] for i in range(8)]))
status=solver.Solve()
if status==pywraplp.Solver.OPTIMAL:
    print(solver.Objective().Value())
#실습5
patterns = [
 [3, 0, 0],
 [1, 1, 0],
 [0, 2, 0],
 [1, 0, 1]
 ]
demands = [400, 120, 80]
from ortools.linear_solver import pywraplp
solver = pywraplp.Solver.CreateSolver("SCIP")

x={}
for i in range(4):
    x[i]=solver.IntVar(0,solver.infinity(),'x[%i]')
for j in range(3):
    solver.Add(sum([patterns[i][j]*x[i] for i in range(4)])>=demands[j])
solver.Minimize(sum([x[i] for i in range(4)])*500)
status=solver.Solve()
if status==pywraplp.Solver.OPTIMAL:
    print(solver.Objective().Value())
#실습6
limits = [ [3500, 3655], [3520, 3905], [3600, 3658], [3650, 4075], [3660, 3915],
 [3900, 4449], [3910, 4095], [3950, 4160], [3995, 4065], [4000, 4195],
 [4000, 4200], [4210, 4405], [4320, 4451], [4350, 4500], [4420, 5400],
 [4450, 4800], [4450, 4570], [5200, 6000], [5600, 6200], [6010, 6400],
 [6015, 6250] ]
costs = [4, 3, 1, 4, 1, 6, 2, 3, 1, 2, 
2, 2, 2, 2, 9, 3, 1, 9, 8, 8, 
2]
names = ['PBD', 'PPO', 'PPF', 'PBO', 'PPD', 'POPOP', 'A-NPO', 'NASAL', 'AMINOB', 'BBO', 'D-STILB', 
'D-POPOP', 'A-NOPON', 'D-ANTH',  '4-METHYL-V', '7-D-4-M', 'ESCULIN', 'NA-FLUOR', 
'RHODAMINE-6G', 'RHODAMINE-B', 'ACRIDINE-RED']
max_val,min_val=max(sum(limits,[])),min(sum(limits,[]))
coverages={}
for i in range(min_val,max_val+1):
    cover=[]
    for j in range(len((limits))):
        if limits[j][0]<=i and limits[j][1]>=i:
            cover.append(j)
    coverages[i]=cover
intervals={}
start=min_val

for i in range(min_val,max_val):
    if coverages[i]==coverages[i+1]:
        continue
    intervals[start]=[start,i]
    start=i+1

#마지막 구간은 for 문에서 자동으로 추가되지 않기 때문에 직접 써준다.
intervals[start]=[start,max_val]


# 데이터 분석 코드
costs = [4, 3, 1, 4, 1, 6, 2, 3, 1, 2, 2, 2, 2, 2, 9, 3, 1, 9, 8, 8, 2]
from ortools.linear_solver import pywraplp
solver = pywraplp.Solver.CreateSolver("SCIP")
infinity = solver.infinity()

# 의사결정변수
x = {}
for i in range(len(names)):
    x[i] = solver.IntVar(0, infinity, f"x[{i}]")

# 제약조건: 각 구간에 커버하는 하나 이상 약품 필요
for interval in intervals.values():
    solver.Add(sum(x[i] for i in range(len(names)) if i in coverages[interval[0]]) >= 1)

# 목적함수
solver.Minimize(sum(costs[i] * x[i] for i in range(len(names))))


with open('or6-6.lp', "w") as out_f:
    lp_text = solver.ExportModelAsLpFormat(False)
    out_f.write(lp_text)
    
# Solve
status = solver.Solve()

# Print solution
if status == pywraplp.Solver.OPTIMAL:
    print("OPTIMAL")
    print(f"목적함수값 = {solver.Objective().Value():.1f}")
    for i in range(len(names)):
        print(f"{x[i].name()} = {x[i].solution_value()}")
else:
    print("The problem does not have an optimal solution.")

#실습7
from ortools.linear_solver import pywraplp

# 카메라별 커버 가능한 구역
camera = {
    1: {1, 3, 4, 6, 7},
    2: {4, 7, 8, 12},
    3: {2, 5, 9, 11, 13},
    4: {1, 2, 14, 15},
    5: {3, 6, 10, 12, 14},
    6: {8, 14, 15},
    7: {1, 2, 6, 11},
    8: {1, 2, 4, 6, 8, 12}
}

all_zones = set(range(1, 16))  # 1~15번 구역

# OR-Tools solver 생성
solver = pywraplp.Solver.CreateSolver('SCIP')

# 카메라 선택 여부를 나타내는 이진 변수
camera_vars = {}
for c in camera:
    camera_vars[c] = solver.BoolVar(f'camera_{c}')

# 제약조건: 모든 구역은 적어도 하나의 카메라에 의해 커버되어야 함
for z in all_zones:
    solver.Add(sum(camera_vars[c] for c in camera if z in camera[c]) >= 1)

# 목적함수: 카메라 선택 수 최소화
solver.Minimize(solver.Sum(camera_vars[c] for c in camera))

# 문제 풀기
status = solver.Solve()

# 결과 출력
if status == pywraplp.Solver.OPTIMAL:
    selected = [c for c in camera_vars if camera_vars[c].solution_value() == 1]
    print("최소 카메라 수:", len(selected))
    print("설치할 카메라 위치:", selected)
