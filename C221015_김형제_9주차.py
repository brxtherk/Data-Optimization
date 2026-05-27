# 예제 1
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

def create_data_model():
    """Stores the data for the problem."""
    data = {}
    data["distance_matrix"] = [
    [0, 2451, 713, 1018, 1631, 1374, 2408, 213, 2571, 875, 1420, 2145, 1972],
    [2451, 0, 1745, 1524, 831, 1240, 959, 2596, 403, 1589, 1374, 357, 579],
    [713, 1745, 0, 355, 920, 803, 1737, 851, 1858, 262, 940, 1453, 1260],
    [1018, 1524, 355, 0, 700, 862, 1395, 1123, 1584, 466, 1056, 1280, 987],
    [1631, 831, 920, 700, 0, 663, 1021, 1769, 949, 796, 879, 586, 371],
    [1374, 1240, 803, 862, 663, 0, 1681, 1551, 1765, 547, 225, 887, 999],
    [2408, 959, 1737, 1395, 1021, 1681, 0, 2493, 678, 1724, 1891, 1114, 701],
    [213, 2596, 851, 1123, 1769, 1551, 2493, 0, 2699, 1038, 1605, 2300, 2099],
    [2571, 403, 1858, 1584, 949, 1765, 678, 2699, 0, 1744, 1645, 653, 600],
    [875, 1589, 262, 466, 796, 547, 1724, 1038, 1744, 0, 679, 1272, 1162],
    [1420, 1374, 940, 1056, 879, 225, 1891, 1605, 1645, 679, 0, 1017, 1200],
    [2145, 357, 1453, 1280, 586, 887, 1114, 2300, 653, 1272, 1017, 0, 504],
    [1972, 579, 1260, 987, 371, 999, 701, 2099, 600, 1162, 1200, 504, 0],
    ]
    data["num_vehicles"] = 1
    data["depot"] = 0
    return data

data = create_data_model()
# 색인 관리자, 일종의 정보관리자
manager = pywrapcp.RoutingIndexManager(
len(data["distance_matrix"]), data["num_vehicles"], data["depot"]
)
# Routing 객체 생성
routing = pywrapcp.RoutingModel(manager)
# 두 점 사이의 거리를 반환한다.
def distance_callback(from_index, to_index):
    # Convert from routing variable Index to distance matrix NodeIndex.
    from_node = manager.IndexToNode(from_index)
    to_node = manager.IndexToNode(to_index)
    return data["distance_matrix"][from_node][to_node]
                
# 거리 계산 함수를 callback 함수로 등록하고 활용함.
transit_callback_index = routing.RegisterTransitCallback(distance_callback)
routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

# 시작해를 찾기 위한 휴리스틱 메소드를 등록
search_parameters = pywrapcp.DefaultRoutingSearchParameters()
search_parameters.first_solution_strategy = (
routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
)

def print_solution(manager, routing, solution):
    """콘솔에 해 출력"""
    print(f"Objective: {solution.ObjectiveValue()} miles")
    index = routing.Start(0)
    plan_output = "Route for vehicle 0:\n"
    route_distance = 0
    while not routing.IsEnd(index):
        plan_output += f" {manager.IndexToNode(index)} ->"
        previous_index = index
        index = solution.Value(routing.NextVar(index))
        route_distance += routing.GetArcCostForVehicle(previous_index, index, 0)
    plan_output += f" {manager.IndexToNode(index)}\n"
    print(plan_output)
    plan_output += f"Route distance: {route_distance}miles\n"

# 문제 풀이
solution = routing.SolveWithParameters(search_parameters)
if solution:
    print_solution(manager, routing, solution)

# 해 경로를 리스트에 저장하기 (Optional)
def get_routes(solution, routing, manager):
    """Get vehicle routes from a solution and store them in an array."""
    # Get vehicle routes and store them in a two dimensional array whose
    # i,j entry is the jth location visited by vehicle i along its route.
    routes = []
    for route_nbr in range(routing.vehicles()):
        index = routing.Start(route_nbr)
        route = [manager.IndexToNode(index)]
        while not routing.IsEnd(index):
            index = solution.Value(routing.NextVar(index))
            route.append(manager.IndexToNode(index))
        routes.append(route)
    return routes

