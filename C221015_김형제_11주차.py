# 연습문제 1
from ortools.linear_solver import pywraplp

def solve_smc_problem():
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        print("솔버를 생성할 수 없습니다.")
        return
    
    shipping_costs = [
        [67, 16, 27, 65, 46, 112], # 공장 1
        [58, 78, 39, 4, 20, 48],   # 공장 2
        [17, 96, 57, 20, 38, 32],  # 공장 3
        [15, 54, 22, 42, 27, 93],  # 공장 4
        [37, 66, 28, 20, 12, 72]   # 공장 5
    ]
    
    fixed_costs = [306, 140, 200, 164, 88] # 연간 고정비
    capacities = [18, 24, 27, 22, 31]      # 연간 생산용량 
    demands = [10, 8, 12, 6, 7, 11]        # 연간 수요량 

    num_plants = len(fixed_costs)
    num_warehouses = len(demands)

    y = [solver.IntVar(0, 1, f'y_{i}') for i in range(num_plants)]
    x = [[solver.NumVar(0, solver.infinity(), f'x_{i}_{j}') 
          for j in range(num_warehouses)] for i in range(num_plants)]

    objective = solver.Objective()
    for i in range(num_plants):
        objective.SetCoefficient(y[i], fixed_costs[i])
        for j in range(num_warehouses):
            objective.SetCoefficient(x[i][j], shipping_costs[i][j])
    objective.SetMinimization()

    for j in range(num_warehouses):
        solver.Add(solver.Sum([x[i][j] for i in range(num_plants)]) == demands[j])
    
    for i in range(num_plants):
        solver.Add(solver.Sum([x[i][j] for j in range(num_warehouses)]) <= capacities[i] * y[i])

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print(f"최적 총 비용: ${objective.Value() * 1000:,.0f}")
        
        active_fixed_cost = sum(fixed_costs[i] for i in range(num_plants) if y[i].solution_value() > 0.5)
        print(f"(고정비 합계: ${active_fixed_cost * 1000:,.0f}, 수송비 합계: ${(objective.Value() - active_fixed_cost) * 1000:,.0f})\n")
        
        for i in range(num_plants):
            if y[i].solution_value() > 0.5:
                print(f"공장 {i+1} 가동")
                for j in range(num_warehouses):
                    if x[i][j].solution_value() > 0:
                        print(f" -> 창고 {j+1}: {x[i][j].solution_value()} (1000대)")
    else:
        print("최적해를 찾을 수 없습니다.")

solve_smc_problem()

# 연습문제 2-1
from ortools.linear_solver import pywraplp

def solve_capacitated_plant_location():
    # 데이터 정의
    facilities = ['루마니아', '폴란드', '아일랜드']
    markets = ['프랑스', '독일', '이탈리아', '스페인', '영국']
    
    fixed_costs = [18000000, 17500000, 24500000]
    capacities = [40000, 40000, 40000]
    demands = [15000, 20000, 13000, 12000, 19000]
    
    variable_costs = [
        [23, 9, 23, 29, 33],  
        [19, 15, 21, 26, 36], 
        [31, 11, 40, 40, 20]  
    ]
    
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        print("SCIP 솔버를 사용할 수 없습니다.")
        return
    
    y = {}
    for i in range(len(facilities)):
        y[i] = solver.IntVar(0, 1, f'y_{i}')
        
    x = {}
    for i in range(len(facilities)):
        for j in range(len(markets)):
            x[i, j] = solver.IntVar(0, solver.infinity(), f'x_{i}_{j}')
            
    for j in range(len(markets)):
        solver.Add(sum(x[i, j] for i in range(len(facilities))) == demands[j])
        
    for i in range(len(facilities)):
        solver.Add(sum(x[i, j] for j in range(len(markets))) <= capacities[i] * y[i])
        
    objective = solver.Objective()
    for i in range(len(facilities)):
        objective.SetCoefficient(y[i], fixed_costs[i])
        for j in range(len(markets)):
            objective.SetCoefficient(x[i, j], variable_costs[i][j])
    objective.SetMinimization()

    status = solver.Solve()
    
    if status == pywraplp.Solver.OPTIMAL:
        print("최적해를 찾았습니다.\n")
        print(f"최소 총 비용: {int(objective.Value()):,} 원")
        print("-" * 40)
        
        for i in range(len(facilities)):
            if y[i].solution_value() > 0.5: 
                print(f"[{facilities[i]}] 생산기지: 가동 (고정비: {fixed_costs[i]:,} 발생)")
                for j in range(len(markets)):
                    if x[i, j].solution_value() > 0:
                        allocated_amount = int(x[i, j].solution_value())
                        print(f"  -> {markets[j]} 시장으로 {allocated_amount:,} 단위 배분")
            else:
                print(f"[{facilities[i]}] 생산기지: 미가동")
    else:
        print("최적해를 찾지 못했습니다. 상태 코드:", status)

