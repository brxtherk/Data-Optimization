# 실습 5-1
# 1번
from ortools.linear_solver import pywraplp

UC = [0] + [10]*24
CAPA = [15,14,16,10,17,16,15,18]
SC = 100 # setup cost

solver = pywraplp.Solver.CreateSolver("SAT")

# 생산량
P = {}
for i in range(8):
    for j in range(1, 25):
        P[i, j] = solver.NumVar(0, solver.infinity(), "P"+str(i)+'_'+str(j))

# 재고량
I = {}
for i in range(8):
    for j in range(25):
        I[i, j] = solver.NumVar(0, solver.infinity(), "I"+str(i)+'_'+str(j))

# 셋업비용 발생여부
S = {}
for i in range(8):
    for j in range(1, 25):
        S[i, j] = solver.IntVar(0, 1, "S"+str(i)+'_'+str(j))

# 기계 가동 여부
Y = {}
for i in range(8):
    for j in range(1, 25):
        Y[i, j] = solver.IntVar(0, 1, "Y"+str(i)+'_'+str(j))

######### 재고제약
# 기계 0 – 6 재고
for i in range(7):
    for j in range(1,25):
        solver.Add(I[i,j] - I[i,j-1] - P[i,j] + P[i+1,j] == 0, 'Inv_' +str(i)+str(j))
                   
# 기계 7 재고
for j in range(1,25):
    solver.Add(I[7,j] - I[7,j-1] - P[7,j] == 0, 'Inv_7'+str(j))

######### 초기재고
# 기계 0-6 초기 재고
for i in range(7):
    solver.Add(I[i,0] - 2 * CAPA[i+1] == 0,'init_inv_'+str(i)+'0')

#기계 7 초기 재고
solver.Add(I[7,0] == 0, 'init_inv_70')

###### 기말재고
# 기계 0 - 기계 6 기말 재고
for i in range(7):
    solver.Add(I[i,24] - 2 * CAPA[i+1] == 0, 'last_inv'+str(i)+'_24')
    #solver.Add(I[i,24] - CAPA[i+1] == 0, 'last_inv'+str(i)+'_24’)

# 기계 7 기말 재고 (= Throughput)
solver.Add(I[7, 24] == 240, 'last_inv_7_24')

# 재고에 의한 생산량 제약
# 기계 0은 재고에 의한 생산 제약이 없음.
for i in range(1, 8):
    for j in range(1, 25):
        solver.Add(P[i,j] - I[i-1,j-1] <= 0, 'prod_inv_'+str(i)+str(j))

# 생산용량에 의한 제약 - 가동여부
for i in range(8):
    for j in range(1, 25):
        solver.Add(P[i,j] - CAPA[i] * Y[i,j] <= 0, 'prod_capa_'+str(i)+str(j))

for i in range(8):
    for j in range(1, 25):
        solver.Add(P[i,j] - Y[i,j] >= 0, 'prod_capa2_'+str(i)+str(j))

###### 준비비용 발생 여부
for i in range(8):
    for j in range(2, 25):
        solver.Add(S[i,j] - Y[i,j] + Y[i,j-1] >= 0, 'setup_cost_'+str(i)+str(j))

# 첫 기간에 대한 준비 비용 발생여부
for i in range(8):
    solver.Add(S[i,1] - Y[i,1] == 0, 'setup_cost_'+str(i)+'1')

# Objective
objective_terms = []
for i in range(8):
    for j in range(1, 25):
        objective_terms.append(UC[j] * P[i,j] + SC * S[i, j])

solver.Minimize(solver.Sum(objective_terms))

status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL:

    for i in range(8):
        for j in range(1,25):
            print(f'P[{i},{j}] = {P[i,j].solution_value()}')

    print('Total cost =', solver.Objective().Value())
    