routes = get_routes(solution, routing, manager)
# Display the routes.
for i, route in enumerate(routes):
    print('Route', i, route)


# 예제 2
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import math
import pandas as pd

def makeDIST(nP):
    DIST = list()
    nCity = len(nP)

    for i in range(nCity):
        DIST.append([])
        for j in range(nCity):
            if j != i:
                # Euclidean Distance
                temp = math.hypot(nP['xc'][i] - nP['xc'][j], nP['yc'][i] - nP['yc'][j])
                DIST[i].append(int(temp))
            else:
                DIST[i].append(0)
    return DIST

def create_data_model(DIST):
    """Stores the data for the problem."""
    data = {}
    data["distance_matrix"] = DIST
    data["num_vehicles"] = 1
    data["depot"] = 0
    return data

def print_solution(manager, routing, solution):
    """Prints solution on console."""
    print(f"Objective: {solution.ObjectiveValue()} miles")
    index = routing.Start(0)
    plan_output = "Route for vehicle 0:\n"
    route_distance = 0
    while not routing.IsEnd(index):
        plan_output += f" {manager.IndexToNode(index)} ->"
        previous_index = index
        index = solution.Value(routing.NextVar(index))
        route_distance += routing.GetArcCostForVehicle(previous_index, index, 0)
    plan_output += f" {manager.IndexToNode(index)}\n"
    print(plan_output)
    plan_output += f"Route distance: {route_distance}miles\n"

# Main Flow
f = open(".\\TSP_data\\a280.tsp", 'r') # 기판
nPos = pd.DataFrame(columns=[ 'xc', 'yc'])

flag = 0
while True:
    line = f.readline().strip()
    if line == "EOF": break

    if line == "NODE_COORD_SECTION":
        flag = 1
        continue

    if flag:
        ss = line.split()
        nPos.loc[len(nPos)] = [float(ss[1]), float((ss[2]))]

f.close()

# Draw a picture
import matplotlib.pyplot as plt
import numpy as np

plt.scatter(nPos['xc'], nPos['yc'])
plt.show()

DIST = makeDIST(nPos)

data = create_data_model(DIST)

manager = pywrapcp.RoutingIndexManager(
len(data["distance_matrix"]), data["num_vehicles"], data["depot"]
)

# Create Routing Model.
routing = pywrapcp.RoutingModel(manager)

def distance_callback(from_index, to_index):
    from_node = manager.IndexToNode(from_index)
    to_node = manager.IndexToNode(to_index)
    return data["distance_matrix"][from_node][to_node]

transit_callback_index = routing.RegisterTransitCallback(distance_callback)

routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

search_parameters = pywrapcp.DefaultRoutingSearchParameters()
search_parameters.first_solution_strategy = (
routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
)

solution = routing.SolveWithParameters(search_parameters)

# Print solution on console.
if solution:
    print_solution(manager, routing, solution)
#코드제출 3
#(2)번 문제는 capacity = 13->14 / data["num_vehicles"] = 3
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp


def create_data_model():
    """Stores the data for the problem."""
    data = {}
    data["distance_matrix"] = [


    [0, 10, 15, 20, 25, 30, 35],   # depot

    [10,  0, 12, 18, 22, 28, 32],  # A

    [15, 12,  0, 14, 18, 22, 28],  # B

    [20, 18, 14,  0, 10, 16, 22],  # C

    [25, 22, 18, 10,  0, 12, 18],  # D

    [30, 28, 22, 16, 12,  0, 14],  # E

    [35, 32, 28, 22, 18, 14,  0],  # F

]
    
    data["demands"] = [0, 3, 5, 4, 6, 2, 5]
    data["num_vehicles"] = 2
    capacity = 13
    data["vehicle_capacities"] = [capacity] * data["num_vehicles"]
    data["depot"] = 0
    return data


