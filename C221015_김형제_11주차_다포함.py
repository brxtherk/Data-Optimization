# -*- coding: utf-8 -*-
"""
Created on Thu May 14 14:18:06 2026

@author: redti
"""

#예제 1
from ortools.linear_solver import pywraplp

def solve_facility_location():
    # 최적화 솔버 소환 (SCIP는 혼합 정수 계획법에 강력함)
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        return

    # --- 1. 데이터 입력 ---
    # 각 창고에서 각 도시로의 운송비용 행렬 (c_ij)
    costs = [
        [1675, 400, 685, 1630, 1160, 2800],  # 창고 A
        [1460, 1940, 970, 100, 495, 1200],   # 창고 B
        [1925, 2400, 1425, 500, 950, 800],   # 창고 C
        [380, 1355, 543, 1045, 665, 2321],   # 창고 D
        [922, 1646, 700, 508, 311, 1797]     # 창고 E
    ]
    
    fixed_costs = [7650, 3500, 3500, 4100, 2200]  # 월 고정비용
    supply_capacity = [18, 24, 27, 22, 31]        # 월 공급량 (용량)
    demand = [10, 8, 12, 6, 7, 11]                # 도시별 월간 수요

    num_warehouses = len(fixed_costs)
    num_cities = len(demand)
    warehouse_names = ['A', 'B', 'C', 'D', 'E']

    # --- 2. 결정 변수 선언 ---
    # y[i] : 창고 i 건설 여부 (0 또는 1)
    y = {}
    for i in range(num_warehouses):
        y[i] = solver.IntVar(0, 1, f'y[{i}]')

    # x[i, j] : 창고 i에서 도시 j로의 운송량 (0 이상 실수/정수)
    x = {}
    for i in range(num_warehouses):
        for j in range(num_cities):
            x[i, j] = solver.NumVar(0, solver.infinity(), f'x[{i},{j}]')

    # --- 3. 목적 함수 설정 ---
    # 최소화: (고정비 * 창고건설여부) + (운송비 * 운송량)
    objective = solver.Objective()
    for i in range(num_warehouses):
        objective.SetCoefficient(y[i], fixed_costs[i])
        for j in range(num_cities):
            objective.SetCoefficient(x[i, j], costs[i][j])
    objective.SetMinimization()

    # --- 4. 제약 조건 설정 ---
    # 제약 1: 수요 충족 (각 도시가 받는 물량의 합 = 그 도시의 수요량)
    for j in range(num_cities):
        constraint = solver.RowConstraint(demand[j], demand[j], f'Demand_{j}')
        for i in range(num_warehouses):
            constraint.SetCoefficient(x[i, j], 1)

    # 제약 2: 공급 용량 제약 및 논리적 연결 (x의 합 <= 용량 * y)
    # y가 0(건설 안함)이면 우변이 0이 되어 운송량 x도 0이 됨.
    for i in range(num_warehouses):
        # 식 정리: (운송량 합) - (용량 * y) <= 0
        constraint = solver.RowConstraint(-solver.infinity(), 0, f'Capacity_{i}')
        constraint.SetCoefficient(y[i], -supply_capacity[i])
        for j in range(num_cities):
            constraint.SetCoefficient(x[i, j], 1)

    # --- 5. 풀이 및 결과 출력 ---
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print(f"최소 총 비용: {objective.Value():,.0f}원\n")
        print("--- 최적 창고 건설 및 운송 계획 ---")
        for i in range(num_warehouses):
            if y[i].solution_value() > 0.5:  # 창고를 건설하는 경우 (1)
                print(f"창고 {warehouse_names[i]} (건설됨, 고정비: {fixed_costs[i]})")
                for j in range(num_cities):
                    if x[i, j].solution_value() > 0:
                        print(f"   -> 도시 {j+1}로 {x[i, j].solution_value()}톤 운송 (단가: {costs[i][j]})")
    else:
        print("최적해를 찾지 못했습니다.")

solve_facility_location()

# 연습문제 1
from ortools.linear_solver import pywraplp