if __name__ == '__main__':
    solve_capacitated_plant_location()

# 연습문제 2-2
from ortools.linear_solver import pywraplp

def solve_updated_capacitated_location():
    # 데이터 정의
    facilities = ['루마니아', '폴란드', '아일랜드']
    markets = ['프랑스', '독일', '이탈리아', '스페인', '영국']
    
    demands = [15000, 40000, 13000, 12000, 19000]
    
    variable_costs = [
        [23, 9, 23, 29, 33],  
        [19, 15, 21, 26, 36], 
        [31, 11, 40, 40, 20] 
    ]
    
    # 저용량 공장 데이터
    fixed_costs_low = [18000000, 17500000, 24500000]
    capacity_low = [40000, 40000, 40000]
    
    # 고용량 공장 데이터
    fixed_costs_high = [23400000, 22750000, 31850000]
    capacity_high = [60000, 60000, 60000]
    
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        print("SCIP 솔버를 사용할 수 없습니다.")
        return

    y_low = {}
    y_high = {}
    for i in range(len(facilities)):
        # y_low[i]: 생산기지 i에 저용량 공장 설립 시 1, 아니면 0
        y_low[i] = solver.IntVar(0, 1, f'y_low_{i}')
        # y_high[i]: 생산기지 i에 고용량 공장 설립 시 1, 아니면 0
        y_high[i] = solver.IntVar(0, 1, f'y_high_{i}')
        
    x = {}
    for i in range(len(facilities)):
        for j in range(len(markets)):
            x[i, j] = solver.IntVar(0, solver.infinity(), f'x_{i}_{j}')
            
    for j in range(len(markets)):
        solver.Add(sum(x[i, j] for i in range(len(facilities))) == demands[j])
        
    for i in range(len(facilities)):
        solver.Add(sum(x[i, j] for j in range(len(markets))) <= capacity_low[i] * y_low[i] + capacity_high[i] * y_high[i])
        
    for i in range(len(facilities)):
        solver.Add(y_low[i] + y_high[i] <= 1)

    objective = solver.Objective()
    for i in range(len(facilities)):
        objective.SetCoefficient(y_low[i], fixed_costs_low[i])
        objective.SetCoefficient(y_high[i], fixed_costs_high[i])
        for j in range(len(markets)):
            objective.SetCoefficient(x[i, j], variable_costs[i][j])
    objective.SetMinimization()

    status = solver.Solve()
    
    if status == pywraplp.Solver.OPTIMAL:
        print("최적해를 찾았습니다.\n")
        print(f"최소 총 비용: {int(objective.Value()):,} 원")
        
        for i in range(len(facilities)):
            if y_low[i].solution_value() > 0.5:
                print(f"[{facilities[i]}] 생산기지: 저용량 공장 가동 (고정비: {fixed_costs_low[i]:,} 발생)")
                for j in range(len(markets)):
                    if x[i, j].solution_value() > 0:
                        print(f"  -> {markets[j]} 시장으로 {int(x[i, j].solution_value()):,} 단위 배분")
            elif y_high[i].solution_value() > 0.5:
                print(f"[{facilities[i]}] 생산기지: 고용량 공장 가동 (고정비: {fixed_costs_high[i]:,} 발생)")
                for j in range(len(markets)):
                    if x[i, j].solution_value() > 0:
                        print(f"  -> {markets[j]} 시장으로 {int(x[i, j].solution_value()):,} 단위 배분")
            else:
                print(f"[{facilities[i]}] 생산기지: 미가동")
    else:
        print("최적해를 찾지 못했습니다. 상태 코드:", status)

if __name__ == '__main__':
    solve_updated_capacitated_location()

# 연습문제 3-1
from ortools.linear_solver import pywraplp