p_data = []
i_data = []
DEBUG = 0
# Print solution.
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:

    # 그래프 그리기 위한 데이터 정리
    for i in range(8):
        temp = []
        for j in range(1, 25):
            temp.append(P[i, j].solution_value())
        p_data.append(temp)

    for i in range(8):
        temp = []
        for j in range(25):
            temp.append(I[i, j].solution_value())
        i_data.append(temp)
    import matplotlib.pyplot as plt
    for i in range(8):
        plt.subplot(2, 4, i+1)
        plt.plot(p_data[i][1:], label = i)
        plt.legend()

    for i in range(8):
        plt.subplot(2, 4, i+1)
        plt.plot(i_data[i][1:], label=i)
        plt.legend()

plt.show()

# 2번
from ortools.linear_solver import pywraplp

UC_plans = [
    [0] + [5]*10 + [10]*2 + [15]*4 + [10]*4 + [5]*4, # UC1
    [0] + [5]*10 + [10]*2 + [20]*4 + [10]*4 + [5]*4, # UC2
    [0] + [5]*10 + [10]*2 + [25]*4 + [10]*4 + [5]*4  # UC3
]
CAPA = [15,14,16,10,17,16,15,18]
#CAPA = [15,14,16,16,17,16,15,18]
SC = 100 # setup cost

for idx, UC in enumerate(UC_plans):
    solver = pywraplp.Solver.CreateSolver("SAT")

    # 생산량
    P = {}
    for i in range(8):
        for j in range(1, 25):
            P[i, j] = solver.NumVar(0, solver.infinity(), "P"+str(i)+'_'+str(j))

    # 재고량
    I = {}
    for i in range(8):
        for j in range(25):
            I[i, j] = solver.NumVar(0, solver.infinity(), "I"+str(i)+'_'+str(j))

    # 셋업비용 발생여부
    S = {}
    for i in range(8):
        for j in range(1, 25):
            S[i, j] = solver.IntVar(0, 1, "S"+str(i)+'_'+str(j))

    # 기계 가동 여부
    Y = {}
    for i in range(8):
        for j in range(1, 25):
            Y[i, j] = solver.IntVar(0, 1, "Y"+str(i)+'_'+str(j))

    ######### 재고제약
    # 기계 0 – 6 재고
    for i in range(7):
        for j in range(1,25):
            solver.Add(I[i,j] - I[i,j-1] - P[i,j] + P[i+1,j] == 0, 'Inv_' +str(i)+str(j))
                    
    # 기계 7 재고
    for j in range(1,25):
        solver.Add(I[7,j] - I[7,j-1] - P[7,j] == 0, 'Inv_7'+str(j))

    ######### 초기재고
    # 기계 0-6 초기 재고
    for i in range(7):
        solver.Add(I[i,0] - 2 * CAPA[i+1] == 0,'init_inv_'+str(i)+'0')

    #기계 7 초기 재고
    solver.Add(I[7,0] == 0, 'init_inv_70')

    ###### 기말재고
    # 기계 0 - 기계 6 기말 재고
    for i in range(7):
        solver.Add(I[i,24] - 2 * CAPA[i+1] == 0, 'last_inv'+str(i)+'_24')
        #solver.Add(I[i,24] - CAPA[i+1] == 0, 'last_inv'+str(i)+'_24’)

    # 기계 7 기말 재고 (= Throughput)
    solver.Add(I[7, 24] == 240, 'last_inv_7_24')

    # 재고에 의한 생산량 제약
    # 기계 0은 재고에 의한 생산 제약이 없음.
    for i in range(1, 8):
        for j in range(1, 25):
            solver.Add(P[i,j] - I[i-1,j-1] <= 0, 'prod_inv_'+str(i)+str(j))

    # 생산용량에 의한 제약 - 가동여부
    for i in range(8):
        for j in range(1, 25):
            solver.Add(P[i,j] - CAPA[i] * Y[i,j] <= 0, 'prod_capa_'+str(i)+str(j))

    for i in range(8):
        for j in range(1, 25):
            solver.Add(P[i,j] - Y[i,j] >= 0, 'prod_capa2_'+str(i)+str(j))

    ###### 준비비용 발생 여부
    for i in range(8):
        for j in range(2, 25):
            solver.Add(S[i,j] - Y[i,j] + Y[i,j-1] >= 0, 'setup_cost_'+str(i)+str(j))

    # 첫 기간에 대한 준비 비용 발생여부
    for i in range(8):
        solver.Add(S[i,1] - Y[i,1] == 0, 'setup_cost_'+str(i)+'1')

    # Objective
    objective_terms = []
    for i in range(8):
        for j in range(1, 25):
            objective_terms.append(UC[j] * P[i,j] + SC * S[i, j])

    solver.Minimize(solver.Sum(objective_terms))

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print('\n', "-" * 30)
        print(f'UC{idx+1}')
        for i in range(8):
            for j in range(1,25):
                print(f'P[{i},{j}] = {P[i,j].solution_value()}')

        print('Total cost =', solver.Objective().Value())
        
    p_data = []
    i_data = []
    DEBUG = 0
    # Print solution.
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:

        # 그래프 그리기 위한 데이터 정리
        for i in range(8):
            temp = []
            for j in range(1, 25):
                temp.append(P[i, j].solution_value())
            p_data.append(temp)

        for i in range(8):
            temp = []
            for j in range(25):
                temp.append(I[i, j].solution_value())
            i_data.append(temp)
        import matplotlib.pyplot as plt
        for i in range(8):
            plt.subplot(2, 4, i+1)
            plt.plot(p_data[i][1:], label = i)
            plt.legend()

        for i in range(8):
            plt.subplot(2, 4, i+1)
            plt.plot(i_data[i][1:], label=i)
            plt.legend()

    plt.show()