def solve_smc_problem():
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        print("솔버를 생성할 수 없습니다.")
        return
    
    # --- 1. 데이터 입력 ---
    shipping_costs = [
        [67, 16, 27, 65, 46, 112], # 공장 1
        [58, 78, 39, 4, 20, 48],   # 공장 2
        [17, 96, 57, 20, 38, 32],  # 공장 3
        [15, 54, 22, 42, 27, 93],  # 공장 4
        [37, 66, 28, 20, 12, 72]   # 공장 5
    ]
    
    fixed_costs = [306, 140, 200, 164, 88] # 연간 고정비 ($1000)
    capacities = [18, 24, 27, 22, 31]      # 연간 생산용량 (1000대)
    demands = [10, 8, 12, 6, 7, 11]        # 연간 수요량 (1000대)

    num_plants = len(fixed_costs)
    num_warehouses = len(demands)

    # --- 2. 변수 선언 ---
    y = [solver.IntVar(0, 1, f'y_{i}') for i in range(num_plants)]
    x = [[solver.NumVar(0, solver.infinity(), f'x_{i}_{j}') 
          for j in range(num_warehouses)] for i in range(num_plants)]

    # --- 3. 목적 함수 (최소화) ---
    # 여기서 objective라는 변수명을 명확히 선언해줄게
    objective = solver.Objective()
    for i in range(num_plants):
        objective.SetCoefficient(y[i], fixed_costs[i])
        for j in range(num_warehouses):
            objective.SetCoefficient(x[i][j], shipping_costs[i][j])
    objective.SetMinimization()

    # --- 4. 제약 조건 ---
    for j in range(num_warehouses):
        solver.Add(solver.Sum([x[i][j] for i in range(num_plants)]) == demands[j])
    
    for i in range(num_plants):
        solver.Add(solver.Sum([x[i][j] for j in range(num_warehouses)]) <= capacities[i] * y[i])

    # --- 5. 풀이 및 출력 ---
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        # 이제 objective.Value()를 써도 에러가 안 나!
        print(f"✅ 최적 총 비용: ${objective.Value() * 1000:,.0f}")
        
        active_fixed_cost = sum(fixed_costs[i] for i in range(num_plants) if y[i].solution_value() > 0.5)
        print(f"(고정비 합계: ${active_fixed_cost * 1000:,.0f}, 수송비 합계: ${(objective.Value() - active_fixed_cost) * 1000:,.0f})\n")
        
        for i in range(num_plants):
            if y[i].solution_value() > 0.5:
                print(f"공장 {i+1} 가동")
                for j in range(num_warehouses):
                    if x[i][j].solution_value() > 0:
                        print(f"   -> 창고 {j+1}: {x[i][j].solution_value()} (1000대)")
    else:
        print("최적해를 찾을 수 없습니다.")

solve_smc_problem()

# 예제 2
from ortools.linear_solver import pywraplp