def print_solution(data, manager, routing, solution):
    """Prints solution on console."""
    print(f"Objective: {solution.ObjectiveValue()}")
    total_distance = 0
    total_load = 0
    for vehicle_id in range(data["num_vehicles"]):
        index = routing.Start(vehicle_id)
        plan_output = f"Route for vehicle {vehicle_id}:\n"
        route_distance = 0
        route_load = 0
        while not routing.IsEnd(index):
            node_index = manager.IndexToNode(index)
            route_load += data["demands"][node_index]
            plan_output += f" {node_index} Load({route_load}) -> "
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id
            )
        plan_output += f" {manager.IndexToNode(index)} Load({route_load})\n"
        plan_output += f"Distance of the route: {route_distance}m\n"
        plan_output += f"Load of the route: {route_load}\n"
        plan_output += f"트럭 적재율: {route_load/data['vehicle_capacities'][vehicle_id]*100:.2f}%\n"

        print(plan_output)
        total_distance += route_distance
        total_load += route_load
    print(f"Total distance of all routes: {total_distance}m")
    print(f"Total load of all routes: {total_load}")
    print(f"적재율: {total_load/sum(data['vehicle_capacities'])*100:.2f}%")



def main():
    """Solve the CVRP problem."""
    # Instantiate the data problem.
    data = create_data_model()

    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(
        len(data["distance_matrix"]), data["num_vehicles"], data["depot"]
    )

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)

    # Create and register a transit callback.
    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data["distance_matrix"][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Add Capacity constraint.
    def demand_callback(from_index):
        """Returns the demand of the node."""
        # Convert from routing variable Index to demands NodeIndex.
        from_node = manager.IndexToNode(from_index)
        return data["demands"][from_node]

    demand_callback_index = routing.RegisterUnaryTransitCallback(demand_callback)
    routing.AddDimensionWithVehicleCapacity(
        demand_callback_index,
        0,  # null capacity slack
        data["vehicle_capacities"],  # vehicle maximum capacities
        True,  # start cumul to zero
        "Capacity",
    )

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    )
    search_parameters.local_search_metaheuristic = (
        routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
    )
    search_parameters.time_limit.FromSeconds(1)

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)

    # Print solution on console.
    if solution:
        print_solution(data, manager, routing, solution)


if __name__ == "__main__":
    main()

#코드제출 4
# (2)번 문제는 data["num_vehicles"] = 5->2, data['cost_per_dist'] = [2, 2], data["vehicle_capacities"] = [20, 20]
# (3)번 문제는 data['cost_per_dist'] = [2, 2, 3, 3, 3]
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp


def create_data_model():
    """Stores the data for the problem."""
    data = {}
    data["distance_matrix"] = [

    [0, 10, 15, 20, 25, 30, 35],   # depot

    [10,  0, 12, 18, 22, 28, 32],  # A

    [15, 12,  0, 14, 18, 22, 28],  # B

    [20, 18, 14,  0, 10, 16, 22],  # C

    [25, 22, 18, 10,  0, 12, 18],  # D

    [30, 28, 22, 16, 12,  0, 14],  # E

    [35, 32, 28, 22, 18, 14,  0],  # F

]
    
    data["demands"] = [0, 3, 5, 4, 6, 2, 5]
    data['cost_per_dist'] = [2, 2, 1, 1, 1]   # 트럭2대=2, 밴3대=1
    data["num_vehicles"] = 5
    data["vehicle_capacities"] = [20, 20, 8, 8, 8]
    data["depot"] = 0
    return data


def print_solution(data, manager, routing, solution):
    """Prints solution on console."""
    print(f"Objective: {solution.ObjectiveValue()}")
    total_cost = 0
    total_load = 0
    for vehicle_id in range(data["num_vehicles"]):
        index = routing.Start(vehicle_id)
        plan_output = f"Route for vehicle {vehicle_id}:\n"
        route_cost = 0
        route_load = 0
        while not routing.IsEnd(index):
            node_index = manager.IndexToNode(index)
            route_load += data["demands"][node_index]
            plan_output += f" {node_index} Load({route_load}) -> "
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_cost += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id
            )
        plan_output += f" {manager.IndexToNode(index)} Load({route_load})\n"
        plan_output += f"Cost of the route: {route_cost}\n"
        plan_output += f"Load of the route: {route_load}\n"
        plan_output += f"트럭 적재율: {route_load/data['vehicle_capacities'][vehicle_id]*100:.2f}%\n"

        print(plan_output)
        total_cost += route_cost
        total_load += route_load
    print(f"Total distance of all routes: {total_cost}")
    print(f"Total load of all routes: {total_load}")
    print(f"적재율: {total_load/sum(data['vehicle_capacities'])*100:.2f}%")