print(f"UC1 요금제: 12360, UC2 요금제: 12700, UC3 요금제: 13030으로 UC1 요금제가 가장\
싸기 때문에 이 회사 입장에서는 UC1 요금제를 택하는 것이 가장 유리하다.")
      
# 3번
from ortools.linear_solver import pywraplp

UC = [0] + [5]*9 + [25]*7 + [5]*8
#CAPA = [15,14,16,10,17,16,15,18]
CAPA = [15,14,16,16,17,16,15,18]  # 기계 3 생산용량 10 -> 16
SC = 100 # setup cost

solver = pywraplp.Solver.CreateSolver("SAT")

# 생산량
P = {}
for i in range(8):
    for j in range(1, 25):
        P[i, j] = solver.NumVar(0, solver.infinity(), "P"+str(i)+'_'+str(j))

# 재고량
I = {}
for i in range(8):
    for j in range(25):
        I[i, j] = solver.NumVar(0, solver.infinity(), "I"+str(i)+'_'+str(j))

# 셋업비용 발생여부
S = {}
for i in range(8):
    for j in range(1, 25):
        S[i, j] = solver.IntVar(0, 1, "S"+str(i)+'_'+str(j))

# 기계 가동 여부
Y = {}
for i in range(8):
    for j in range(1, 25):
        Y[i, j] = solver.IntVar(0, 1, "Y"+str(i)+'_'+str(j))

######### 재고제약
# 기계 0 – 6 재고
for i in range(7):
    for j in range(1,25):
        solver.Add(I[i,j] - I[i,j-1] - P[i,j] + P[i+1,j] == 0, 'Inv_' +str(i)+str(j))
                   
# 기계 7 재고
for j in range(1,25):
    solver.Add(I[7,j] - I[7,j-1] - P[7,j] == 0, 'Inv_7'+str(j))

######### 초기재고
# 기계 0-6 초기 재고
for i in range(7):
    solver.Add(I[i,0] - 2 * CAPA[i+1] == 0,'init_inv_'+str(i)+'0')

#기계 7 초기 재고
solver.Add(I[7,0] == 0, 'init_inv_70')

###### 기말재고
# 기계 0 - 기계 6 기말 재고
for i in range(7):
    solver.Add(I[i,24] - 2 * CAPA[i+1] == 0, 'last_inv'+str(i)+'_24')
    #solver.Add(I[i,24] - CAPA[i+1] == 0, 'last_inv'+str(i)+'_24’)

