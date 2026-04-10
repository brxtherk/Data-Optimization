#예제1
def create_model():
    data={}
    data['cost']=[[1675, 400, 685, 1630 ,1160, 2800],
       [1460, 1940, 970, 100, 495, 1200],
       [1925, 2400, 1425, 500, 950, 800],
       [380, 1355, 543, 1045, 665 ,2321],
        [922, 1646, 700 ,508, 311 ,1797]
        ]
    data['ware']=['A','B','C','D','E']
    data['region']=6
    data['require']=[10,8,12,6,7,11]
    data['supply']=[18,24,27,22,31]
    data['fixed']=[7650,3500,3500,4100,2200]
    return data

from ortools.linear_solver import pywraplp
solver=pywraplp.Solver.CreateSolver('SCIP')
def main():
    data=create_model()
    x={}
    y={}
    for i in range(len(data['ware'])):
        y[i]=solver.BoolVar(data['ware'][i])
        for j in range(data['region']):
            x[i,j]=solver.NumVar(0,solver.infinity(),f'x[{i},{j}]')
    for i in range(len(data['ware'])):
        solver.Add(sum(x[i,j] for j in range(data['region']))<=data['supply'][i]*y[i])
    for j in range(data['region']):
        solver.Add(sum(x[i,j] for i in range(len(data['ware'])))>=data['require'][j])
    
    obj=[]
    for i in range(len(data['ware'])):
        obj.append(data['fixed'][i]*y[i])
        for j in range(data['region']):
            obj.append(data['cost'][i][j]*x[i,j])
    solver.Minimize(sum(obj))
    status=solver.Solve()
    if status==pywraplp.Solver.OPTIMAL:
        print(f'Total cost: {solver.Objective().Value()}')
        for i in range(len(data['ware'])):
            if y[i].solution_value()==1:
                print(y[i].name(),': 창고 건설')
if __name__=='__main__':
    main()

#연습문제1
def create_model():
    data={}
    data['cost']=[[67,16,27,65,46,112],
                  [58,78,39,4,20,48],
                  [17,96,57,20,38,32],
                  [15,54,22,42,27,93],
                  [37,66,28,20,12,72]]
    data['fac']=5
    data['ware']=6
    data['supply']=[18,24,27,22,31]
    data['require']=[10,8,12,6,7,11]
    data['fixed']=[306,140,200,164,88]
    data['past']=[[0,8,0,0,0,0],
                  [0,0,0,6,0,0],
                  [0,0,0,0,0,11],
                  [10,0,12,0,0,0],
                  [0,0,0,0,7,0]]
    
    return data
def main():
    from ortools.linear_solver import pywraplp
    solver=pywraplp.Solver.CreateSolver('SCIP')
    data=create_model()
    x={}
    y={}
    for i in range(data['fac']):
        y[i]=solver.BoolVar('y[%i]'%i)
        for j in range(data['ware']):
            x[i,j]=solver.NumVar(0,solver.infinity(),f'x[{i},{j}]')
    for i in range(data['fac']):
        solver.Add(sum(x[i,j] for j in range(data['ware']))<=data['supply'][i]*y[i])
    for j in range(data['ware']):
        solver.Add(sum(x[i,j] for i in range(data['fac']))>=data['require'][j])
    obj=[]
    past=[]
    for i in range(data['fac']):
        obj.append(y[i]*data['fixed'][i])
        past.append(data['fixed'][i])
        for j in range(data['ware']):
            obj.append(x[i,j]*data['cost'][i][j])
            past.append(data['past'][i][j]*data['cost'][i][j])
    solver.Minimize(sum(obj))
    status=solver.Solve()
    if status==pywraplp.Solver.OPTIMAL:
        print(f'Total cost: {solver.Objective().Value()}')
        print(f'과거 총 비용: {sum(past)}')
        if sum(past)>=solver.Objective().Value():
            print(f'고정 운영비의 감소가 {sum(past)-solver.Objective().Value()} 더 이득이다')
        for i in range(data['fac']):
            if y[i].solution_value()==0:
                print(y[i].name(),': 공장%i 폐쇄'%(i+1))
        for i in range(data['fac']):
            for j in range(data['ware']):
                if x[i,j].solution_value() >0:
                    print(x[i,j].name(),':',x[i,j].solution_value())
if __name__=='__main__':
    main()       

#예제2
def create_model():
    data={}
    data['cost']=[[81,92,101,130,115],
                  [117,77,108,98,100],
                  [102,105,95,119,111],
                  [115,125,90,59,74],
                  [142,100,103,105,71]
    ]
    data['contry']=['북미','남미','유럽','아시아','아프리카']
    data['require']=[12,8,14,16,7]
    data['low_F']=[6000,4500,6500,4100,4000]
    data['low_cap']=10
    data['high_F']=[9000,6750,9750,6150,6000]
    data['high_cap']=20
    return data