def solve_sunoil_location():
    # 데이터 정의
    regions = ['북미', '남미', '유럽', '아시아', '아프리카']
    demands = [12, 8, 14, 16, 7]
    
    # 단위당 변동비용 + 배송비용 (행: 공급지역, 열: 수요지역)
    variable_costs = [
        [81, 92, 101, 130, 115],   # 북미
        [117, 77, 108, 98, 100],   # 남미
        [102, 105, 95, 119, 111],  # 유럽
        [115, 125, 90, 59, 74],    # 아시아
        [142, 100, 103, 105, 71]   # 아프리카
    ]
    
    # 저생산 공장 데이터
    fixed_costs_low = [6000, 4500, 6500, 4100, 4000]
    capacity_low = [10, 10, 10, 10, 10]
    
    # 고생산 공장 데이터
    fixed_costs_high = [9000, 6750, 9750, 6150, 6000]
    capacity_high = [20, 20, 20, 20, 20]
    
    # 솔버 생성 (MIP)
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        print("SCIP 솔버를 사용할 수 없습니다.")
        return

    # 1. 변수 선언
    y_low = {}
    y_high = {}
    for i in range(len(regions)):
        # y_low[i]: i 지역에 저생산 공장 설립 시 1, 아니면 0
        y_low[i] = solver.IntVar(0, 1, f'y_low_{i}')
        # y_high[i]: i 지역에 고생산 공장 설립 시 1, 아니면 0
        y_high[i] = solver.IntVar(0, 1, f'y_high_{i}')
        
    # x[i, j]: i 지역에서 j 지역으로 보내는 물동량
    x = {}
    for i in range(len(regions)):
        for j in range(len(regions)):
            x[i, j] = solver.IntVar(0, solver.infinity(), f'x_{i}_{j}')
            
    # 2. 제약식 추가
    # 제약식 A: 각 지역의 수요량 완벽히 충족
    for j in range(len(regions)):
        solver.Add(sum(x[i, j] for i in range(len(regions))) == demands[j])
        
    # 제약식 B: 생산 용량 제한 (해당 지역에 지어진 공장의 용량을 초과할 수 없음)
    for i in range(len(regions)):
        solver.Add(sum(x[i, j] for j in range(len(regions))) <= capacity_low[i] * y_low[i] + capacity_high[i] * y_high[i])
        
    # 제약식 C: 한 지역에는 최대 하나의 공장만 설립 가능 (저생산과 고생산 중복 설립 방지)
    for i in range(len(regions)):
        solver.Add(y_low[i] + y_high[i] <= 1)

    # 3. 목적함수 설정: (저생산 고정비) + (고생산 고정비) + (단위당 변동비 * 분배물량)
    objective = solver.Objective()
    for i in range(len(regions)):
        objective.SetCoefficient(y_low[i], fixed_costs_low[i])
        objective.SetCoefficient(y_high[i], fixed_costs_high[i])
        for j in range(len(regions)):
            objective.SetCoefficient(x[i, j], variable_costs[i][j])
    objective.SetMinimization()
    
    # 4. 모델 최적화 풀이
    status = solver.Solve()
    
    # 5. 결과 출력
    if status == pywraplp.Solver.OPTIMAL:
        print("최적해를 찾았습니다.\n")
        print(f"최소 총 비용: {int(objective.Value()):,} $")
        print("-" * 50)
        
        for i in range(len(regions)):
            if y_low[i].solution_value() > 0.5:
                print(f"[{regions[i]}] 공장: 저생산 설립 (고정비: {fixed_costs_low[i]:,} $)")
                for j in range(len(regions)):
                    if x[i, j].solution_value() > 0:
                        print(f"  -> {regions[j]} 시장으로 {int(x[i, j].solution_value())} 단위 배분")
            elif y_high[i].solution_value() > 0.5:
                print(f"[{regions[i]}] 공장: 고생산 설립 (고정비: {fixed_costs_high[i]:,} $)")
                for j in range(len(regions)):
                    if x[i, j].solution_value() > 0:
                        print(f"  -> {regions[j]} 시장으로 {int(x[i, j].solution_value())} 단위 배분")
            else:
                print(f"[{regions[i]}] 공장: 미설립")
    else:
        print("최적해를 찾지 못했습니다. 상태 코드:", status)

if __name__ == '__main__':
    solve_sunoil_location()

# 연습문제 2-1
from ortools.linear_solver import pywraplp