# 기계 7 기말 재고 (= Throughput)
solver.Add(I[7, 24] == 336, 'last_inv_7_24')  # 전체 Throughput 240 -> 336

# 재고에 의한 생산량 제약
# 기계 0은 재고에 의한 생산 제약이 없음.
for i in range(1, 8):
    for j in range(1, 25):
        solver.Add(P[i,j] - I[i-1,j-1] <= 0, 'prod_inv_'+str(i)+str(j))

# 생산용량에 의한 제약 - 가동여부
for i in range(8):
    for j in range(1, 25):
        solver.Add(P[i,j] - CAPA[i] * Y[i,j] <= 0, 'prod_capa_'+str(i)+str(j))

for i in range(8):
    for j in range(1, 25):
        solver.Add(P[i,j] - Y[i,j] >= 0, 'prod_capa2_'+str(i)+str(j))

###### 준비비용 발생 여부
for i in range(8):
    for j in range(2, 25):
        solver.Add(S[i,j] - Y[i,j] + Y[i,j-1] >= 0, 'setup_cost_'+str(i)+str(j))

# 첫 기간에 대한 준비 비용 발생여부
for i in range(8):
    solver.Add(S[i,1] - Y[i,1] == 0, 'setup_cost_'+str(i)+'1')

# Objective
objective_terms = []
for i in range(8):
    for j in range(1, 25):
        objective_terms.append(UC[j] * P[i,j] + SC * S[i, j])

solver.Minimize(solver.Sum(objective_terms))

status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL:
    print('\n', '-'*30)
    for i in range(8):
        for j in range(1,25):
            print(f'P[{i},{j}] = {P[i,j].solution_value()}')

    print('Total cost =', solver.Objective().Value())
    
p_data = []
i_data = []
DEBUG = 0
# Print solution.
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:

    # 그래프 그리기 위한 데이터 정리
    for i in range(8):
        temp = []
        for j in range(1, 25):
            temp.append(P[i, j].solution_value())
        p_data.append(temp)

    for i in range(8):
        temp = []
        for j in range(25):
            temp.append(I[i, j].solution_value())
        i_data.append(temp)
    import matplotlib.pyplot as plt
    for i in range(8):
        plt.subplot(2, 4, i+1)
        plt.plot(p_data[i][1:], label = i)
        plt.legend()

    for i in range(8):
        plt.subplot(2, 4, i+1)
        plt.plot(i_data[i][1:], label=i)
        plt.legend()

plt.show()

# 실습 5-2
from ortools.linear_solver import pywraplp

UC = [0] + [5]*6 + [10]*3 + [15]*4 + [25]*3 + [15]*3 + [10]*3 + [5]*2
CAPA = [12, 8, 15, 5, 15]
SC = 100 # setup cost

solver = pywraplp.Solver.CreateSolver("SAT")

# 생산량
P = {}
for i in range(5):
    for j in range(1, 25):
        P[i, j] = solver.NumVar(0, solver.infinity(), "P"+str(i)+'_'+str(j))

# 재고량
I = {}
for i in range(5):
    for j in range(25):
        I[i, j] = solver.NumVar(0, solver.infinity(), "I"+str(i)+'_'+str(j))

# 셋업비용 발생여부
S = {}
for i in range(5):
    for j in range(1, 25):
        S[i, j] = solver.IntVar(0, 1, "S"+str(i)+'_'+str(j))

# 기계 가동 여부
Y = {}
for i in range(5):
    for j in range(1, 25):
        Y[i, j] = solver.IntVar(0, 1, "Y"+str(i)+'_'+str(j))