def main():
    from ortools.linear_solver import pywraplp
    solver=pywraplp.Solver.CreateSolver('SCIP')
    data=create_model()
    x={}
    y={}
    z={}
    L=len(data['contry'])
    for i in range(L):
        y[i]=solver.BoolVar(data['contry'][i])
        z[i]=solver.BoolVar('z[%i]'%i)
        for j in range(L):
            x[i,j]=solver.IntVar(0,solver.infinity(),data['contry'][i]+str('로부터 ')+data['contry'][j])
    for i in range(L):
        #z값이 0이면 고생산공장, 1이면 저생산공장 
        solver.Add(z[i]<=y[i])
        total_supply = solver.Sum(x[i, j] for j in range(L))
        solver.Add(total_supply <= data['low_cap'] * z[i] + data['high_cap'] * (y[i] - z[i]))
    for j in range(L):
        solver.Add(sum(x[i,j] for i in range(L))>=data['require'][j])
    obj=[]
    for i in range(L):
        obj.append(data['low_F'][i] * z[i])
        obj.append(data['high_F'][i] * y[i])
        obj.append(-data['high_F'][i] * z[i])
        for j in range(L):
            obj.append(x[i,j]*data['cost'][i][j])
    solver.Minimize(sum(obj))
    status=solver.Solve()
    if status==pywraplp.Solver.OPTIMAL:
        print(f'Total cost: {solver.Objective().Value()}')
        for i in range(L):
            if y[i].solution_value()==1:
                if z[i].solution_value()==0:
                    print(y[i].name(),': 고 생산 공장 건설')
                else:
                    print(y[i].name(),': 저 생산 공장 건설')
        for i in range(L):
            for j in range(L):
                if x[i,j].solution_value()!=0:
                    print(x[i,j].name(),':',x[i,j].solution_value())
if __name__=='__main__':
    main()    

#연습문제2
def create_model():
    data = {}
    
    data['cost'] = [
        [23, 9, 23, 29, 33],   
        [19, 15, 21, 26, 36],  
        [31, 11, 40, 40, 20]   
    ]

    data['plants'] = ['루마니아', '폴란드', '아일랜드']
    data['markets'] = ['프랑스', '독일', '이탈리아', '스페인', '영국']
    data['demand'] = [15000, 20000, 13000, 12000, 19000]
    data['capacity'] = [40000, 40000, 40000]
    data['fixed'] = [18000000,17500000,24500000]
    data['type']='basic'
    return data
def create_model_modified():
    data = {}
    
    data['cost'] = [
        [23, 9, 23, 29, 33],   
        [19, 15, 21, 26, 36],  
        [31, 11, 40, 40, 20]   
    ]

    data['plants'] = ['루마니아', '폴란드', '아일랜드']
    data['markets'] = ['프랑스', '독일', '이탈리아', '스페인', '영국']
    data['demand'] = [15000, 40000, 13000, 12000, 19000]
    data['cap_low'] = [40000, 40000, 40000]
    data['fixed_low'] = [18000000,17500000,24500000]
    data['cap_high'] = [60000,60000,60000]
    data['fixed_high']=[23400000,22750000,31850000]
    data['type']='extended'


    return data
def main(data):
    from ortools.linear_solver import pywraplp
    solver=pywraplp.Solver.CreateSolver('SCIP')
    x={}
    y={}
    z={}
    candidate=len(data['plants'])
    Europe=len(data['markets'])
    for i in range(candidate):
        y[i]=solver.BoolVar(data['plants'][i])
        z[i]=solver.BoolVar('z[%i]'%i)
        for j in range(Europe):
            x[i,j]=solver.IntVar(0,solver.infinity(),data['plants'][i]+str('로부터 ')+data['markets'][j])

    for j in range(Europe):
        solver.Add(sum(x[i,j] for i in range(candidate))>=data['demand'][j])
    obj=[]
    if data['type']=='basic':
        for i in range(candidate):
            solver.Add(sum(x[i,j] for j in range(Europe))<=y[i]*data['capacity'][i])
        for i in range(candidate):
            obj.append(data['fixed'][i]*y[i])
            for j in range(Europe):
                obj.append(x[i,j]*data['cost'][i][j])
    if data['type']=='extended':
        for i in range(candidate): 
            solver.Add(y[i]>=z[i])
           #z가 0이면 고용량 공장, z가 1이면 저용량공장
            solver.Add(sum(x[i,j] for j in range(Europe))<=z[i]*data['cap_low'][i]+(y[i]-z[i])*data['cap_high'][i])

        for i in range(candidate):
            obj.append(data['fixed_low'][i]*z[i])
            obj.append(data['fixed_high'][i]*(y[i]-z[i]))
            for j in range(Europe):
                obj.append(x[i,j]*data['cost'][i][j])


    solver.Minimize(sum(obj))
    status=solver.Solve()
    if status==pywraplp.Solver.OPTIMAL:
        print(f'Total cost: {solver.Objective().Value()}')
        for i in range(candidate):
            if y[i].solution_value()==1:
                print(y[i].name(),' 선정')
        for i in range(candidate):
            for j in range(Europe):
                if x[i,j].solution_value() >0:
                    print(x[i,j].name(),':',x[i,j].solution_value())