def solve_capacitated_plant_location():
    # 데이터 정의
    facilities = ['루마니아', '폴란드', '아일랜드']
    markets = ['프랑스', '독일', '이탈리아', '스페인', '영국']
    
    fixed_costs = [18000000, 17500000, 24500000]
    capacities = [40000, 40000, 40000]
    demands = [15000, 20000, 13000, 12000, 19000]
    
    # 단위당 분배 비용 (행: 생산기지, 열: 수요시장)
    variable_costs = [
        [23, 9, 23, 29, 33],  # 루마니아
        [19, 15, 21, 26, 36], # 폴란드
        [31, 11, 40, 40, 20]  # 아일랜드
    ]
    
    # 솔버 생성 (MIP 솔버인 SCIP 사용)
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        print("SCIP 솔버를 사용할 수 없습니다.")
        return
    
    # 1. 변수 선언
    # y[i]: 생산기지 i가 가동되면 1, 아니면 0
    y = {}
    for i in range(len(facilities)):
        y[i] = solver.IntVar(0, 1, f'y_{i}')
        
    # x[i, j]: 생산기지 i에서 시장 j로 보내는 물동량
    x = {}
    for i in range(len(facilities)):
        for j in range(len(markets)):
            x[i, j] = solver.IntVar(0, solver.infinity(), f'x_{i}_{j}')
            
    # 2. 제약식 추가
    # 제약식 A: 각 수요시장의 수요량 충족
    for j in range(len(markets)):
        solver.Add(sum(x[i, j] for i in range(len(facilities))) == demands[j])
        
    # 제약식 B: 각 생산기지의 생산 용량 제한 및 가동 여부 연동
    for i in range(len(facilities)):
        solver.Add(sum(x[i, j] for j in range(len(markets))) <= capacities[i] * y[i])
        
    # 3. 목적함수 설정: (고정비 * 가동여부) + (단위당 분배비용 * 분배물량)
    objective = solver.Objective()
    for i in range(len(facilities)):
        objective.SetCoefficient(y[i], fixed_costs[i])
        for j in range(len(markets)):
            objective.SetCoefficient(x[i, j], variable_costs[i][j])
    objective.SetMinimization()
    
    # 4. 모델 최적화 풀이
    status = solver.Solve()
    
    # 5. 결과 출력
    if status == pywraplp.Solver.OPTIMAL:
        print("최적해를 찾았습니다.\n")
        print(f"최소 총 비용: {int(objective.Value()):,} 원")
        print("-" * 40)
        
        for i in range(len(facilities)):
            if y[i].solution_value() > 0.5: # 가동 상태(1)인 경우
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
    
    # 수요량 (독일 수요 40,000으로 변경)
    demands = [15000, 40000, 13000, 12000, 19000]
    
    # 단위당 분배 비용 (행: 생산기지, 열: 수요시장)
    variable_costs = [
        [23, 9, 23, 29, 33],  # 루마니아
        [19, 15, 21, 26, 36], # 폴란드
        [31, 11, 40, 40, 20]  # 아일랜드
    ]
    
    # 저용량 공장 데이터
    fixed_costs_low = [18000000, 17500000, 24500000]
    capacity_low = [40000, 40000, 40000]
    
    # 고용량 공장 데이터
    fixed_costs_high = [23400000, 22750000, 31850000]
    capacity_high = [60000, 60000, 60000]
    
    # 솔버 생성 (MIP)
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        print("SCIP 솔버를 사용할 수 없습니다.")
        return

    # 1. 변수 선언
    y_low = {}
    y_high = {}
    for i in range(len(facilities)):
        # y_low[i]: 생산기지 i에 저용량 공장 설립 시 1, 아니면 0
        y_low[i] = solver.IntVar(0, 1, f'y_low_{i}')
        # y_high[i]: 생산기지 i에 고용량 공장 설립 시 1, 아니면 0
        y_high[i] = solver.IntVar(0, 1, f'y_high_{i}')
        
    # x[i, j]: 생산기지 i에서 시장 j로 보내는 물동량
    x = {}
    for i in range(len(facilities)):
        for j in range(len(markets)):
            x[i, j] = solver.IntVar(0, solver.infinity(), f'x_{i}_{j}')
            
    # 2. 제약식 추가
    # 제약식 A: 각 수요시장의 수요량 완벽히 충족
    for j in range(len(markets)):
        solver.Add(sum(x[i, j] for i in range(len(facilities))) == demands[j])
        
    # 제약식 B: 생산 용량 제한 (설립된 공장 유형의 용량을 초과할 수 없음)
    for i in range(len(facilities)):
        solver.Add(sum(x[i, j] for j in range(len(markets))) <= capacity_low[i] * y_low[i] + capacity_high[i] * y_high[i])
        
    # 제약식 C: 한 지역에는 저용량 또는 고용량 중 최대 하나의 공장만 설립 가능
    for i in range(len(facilities)):
        solver.Add(y_low[i] + y_high[i] <= 1)

    # 3. 목적함수 설정: (저용량 고정비) + (고용량 고정비) + (단위당 분배비용 * 분배물량)
    objective = solver.Objective()
    for i in range(len(facilities)):
        objective.SetCoefficient(y_low[i], fixed_costs_low[i])
        objective.SetCoefficient(y_high[i], fixed_costs_high[i])
        for j in range(len(markets)):
            objective.SetCoefficient(x[i, j], variable_costs[i][j])
    objective.SetMinimization()
    
    # 4. 모델 최적화 풀이
    status = solver.Solve()
    
    # 5. 결과 출력
    if status == pywraplp.Solver.OPTIMAL:
        print("최적해를 찾았습니다.\n")
        print(f"최소 총 비용: {int(objective.Value()):,} 원")
        print("-" * 50)
        
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

