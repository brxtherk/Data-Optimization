#수송문제1
#제약조건: 각 공급지는 자신의 생산 능력 이상 보낼 수 없음
#각 수요지는 필요한 만큼 꼭 받아야 함
#목적함수: 총 운송비용 최소화
from ortools.linear_solver import pywraplp
solver=pywraplp.Solver.CreateSolver('SCIP')
tcosts = [
 [464, 513, 654, 867],
 [352, 416, 690, 791],
 [995, 682, 388, 685]
 ]
x={}
for i in range(3):
    for j in range(4):
        x[i,j]=solver.IntVar(0,solver.infinity(),f'x[{i},{j}]')
#data={'output':{75,125,100}, 'allocation' : {80,65,70,85}}
#위처럼 데이터 입력했을 때 집합으로 정의된 숫자 사이에는 순서가 부여되지 않는다. 순서대로 값을 부여하는 for 문을 사용할 것이므로 리스트 형식을 쓰면 순서가 부여된다.
data={'output':[75,125,100], 'allocation' : [80,65,70,85]}
for j,c in enumerate(data['allocation']):
    solver.Add(sum(x[i,j] for i in range(3))>=c)
for i,c in enumerate(data['output']):
    solver.Add(sum(x[i,j] for j in range(4))<=c)
solver.Minimize(sum(tcosts[i][j]*x[i,j] for i in range(3) for j in range(4)))
with open('수송1','w') as out_f:
    lp_text=solver.ExportModelAsLpFormat(False)
    out_f.write(lp_text)
    
status=solver.Solve()
if status==pywraplp.Solver.OPTIMAL:
    print(solver.Objective().Value())
    for i in range(3):
        for j in range(4):
            if x[i,j].solution_value() !=0:
                print(x[i,j].name(),':',x[i,j].solution_value())
#수송문제2-풀이1
from ortools.linear_solver import pywraplp
solver=pywraplp.Solver.CreateSolver('SCIP')
#생산>설치
product=[25,35,30,10]
install=[10,15,25,20]
#i달의 생산 개수
x={}
for i in range(4):
    x[i]=solver.IntVar(0,product[i],'x[%i]'%i)
#i달의 설치 개수
y={}
for i in range(4):
    y[i]=solver.IntVar(install[i],solver.infinity(),'y[%i]'%i)
#저장한 상품 누적 제약조건
#누적된 개수
z={}
z[0]=x[0]-y[0]
for i in range(3):
    z[i+1]=x[i+1]-y[i+1]+z[i]
solver.Add(z[3]==0)
cost=[1.08,1.11,1.1,1.13]
cost_save=[0.015,0.015,0.015,0]
solver.Minimize(sum(cost[i]*x[i]+cost_save[i]*z[i] for i in range(4)))

status=solver.Solve()
if status==pywraplp.Solver.OPTIMAL:
    print('Total cost =' ,solver.Objective().Value())
else:
    print('a')

#수송문제2 -풀이2 with 더미도착지
from ortools.linear_solver import pywraplp
solver = pywraplp.Solver.CreateSolver("SCIP")

# 모델링
# 의사결정변수 (4x5 짜리 변수 생성)
# 제약조건 : x00 + x01 x02 x03 x04 ==25... 


# 의사결정변수
x = {}
for i in range(4) :
    for j in range(5) :
        x[i, j] = solver.IntVar(0, solver.infinity(), 'x[%i, %i] ' % (i, j))
        

# 제약조건
M = 10000000000000

cost = [
        [1.080, 1.095, 1.110, 1.125, 0],
        [M, 1.110, 1.125, 1.140, 0],
        [M, M, 1.100, 1.115, 0],
        [M, M, M, 1.130, 0]
        ]

demand = [10, 15, 25, 20, 30]
supply = [25, 35, 30, 10]

# 1)
for i in range(4) :
    co1 = [x[i, j] for j in range(5)] 
    solver.Add(solver.Sum(co1) == supply[i])

# 2)
for j in range(5) :
    co2 = [x[i, j] for i in range(4)]
    solver.Add(solver.Sum(co2) == demand[j])

# 목적함수
ob = []
for i in range(4) :
    for j in range(5):
        ob.append(cost[i][j] * x[i, j])

solver.Minimize(solver.Sum(ob))

status = solver.Solve()

# Print solution
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print(f"Total cost = {solver.Objective().Value():.1f}" )

#%% 수송 문제 with 더미 도착지 (실습) – Option 1
from ortools.linear_solver import pywraplp
solver=pywraplp.Solver.CreateSolver('SCIP')
M = 10000000000000

ab = [
      [41, 27, 28, 24, 0],
      [40, 29, M, 23, 0],
      [37, 30, 27, 21, 0]
      ]

demand = [ 20, 30, 30, 40, 75 ]
supply = [75, 75, 45]
x={}
# 의사결정변수
for i in range(3) :
    for j in range(5) :
        x[i,j] = solver.IntVar(0, solver.infinity(), 'x[%i, %i]' % (i, j))
        
# 제약조건
# 1)
for i in range(3) :
    co1 = [x[i, j] for j in range(5)] 
    solver.Add(solver.Sum(co1) == supply[i])

# 2)
for j in range(5) :
    co2 = [x[i, j] for i in range(3)]
    solver.Add(solver.Sum(co2) == demand[j])