def main():
    """Solve the CVRP problem."""
    # Instantiate the data problem.
    data = create_data_model()

    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(
        len(data["distance_matrix"]), data["num_vehicles"], data["depot"]
    )

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)

    cost_per_dist = data["cost_per_dist"]   # 트럭2대=2, 밴3대=1
    
    for v in range(data["num_vehicles"]):
        def make_cb(vid):
            def cb(fi, ti):
                fn = manager.IndexToNode(fi)
                tn = manager.IndexToNode(ti)
                return data["distance_matrix"][fn][tn] * cost_per_dist[vid]
            return cb
        idx = routing.RegisterTransitCallback(make_cb(v))
        routing.SetArcCostEvaluatorOfVehicle(idx, v)

    # Add Capacity constraint.
    def demand_callback(from_index):
        """Returns the demand of the node."""
        # Convert from routing variable Index to demands NodeIndex.
        from_node = manager.IndexToNode(from_index)
        return data["demands"][from_node]

    demand_callback_index = routing.RegisterUnaryTransitCallback(demand_callback)
    routing.AddDimensionWithVehicleCapacity(
        demand_callback_index,
        0,  # null capacity slack
        data["vehicle_capacities"],  # vehicle maximum capacities
        True,  # start cumul to zero
        "Capacity",
    )

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    )
    search_parameters.local_search_metaheuristic = (
        routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
    )
    search_parameters.time_limit.FromSeconds(1)

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)

    # Print solution on console.
    if solution:
        print_solution(data, manager, routing, solution)


if __name__ == "__main__":
    main()

# 코드제출 5
# (3)번 문제는 data["num_vehicles"] = 2->1
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp


def create_data_model():
    """Stores the data for the problem."""
    data = {}
    # 시간 행렬 (6×6, 단위: 분)

    data["time_matrix"] = [
    
        [0,  8, 12, 10,  6, 15],  # 약국(0)
    
        [8,  0,  7,  9,  5, 12],  # 내과(1)
    
        [12, 7,  0,  8, 10, 10],  # 외과(2)
    
        [10, 9,  8,  0,  7, 11],  # 소아과(3)
    
        [6,  5, 10,  7,  0,  9],  # 응급실(4)
    
        [15, 12, 10, 11,  9,  0], # 중환자실(5)
    
    ]
    
     
    
    data["time_windows"] = [
    
        (0, 120),   # 약국
    
        (20, 50),   # 내과
    
        (40, 80),   # 외과
    
        (60, 100),  # 소아과
    
        (0, 120),   # 응급실
    
        (10, 40),   # 중환자실  ← 가장 빡빡
    
    ]
    
    data["num_vehicles"] = 2
    data["depot"] = 0
    return data


def print_solution(data, manager, routing, solution):
    """Prints solution on console."""
    print(f"Objective: {solution.ObjectiveValue()}")
    time_dimension = routing.GetDimensionOrDie("Time")
    total_time = 0
    for vehicle_id in range(data["num_vehicles"]):
        index = routing.Start(vehicle_id)
        plan_output = f"Route for vehicle {vehicle_id}:\n"
        while not routing.IsEnd(index):
            time_var = time_dimension.CumulVar(index)
            plan_output += (
                f"{manager.IndexToNode(index)}"
                f" Time({solution.Min(time_var)},{solution.Max(time_var)})"
                " -> "
            )
            index = solution.Value(routing.NextVar(index))
        time_var = time_dimension.CumulVar(index)
        plan_output += (
            f"{manager.IndexToNode(index)}"
            f" Time({solution.Min(time_var)},{solution.Max(time_var)})\n"
        )
        plan_output += f"Time of the route: {solution.Min(time_var)}min\n"
        print(plan_output)
        total_time += solution.Min(time_var)
    print(f"Total time of all routes: {total_time}min")


