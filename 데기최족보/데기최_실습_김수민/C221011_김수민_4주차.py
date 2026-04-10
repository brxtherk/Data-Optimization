#4-1 정수 계획 모형
from ortools.linear_solver import pywraplp
def main():
    # Create the mip solver with the SCIP backend.
    solver = pywraplp.Solver.CreateSolver("SAT")
    if not solver: 
        return
    
    infinity = solver.infinity()
    # x and y are integer non-negative variables.
    #x = solver.IntVar(0.0, infinity, "x")
    #y = solver.IntVar(0.0, infinity, "y")
    x = solver.NumVar(0.0, infinity, "x")
    y = solver.NumVar(0.0, infinity, "y")

    solver.Add(x + 7 * y <= 17.5)
    solver.Add(x <= 3.5)
    
    solver.Maximize(x + 10 * y)
    
    print(f"Solving with {solver.SolverVersion()}")

    status = solver.Solve()
    
    if status == pywraplp.Solver.OPTIMAL:
        print("Solution:")
        print("Objective value =", solver.Objective().Value())
        print("x =", x.solution_value())
        print("y =", y.solution_value())
    else:
        print("The problem does not have an optimal solution.")
if __name__ == "__main__":
    main()

# 4-2. 스태프 결정 문제

from ortools.linear_solver import pywraplp
solver = pywraplp.Solver.CreateSolver("SAT")

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
with open('문제4-2.lp', "w") as out_f:
    lp_text = solver.ExportModelAsLpFormat(False)
    out_f.write(lp_text)
    
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL:
    print("Objective value =", solver.Objective().Value())
    for i in range(7):
        print(x[i].name(), " = ", x[i].solution_value())
else:
    print("The problem does not have an optimal solution.")


# 4-3. 스태프 결정 문제 2

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

with open("문제4-3.lp", "w") as out_f:
    lp_text = solver.ExportModelAsLpFormat(False)
    out_f.write(lp_text)

status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL:
    print("Objective value = {}".format(solver.Objective().Value()))
    for i in range(24):
        print("{} = {}".format(x[i].name(), x[i].solution_value()))
else:
    print("The problem does not have an optimal solution.")

#문제 4-4. 클러스터링
from ortools.linear_solver import pywraplp
solver=pywraplp.Solver.CreateSolver('SAT')
x={}
for i in range(8):
    for j in range(8):
        if i !=j:
            x[i,j]=solver.IntVar(0,1,'X'+str(i)+str(j))
#Rating[j,i]는 x[i,j]의 목적함수 계수
Ratings = [
    [0, 9, 3, 4, 2, 1, 5, 6],
    [0, 0, 1, 7, 3, 5, 2, 1],
    [0, 0, 0, 4, 4, 2, 9, 2],
    [0, 0, 0, 0, 1, 5, 5, 2],
    [0, 0, 0, 0, 0, 8, 7, 6],
    [0, 0, 0, 0, 0, 0, 2, 3],
    [0, 0, 0, 0, 0, 0, 0, 4]
]
con=[]
for i in range(8):
    con.append(solver.Constraint(1,1))
    for j in range(8):
        if i !=j:
            con[i].SetCoefficient(x[i,j],1)

for i in range(8):
    for j in range(8):
        if i < j:
            solver.Add(x[i, j] ==x[j, i], 'x_'+str(i)+'_'+str(j))
obj=solver.Objective()
for i in range(7):
    for j in range(8):
        if i!=j:
            obj.SetCoefficient(x[i,j],Ratings[i][j])
obj.SetMaximization()

with open('실습4주차(1)','w') as out_f:
    lp_text=solver.ExportModelAsLpFormat(False)
    out_f.write(lp_text)
status=solver.Solve()
if status==pywraplp.Solver.OPTIMAL:
    print('objective value=' ,obj.Value())
    for i in range(8):
        for j in range(8):
            if i!=j and x[i,j].solution_value()!=0:
                print(x[i,j].name(),x[i,j].solution_value())

#추가실습1. 집안일문제
Time=[[4.5,7.8,3.6,2.9],
      [4.9,7.2,4.3,3.1]]
from ortools.linear_solver import pywraplp
solver=pywraplp.Solver.CreateSolver('SAT')