######### 재고제약
for j in range(1,25):
    # A라인: A1(0) -> A2(1) -> C(4)
    solver.Add(I[0,j] - I[0,j-1] - P[0,j] + P[1,j] == 0)
    solver.Add(I[1,j] - I[1,j-1] - P[1,j] + P[4,j] == 0)
    
    # B라인: B1(2) -> B2(3) -> C(4)
    solver.Add(I[2,j] - I[2,j-1] - P[2,j] + P[3,j] == 0)
    solver.Add(I[3,j] - I[3,j-1] - P[3,j] + P[4,j] == 0)
    
    # C라인 (완제품): C(4) -> 끝
    solver.Add(I[4,j] - I[4,j-1] - P[4,j] == 0)

######### 초기재고
solver.Add(I[0,0] - 2 * CAPA[1] == 0) # A1 다음은 A2(1)
solver.Add(I[1,0] - 2 * CAPA[4] == 0) # A2 다음은 C(4)
solver.Add(I[2,0] - 2 * CAPA[3] == 0) # B1 다음은 B2(3)
solver.Add(I[3,0] - 2 * CAPA[4] == 0) # B2 다음은 C(4)
solver.Add(I[4,0] == 0)               # C 초기재고 0

###### 기말재고
solver.Add(I[0,24] - 2 * CAPA[1] == 0)
solver.Add(I[1,24] - 2 * CAPA[4] == 0)
solver.Add(I[2,24] - 2 * CAPA[3] == 0)
solver.Add(I[3,24] - 2 * CAPA[4] == 0)
solver.Add(I[4, 24] == 120) # B2가 시간당 5개라 120개가 최대 병목

# 재고에 의한 생산량 제약
for j in range(1, 25):
    solver.Add(P[1,j] - I[0,j-1] <= 0) # A2는 A1 재고 필요
    solver.Add(P[3,j] - I[2,j-1] <= 0) # B2는 B1 재고 필요
    solver.Add(P[4,j] - I[1,j-1] <= 0) # C는 A2 재고 필요
    solver.Add(P[4,j] - I[3,j-1] <= 0) # C는 B2 재고도 필요 (동시 만족)

# 생산용량에 의한 제약 - 가동여부
for i in range(5):
    for j in range(1, 25):
        solver.Add(P[i,j] - CAPA[i] * Y[i,j] <= 0, 'prod_capa_'+str(i)+str(j))

for i in range(5):
    for j in range(1, 25):
        solver.Add(P[i,j] - Y[i,j] >= 0, 'prod_capa2_'+str(i)+str(j))

###### 준비비용 발생 여부
for i in range(5):
    for j in range(2, 25):
        solver.Add(S[i,j] - Y[i,j] + Y[i,j-1] >= 0, 'setup_cost_'+str(i)+str(j))

# 첫 기간에 대한 준비 비용 발생여부
for i in range(5):
    solver.Add(S[i,1] - Y[i,1] == 0, 'setup_cost_'+str(i)+'1')

# Objective
objective_terms = []
for i in range(5):
    for j in range(1, 25):
        objective_terms.append(UC[j] * P[i,j] + SC * S[i, j])

solver.Minimize(solver.Sum(objective_terms))

status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL:
    print("-" * 30)
    print('실습 5-2 운영계획')
    for i in range(5):
        for j in range(1,25):
            print(f'P[{i},{j}] = {P[i,j].solution_value()}')

    print('Total cost =', solver.Objective().Value())
    
p_data = []
i_data = []
DEBUG = 0
# Print solution.
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:

    # 그래프 그리기 위한 데이터 정리
    for i in range(5):
        temp = []
        for j in range(1, 25):
            temp.append(P[i, j].solution_value())
        p_data.append(temp)

    for i in range(5):
        temp = []
        for j in range(25):
            temp.append(I[i, j].solution_value())
        i_data.append(temp)
    import matplotlib.pyplot as plt
    for i in range(5):
        plt.subplot(2, 4, i+1)
        plt.plot(p_data[i][1:], label = i)
        plt.legend()

    for i in range(5):
        plt.subplot(2, 4, i+1)
        plt.plot(i_data[i][1:], label=i)
        plt.legend()

plt.show()