def main():
    """Solve the VRP with time windows."""
    # Instantiate the data problem.
    data = create_data_model()

    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(
        len(data["time_matrix"]), data["num_vehicles"], data["depot"]
    )

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)

    # Create and register a transit callback.
    def time_callback(from_index, to_index):
        """Returns the travel time between the two nodes."""
        # Convert from routing variable Index to time matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data["time_matrix"][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(time_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Add Time Windows constraint.
    time = "Time"
    routing.AddDimension(
        transit_callback_index,
        120,
        120,  # 최대 근무 시간: 120분
        False,  # Don't force start cumul to zero.
        time,
    )
    time_dimension = routing.GetDimensionOrDie(time)
    # Add time window constraints for each location except depot.
    for location_idx, time_window in enumerate(data["time_windows"]):
        if location_idx == data["depot"]:
            continue
        index = manager.NodeToIndex(location_idx)
        time_dimension.CumulVar(index).SetRange(time_window[0], time_window[1])
    # Add time window constraints for each vehicle start node.
    depot_idx = data["depot"]
    for vehicle_id in range(data["num_vehicles"]):
        index = routing.Start(vehicle_id)
        time_dimension.CumulVar(index).SetRange(
            data["time_windows"][depot_idx][0], data["time_windows"][depot_idx][1]
        )

    # Instantiate route start and end times to produce feasible times.
    for i in range(data["num_vehicles"]):
        routing.AddVariableMinimizedByFinalizer(
            time_dimension.CumulVar(routing.Start(i))
        )
        routing.AddVariableMinimizedByFinalizer(time_dimension.CumulVar(routing.End(i)))

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    )

    TIMEOUT = 3
    search_parameters.time_limit.FromSeconds(TIMEOUT)

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)

    # Print solution on console.
    if solution:
        print_solution(data, manager, routing, solution)
    else:
        # status 확인
        status = routing.status()
        if status == 3:  # ROUTING_FAIL_TIMEOUT
            print(f"⏱  탐색 시간 {TIMEOUT} 초 초과 — 해를 찾지 못했습니다.")
        else:
            print("❌  해 없음 (infeasible) — 용량·제약 조건을 확인하세요.")


if __name__ == "__main__":
    main()

# 코드제출 6 (실습 1)
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

def create_data_model():
    data = {}
    # 6x6 거리(Setup 시간) 행렬
    # 인덱스: 0(더미/없음), 1(A), 2(B), 3(C), 4(D), 5(E)
    data["distance_matrix"] = [
        # 0   A   B   C   D   E  (도착)
        [ 0,  4,  5,  8,  9,  4], # 0 (더미: 시작) -> 각 작업 첫 Setup
        [ 0,  0,  7, 12, 10,  9], # A -> 더미로 돌아가는 비용은 0 (Open-tour)
        [ 0,  6,  0, 10, 14, 11], # B -> "
        [ 0, 10, 11,  0, 12, 10], # C -> "
        [ 0,  7,  8, 15,  0,  7], # D -> "
        [ 0, 12,  9,  8, 16,  0], # E -> "
    ]
    data["num_vehicles"] = 1
    data["depot"] = 0 # 더미 노드를 출발점(Depot)으로 설정
    return data

def print_solution(manager, routing, solution):
    """결과를 출력합니다."""
    print(f"Objective (최소 Setup 시간): {solution.ObjectiveValue()}")
    
    index = routing.Start(0)
    plan_output = "최적 작업 순서:\n"
    route_distance = 0
    
    while not routing.IsEnd(index):
        plan_output += f" {manager.IndexToNode(index)} ->"
        previous_index = index
        index = solution.Value(routing.NextVar(index))
        route_distance += routing.GetArcCostForVehicle(previous_index, index, 0)
        
    plan_output += f" {manager.IndexToNode(index)}\n"
    plan_output += f"총 Setup 시간: {route_distance}"
    
    print(plan_output)

def main():
    data = create_data_model()

    manager = pywrapcp.RoutingIndexManager(
        len(data["distance_matrix"]), data["num_vehicles"], data["depot"]
    )

    routing = pywrapcp.RoutingModel(manager)

    def distance_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data["distance_matrix"][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    )

    solution = routing.SolveWithParameters(search_parameters)

    if solution:
        print_solution(manager, routing, solution)

if __name__ == "__main__":
    main()