x={}
for i in range(2):
    for j in range(4):
        x[i,j]=solver.IntVar(0,1,'X'+str(i)+str(j))
#각 두개씩
min_2=[]
for i in range(2):
    min_2.append(solver.Constraint(2,solver.infinity()))
    for j in range(4):
        min_2[i].SetCoefficient(x[i,j],1)
#각 집안일 당 한명 배치
Work=[]
for i in range(4):
    Work.append(solver.Constraint(1,1))
    for j in range(2):
        Work[i].SetCoefficient(x[j,i],1)
#목적함수
objective=solver.Objective()
for i in range(2):
    for j in range(4):
        objective.SetCoefficient(x[i,j],Time[i][j])        
objective.SetMinimization()

with open('실습4주차(2)','w') as out_f:
    lp_text=solver.ExportModelAsLpFormat(False)
    out_f.write(lp_text)
status=solver.Solve()
if status==pywraplp.Solver.OPTIMAL:
    print(f'objective value= {objective.Value():.1f}')
    for i in range(2):
        for j in range(4):
            print(x[i,j].name(), ':',x[i,j].solution_value())

#추가실습2. 투자문제
profit=[17,10,15,19,7,13,9]
required=[43,28,34,48,17,32,23]
#총 투자 가능 금액 1억달러(100)
from ortools.linear_solver import pywraplp
solver=pywraplp.Solver.CreateSolver('SAT')
#SAT는 정수 계획형에 더 적합
x= {}
for i in range(7):
    x[i]=solver.IntVar(0,1,'X'+str(i))
    
#제약조건1
#투자 가능 금액 1억
limit=[]
for i in range(7):
    limit.append(x[i]*required[i])
solver.Add(sum(limit)<=100)

#1과 2중 하나가 선택되지 않으면 3,4 선택 불가능
#x[i]는 0 또는 1 (이진변수)
solver.Add(x[0]+x[1]>=x[2])
solver.Add(x[0]+x[1]>=x[3])
obj=[]
for i in range(7):
    obj.append(x[i]*profit[i])
solver.Maximize(sum(obj))

with open('실습4주차 추가실습(2)','w') as out_f:
    lp_text=solver.ExportModelAsLpFormat(False)
    out_f.write(lp_text)
    
status=solver.Solve()
if status==pywraplp.Solver.OPTIMAL:
    print(solver.Objective().Value())
    for i in range(7):
        print(x[i].name(),':', x[i].solution_value())

#추가실습3. 수송문제
#공장 제작 수량 60,80,40
#고객1,2 주문 수량 40,60
#고객 3 최소 20 ~ INFINITY
#고객 4 남는 것 가능한 많이

profit=[[800,700,500,200],
        [500,200,100,300],
        [600,400,300,500]
        ]
from ortools.linear_solver import pywraplp
solver=pywraplp.Solver.CreateSolver('SAT')
x={}
for i in range (3):
    for j in range(4):
        x[i,j]=solver.IntVar(0,solver.infinity(),'X'+str(i)+str(j))
    
#제약조건1: 공장 제작 수량
product=[60,80,40]
fac=[]
for i in range(3):
    fac.append(solver.Constraint(product[i],product[i]))
    for j in range(4):
        fac[i].SetCoefficient(x[i,j],1)

#고객 주문량
needs_min=[40,60,20,0]
needs_max=[40,60,solver.infinity(),solver.infinity()]
order=[]
for j in range(4):
    order.append(solver.Constraint(needs_min[j],needs_max[j]))
    for i in range(3):
        order[j].SetCoefficient(x[i,j],1)

objective=solver.Objective()
for i in range(3):
    for j in range(4):
        objective.SetCoefficient(x[i,j],profit[i][j])
objective.SetMaximization()

with open('실습4주차 추가실습(3)','w') as out_f:
    lp_text=solver.ExportModelAsLpFormat(False)
    out_f.write(lp_text)
    
status=solver.Solve()
if status==pywraplp.Solver.OPTIMAL:
    print(objective.Value())
    for j in range(4):
        print(f'고객 {j} 총 구입량: {sum(x[i,j].solution_value() for i in range(3))}')
        for i in range(3):
            print(f'{x[i,j].name()}: {x[i,j].solution_value()}')
else:
    print("The problem does not have an optimal solution.")