# 예제 3
from ortools.linear_solver import pywraplp

def solve_shortest_path():
    # 솔버 생성 (MIP)
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        print("SCIP 솔버를 사용할 수 없습니다.")
        return

    # 데이터 정의
    node_name = {0: 'O', 1: 'A', 2: 'B', 3: 'C', 4: 'D', 5: 'E', 6: 'T'}
    
    COSTS = {
        (0, 1): 2, (0, 2): 5, (0, 3): 4, 
        (1, 2): 2, (1, 4): 7, 
        (2, 3): 1, (2, 4): 4, (2, 5): 3, 
        (3, 2): 1, (3, 5): 4, 
        (4, 5): 1, (4, 6): 5, 
        (5, 4): 1, (5, 6): 7
    }
    
    # 각 노드별 순유량 (Flow Conservation)
    # [O, A, B, C, D, E, T]
    FLOW = [1, 0, 0, 0, 0, 0, -1]
    nNodes = len(FLOW)
    
    # 1. 의사결정변수 선언
    X = {}
    for key in COSTS.keys():
        # X[i, j]: 노드 i에서 j로 이동하면 1, 아니면 0
        X[key] = solver.IntVar(0, 1, "X[%i,%i]" % (key[0], key[1]))
        
    # 2. 제약조건 설정 (유량 보존)
    for i in range(nNodes):
        const_expr = []
        for key in COSTS.keys():
            if key[0] == i: # 해당 노드에서 나가는 트래픽 (Outgoing)
                const_expr.append(X[key])
            elif key[1] == i: # 해당 노드로 들어오는 트래픽 (Incoming)
                const_expr.append(-X[key])
                
        # 나가는 유량의 합 - 들어오는 유량의 합 = 순유량
        solver.Add(solver.Sum(const_expr) == FLOW[i], 'node_'+str(i))
        
    # 3. 목적함수 설정 (총 이동 비용 최소화)
    objective = solver.Objective()
    for key in COSTS.keys():
        objective.SetCoefficient(X[key], COSTS[key])
    objective.SetMinimization()
    
    # 4. 모델 최적화 풀이
    status = solver.Solve()
    
    # 5. 결과 출력
    if status == pywraplp.Solver.OPTIMAL:
        print("최적해를 찾았습니다.\n")
        print(f"최단 거리 (최소 비용): {int(objective.Value())}")
        print("-" * 40)
        print("선정된 최단 경로:")
        
        # 선택된 경로 추적
        current_node = 0 # 출발지 'O'
        while current_node != 6: # 도착지 'T'가 아닐 때까지 반복
            for key in COSTS.keys():
                if key[0] == current_node and X[key].solution_value() > 0.5:
                    print(f"  {node_name[key[0]]} -> {node_name[key[1]]} (비용: {COSTS[key]})")
                    current_node = key[1]
                    break
    else:
        print("최적해를 찾지 못했습니다.")