def solve_shortest_path_ex3_1():
    # 솔버 생성 (MIP)
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        print("SCIP 솔버를 사용할 수 없습니다.")
        return

    # 데이터 정의
    node_name = {0: 'O', 1: 'A', 2: 'B', 3: 'C', 4: 'D', 5: 'E', 6: 'T'}
    
    COSTS = {
        (0, 1): 4, (0, 2): 6, (0, 3): 5,
        (1, 2): 1, (2, 1): 1,
        (1, 4): 7, (4, 1): 7,
        (2, 3): 2, (3, 2): 2,
        (2, 4): 5, (4, 2): 5,
        (2, 5): 4, (5, 2): 4,
        (3, 5): 5, (5, 3): 5,
        (4, 5): 1, (5, 4): 1,
        (4, 6): 6,
        (5, 6): 8
    }
    
    FLOW = [1, 0, 0, 0, 0, 0, -1]
    nNodes = len(FLOW)
    
    X = {}
    for key in COSTS.keys():
        X[key] = solver.IntVar(0, 1, "X[%i,%i]" % (key[0], key[1]))
        
    for i in range(nNodes):
        const_expr = []
        for key in COSTS.keys():
            if key[0] == i: 
                const_expr.append(X[key])
            elif key[1] == i: 
                const_expr.append(-X[key])
                
        solver.Add(solver.Sum(const_expr) == FLOW[i], 'node_'+str(i))
        
    objective = solver.Objective()
    for key in COSTS.keys():
        objective.SetCoefficient(X[key], COSTS[key])
    objective.SetMinimization()
    
    status = solver.Solve()
    
    if status == pywraplp.Solver.OPTIMAL:
        print("최적해를 찾았습니다.\n")
        print(f"최단 거리 (최소 비용): {int(objective.Value())}")
        print("-" * 40)
        print("선정된 최단 경로:")
        
        current_node = 0
        while current_node != 6:
            for key in COSTS.keys():
                if key[0] == current_node and X[key].solution_value() > 0.5:
                    print(f"  {node_name[key[0]]} -> {node_name[key[1]]} (비용: {COSTS[key]})")
                    current_node = key[1]
                    break
    else:
        print("최적해를 찾지 못했습니다.")

if __name__ == '__main__':
    solve_shortest_path_ex3_1()

# 연습문제 3-2
from ortools.linear_solver import pywraplp

def solve_shortest_path_ex3_2():
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        print("SCIP 솔버를 사용할 수 없습니다.")
        return

    node_name = {
        0: 'O', 1: 'A', 2: 'B', 3: 'C', 4: 'D', 
        5: 'E', 6: 'F', 7: 'G', 8: 'H', 9: 'I', 10: 'T'
    }
    
    COSTS = {
        (0, 1): 4, (0, 3): 6, (0, 2): 3,  
        (1, 4): 3, (1, 3): 5,             
        (2, 3): 4, (2, 5): 6,             
        (3, 4): 2, (3, 6): 2, (3, 5): 5,  
        (4, 7): 4, (4, 6): 2,             
        (5, 6): 1, (5, 8): 2, (5, 9): 5, 
        (6, 7): 2, (6, 8): 5,             
        (8, 7): 2,                        
        (7, 10): 7,                       
        (8, 10): 8,                       
        (9, 8): 3, (9, 10): 4            
    }
    
    FLOW = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1]
    nNodes = len(FLOW)
    
  
    X = {}
    for key in COSTS.keys():
        X[key] = solver.IntVar(0, 1, f"X[{key[0]},{key[1]}]")
        
    for i in range(nNodes):
        const_expr = []
        for key in COSTS.keys():
            if key[0] == i:   
                const_expr.append(X[key])
            elif key[1] == i: 
                const_expr.append(-X[key])
                
        solver.Add(solver.Sum(const_expr) == FLOW[i], f'node_{i}')
        

    objective = solver.Objective()
    for key in COSTS.keys():
        objective.SetCoefficient(X[key], COSTS[key])
    objective.SetMinimization()
    
    status = solver.Solve()
    
    if status == pywraplp.Solver.OPTIMAL:
        print("최적해를 찾았습니다.\n")
        print(f"최단 거리 (최소 비용): {int(objective.Value())}")
        print("선정된 최단 경로:")
        

        current_node = 0 
        target_node = 10 
        
        while current_node != target_node:
            for key in COSTS.keys():
                if key[0] == current_node and X[key].solution_value() > 0.5:
                    print(f"  {node_name[key[0]]} -> {node_name[key[1]]} (비용: {COSTS[key]})")
                    current_node = key[1]
                    break
    else:
        print("최적해를 찾지 못했습니다.")

if __name__ == '__main__':
    solve_shortest_path_ex3_2()