if __name__=='__main__':
    print('예제2-1')
    main(create_model())
    print('\n예제2-2')
    main(create_model_modified())

#예제3
from ortools.linear_solver import pywraplp

def main():
    # 노드 정의
    node_name = {0: 'O', 1: 'A', 2: 'B', 3: 'C', 4: 'D', 5: 'E', 6: 'T'}
    
    # 간선별 비용 (단방향)
    COSTS = {
        (0, 1): 2, (0, 2): 5,
        (1, 3): 4, (1, 2): 2, (1, 4): 7,
        (2, 3): 1, (2, 4): 4,
        (3, 2): 1, (3, 5): 4,
        (4, 5): 1, (4, 6): 5,
        (5, 4): 1, (5, 6): 7
    }

    # 각 노드에서의 유량 균형 (출발지=+1, 도착지=-1, 나머지는 0)
    FLOW = [1, 0, 0, 0, 0, 0, -1]

    nNodes = len(FLOW)

    # Solver 초기화
    solver = pywraplp.Solver.CreateSolver('SCIP')

    # 변수 생성
    X = {}
    for key in COSTS.keys():
        X[key] = solver.IntVar(0, 1, f"X[{key[0]},{key[1]}]")

    # 제약 조건: 각 노드의 유량 균형
    for i in range(nNodes):
        const_expr = []
        for key in COSTS.keys():
            if key[0] == i:  # incoming traffic
                const_expr.append(X[key])
            elif key[1] == i:  # outgoing traffic
                const_expr.append(-X[key])
        solver.Add(solver.Sum(const_expr) == FLOW[i], 'node_' + str(i))


    # 목적함수: 전체 비용 최소화
    solver.Minimize(solver.Sum(COSTS[key] * X[key] for key in COSTS.keys()))

    # 풀이
    status = solver.Solve()

    # 출력
    if status == pywraplp.Solver.OPTIMAL:
        print(f"최소 비용: {solver.Objective().Value()}")
        print("선택된 경로:")
        for (u, v) in COSTS.keys():
            if X[(u, v)].solution_value() > 0.5:
                print(f"  {node_name[u]} -> {node_name[v]}")
    else:
        print("최적해를 찾을 수 없습니다.")

if __name__ == "__main__":
    main()

#연습문제3
from ortools.linear_solver import pywraplp

def main():
    # 노드 정의
    node_name = {0: 'O', 1: 'A', 2: 'B', 3: 'C', 4: 'D', 5: 'E', 6: 'F',7:'G',8:'H',9:'I',10:'T'}
    
    # 간선별 비용 (단방향)
    COSTS = {
        (0, 1): 4, (0, 2): 3,(0,3):6,
        (1, 3): 5, (1,4): 3, (2, 3): 4,
        (2,5): 6, (3, 4): 2,(3,5):5,(3,6):2,
        (4, 6): 2, (4, 7): 4,
        (5, 6): 1, (5, 8): 2,(5,9):5,
        (6, 7): 2, (6, 8): 5,
        (7,10):7,(8,7):2,(8,10):8,
        (9,8):3,(9,10):4
    }

    # 각 노드에서의 유량 균형 (출발지=+1, 도착지=-1, 나머지는 0)
    FLOW = [1,0, 0, 0, 0, 0, 0,0,0,-1]

    nNodes = len(FLOW)

    # Solver 초기화
    solver = pywraplp.Solver.CreateSolver('SCIP')

    # 변수 생성
    X = {}
    for key in COSTS.keys():
        X[key] = solver.IntVar(0, 1, f"X[{key[0]},{key[1]}]")

    # 제약 조건: 각 노드의 유량 균형
    for i in range(nNodes):
        const_expr = []
        for key in COSTS.keys():
            if key[0] == i:  # incoming traffic
                const_expr.append(X[key])
            elif key[1] == i:  # outgoing traffic
                const_expr.append(-X[key])
        solver.Add(solver.Sum(const_expr) == FLOW[i], 'node_' + str(i))


    # 목적함수: 전체 비용 최소화
    solver.Minimize(solver.Sum(COSTS[key] * X[key] for key in COSTS.keys()))

    # 풀이
    status = solver.Solve()

    # 출력
    if status == pywraplp.Solver.OPTIMAL:
        print(f"최소 비용: {solver.Objective().Value()}")
        print("선택된 경로:")
        for (u, v) in COSTS.keys():
            if X[(u, v)].solution_value() > 0.5:
                print(f"  {node_name[u]} -> {node_name[v]}")
    else:
        print("최적해를 찾을 수 없습니다.")

if __name__ == "__main__":
    main()