# 목적함수
ob = []
for i in range(3) :
    for j in range(5):
        ob.append(ab[i][j] * x[i, j])

solver.Minimize(solver.Sum(ob))

# Solve the problem
status = solver.Solve()

# Print solution
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print(f"총 생산량 = {solver.Objective().Value():.1f}" )
    for src in range(3):
        for dest in range(5):
            if x[src, dest].solution_value() > 0.5:
                print(
                    f"Source {src} supplies to destination {dest}."
                    + f"Quantity = {x[src, dest].solution_value():.1f}")
else:
    print("No solution found.")
    
#%% 수송 문제 with 더미 도착지 (실습) – Option 2


# Data
M = 10000000000

tcosts =  [
    [820, 810, 840, 960, 0],
    [820, 810, 840, 960, 0],
    [800, 870, M, 920, 0],
    [800, 870, M, 920, 0],
    [740, 900, 810, 840, M]
]

x = {}
for i in range(5):
    for j in range(5):
        x[i, j] = solver.IntVar(0, 1, f"x[{i},{j}]")
#할당문제를 수송문제로 (실습문제2)
from ortools.graph.python import min_cost_flow
smcf=min_cost_flow.SimpleMinCostFlow()
start_nodes = (
 [0, 0, 0, 0] + [1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4] + [5, 6, 7, 8]
 )
end_nodes = (
 [1, 2, 3, 4] + [5, 6, 7, 8, 5, 6, 7, 8, 5, 6, 7, 8, 5, 6, 7, 8] + [9, 9, 9, 9]
 )
capacities = (
 [1, 1, 1, 1] + [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1] + [1, 1, 1, 1]
 )
cost=(
      [0,0,0,0]+[500,400,600,700,600,600,700,500,700,500,700,600,500,400,600,600] +[0,0,0,0])
source=0
sink=9
tasks=4
#supllies는 4개(tasks)가 출발하고 마지막 값은 4개를 받아야 한다는 뜻
#중간 노드들은 들어온만큼 내보내기 때문에 0으로 세팅함
supplies=[tasks,0,0,0,0,0,0,0,0,-tasks]
for i in range(len(start_nodes)):
    smcf.add_arc_with_capacity_and_unit_cost( 
    start_nodes[i], end_nodes[i], capacities[i], cost[i]
 )
 # Add node supplies.
for i in range(len(supplies)):
    smcf.set_node_supply(i, supplies[i])
supplies = [tasks, 0, 0, 0, 0, 0, 0, 0, 0, -tasks]
 # Find the minimum cost flow between node 0 and node 10.
status = smcf.solve()
if status == smcf.OPTIMAL:
    print(smcf.optimal_cost())
    for arc in range(smcf.num_arcs()):
        if smcf.tail(arc) != source and smcf.head(arc)!=sink:
            if smcf.flow(arc)>0:
                print(
                    'ship%d port%d cost$%d'%(smcf.tail(arc),smcf.head(arc),smcf.unit_cost(arc)))
#할당문제를 수송문제로 … (실습문제 3)

from ortools.graph.python import min_cost_flow

# Instantiate a SimpleMinCostFlow solver.
smcf = min_cost_flow.SimpleMinCostFlow()

# Define the directed graph for the flow.
start_nodes = (
[0, 0, 0, 0] + [1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4] + [5, 6, 7, 8, 9]
)
end_nodes = (
[1, 2, 3, 4] + [5, 6, 7, 8, 9, 5, 6, 7, 8, 9, 5, 6, 7, 8, 9, 5, 6, 7, 8, 9] + [10, 10, 10, 10, 10]
)
capacities = (
[1, 1, 1, 1] + [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1] + [1, 1, 1, 1, 1]
)
costs = (
[0, 0, 0, 0]
+ [377, 329, 338, 370, 354, 434, 331, 422, 347, 418, 333, 285, 389, 304, 336, 292, 264, 296, 285, 311]
+ [0, 0, 0, 0, 0]
)

source = 0
sink = 10
tasks = 4

supplies = [tasks, 0, 0, 0, 0, 0, 0, 0, 0, 0, -tasks]

# Add each arc.
for i in range(len(start_nodes)):
    smcf.add_arc_with_capacity_and_unit_cost(
    start_nodes[i], end_nodes[i], capacities[i], costs[i]
    )
# Add node supplies.
for i in range(len(supplies)):
    smcf.set_node_supply(i, supplies[i])
    supplies = [tasks, 0, 0, 0, 0, 0, 0, 0, 0, 0, -tasks]
    
# Find the minimum cost flow between node 0 and node 10.
status = smcf.solve()

if status == smcf.OPTIMAL:
    print("Total cost = ", smcf.optimal_cost())
    print()
    for arc in range(smcf.num_arcs()):
# Can ignore arcs leading out of source or into sink.
        if smcf.tail(arc) != source and smcf.head(arc) != sink:
# Arcs in the solution have a flow value of 1. Their start and end nodes
# give an assignment of worker to task.     
            if smcf.flow(arc) > 0:
                print("Worker %d assigned to task %d. Cost = %d"% (smcf.tail(arc), smcf.head(arc), smcf.unit_cost(arc)))
else:
    print("There was an issue with the min cost flow input.")
    print(f"Status: {status}")
    