if __name__ == '__main__':
    solve_shortest_path()

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
    
    # 간선에 화살표가 없는 무방향 그래프이므로 양방향 간선을 모두 정의
    # (단, O로 들어오거나 T에서 나가는 불필요한 간선은 제외)
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
    
    # 각 노드별 순유량 (Origin: 1, Destination: -1, 경유지: 0)
    # [O, A, B, C, D, E, T]
    FLOW = [1, 0, 0, 0, 0, 0, -1]
    nNodes = len(FLOW)
    
    # 1. 의사결정변수 선언
    X = {}
    for key in COSTS.keys():
        # X[i, j]: 노드 i에서 j로 이동하면 1, 아니면 0
        X[key] = solver.IntVar(0, 1, "X[%i,%i]" % (key[0], key[1]))
        
    # 2. 제약조건 설정 (유량 보존의 법칙)
    for i in range(nNodes):
        const_expr = []
        for key in COSTS.keys():
            if key[0] == i: # 해당 노드에서 나가는 트래픽 (Outgoing)
                const_expr.append(X[key])
            elif key[1] == i: # 해당 노드로 들어오는 트래픽 (Incoming)
                const_expr.append(-X[key])
                
        # 나가는 유량의 합 - 들어오는 유량의 합 = 순유량
        solver.Add(solver.Sum(const_expr) == FLOW[i], 'node_'+str(i))
        
    # 3. 목적함수 설정 (총 이동 비용 최소화)
    objective = solver.Objective()
    for key in COSTS.keys():
        objective.SetCoefficient(X[key], COSTS[key])
    objective.SetMinimization()
    
    # 4. 모델 최적화 풀이
    status = solver.Solve()
    
    # 5. 결과 출력
    if status == pywraplp.Solver.OPTIMAL:
        print("최적해를 찾았습니다.\n")
        print(f"최단 거리 (최소 비용): {int(objective.Value())}")
        print("-" * 40)
        print("선정된 최단 경로:")
        
        # 선택된 경로 추적하여 출력
        current_node = 0 # 출발지 'O'
        while current_node != 6: # 도착지 'T'가 아닐 때까지 반복
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
    # 솔버 생성 (MIP)
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        print("SCIP 솔버를 사용할 수 없습니다.")
        return

    # 노드 매핑 (총 11개 노드)
    node_name = {
        0: 'O', 1: 'A', 2: 'B', 3: 'C', 4: 'D', 
        5: 'E', 6: 'F', 7: 'G', 8: 'H', 9: 'I', 10: 'T'
    }
    
    # 방향성이 있는 간선 (Directed Edge) 데이터 입력
    # (출발노드, 도착노드): 비용
    COSTS = {
        (0, 1): 4, (0, 3): 6, (0, 2): 3,  # O -> A, C, B
        (1, 4): 3, (1, 3): 5,             # A -> D, C
        (2, 3): 4, (2, 5): 6,             # B -> C, E
        (3, 4): 2, (3, 6): 2, (3, 5): 5,  # C -> D, F, E
        (4, 7): 4, (4, 6): 2,             # D -> G, F
        (5, 6): 1, (5, 8): 2, (5, 9): 5,  # E -> F, H, I
        (6, 7): 2, (6, 8): 5,             # F -> G, H
        (8, 7): 2,                        # H -> G
        (7, 10): 7,                       # G -> T
        (8, 10): 8,                       # H -> T
        (9, 8): 3, (9, 10): 4             # I -> H, T
    }
    
    # 각 노드별 순유량 (O: 1, T: -1, 나머지 경유지: 0)
    # [O, A, B, C, D, E, F, G, H, I, T]
    FLOW = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1]
    nNodes = len(FLOW)
    
    # 1. 의사결정변수 선언
    X = {}
    for key in COSTS.keys():
        X[key] = solver.IntVar(0, 1, f"X[{key[0]},{key[1]}]")
        
    # 2. 제약조건 설정 (유량 보존의 법칙)
    for i in range(nNodes):
        const_expr = []
        for key in COSTS.keys():
            if key[0] == i:   # 해당 노드에서 나가는 트래픽 (Outgoing)
                const_expr.append(X[key])
            elif key[1] == i: # 해당 노드로 들어오는 트래픽 (Incoming)
                const_expr.append(-X[key])
                
        # 나가는 유량 - 들어오는 유량 = 순유량
        solver.Add(solver.Sum(const_expr) == FLOW[i], f'node_{i}')
        
    # 3. 목적함수 설정 (총 이동 비용 최소화)
    objective = solver.Objective()
    for key in COSTS.keys():
        objective.SetCoefficient(X[key], COSTS[key])
    objective.SetMinimization()
    
    # 4. 모델 최적화 풀이
    status = solver.Solve()
    
    # 5. 결과 출력
    if status == pywraplp.Solver.OPTIMAL:
        print("최적해를 찾았습니다.\n")
        print(f"최단 거리 (최소 비용): {int(objective.Value())}")
        print("-" * 40)
        print("선정된 최단 경로:")
        
        # 선택된 경로 추적하여 출력
        current_node = 0 # 출발지 'O'
        target_node = 10 # 도착지 'T'
        
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