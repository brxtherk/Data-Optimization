# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 11:21:32 2026

@author: redti
"""

# 예제 1

from ortools.sat.python import cp_model

demand_cities = ["강남", "강북", "인천", "수원", "성남", "고양", "부천", 
"안양"]
candidates = ["김포", "강동", "의왕", "파주", "하남", "안산", "남양주"]

# 각수요도시의월간수요량(톤)

weights = [120, 90, 150, 110, 80, 100, 95, 70]

# 거리행렬 d[i][j]: 수요 도시 i → 후보 창고 j (km)
# 김포 강동 의왕 파주 하남 안산 남양주

distances=[
    [38, 15, 22, 55, 20, 40, 28],  # 강남
    [25, 30, 40, 32, 35, 55, 25],  # 강북
    [18, 52, 48, 45, 58, 28, 62],  # 인천
    [40, 38, 15, 65, 42, 22, 50],  # 수원
    [45, 18, 16, 58, 22, 32, 30],  # 성남
    [20, 38, 50, 18, 42, 58, 38],  # 고양
    [15, 38, 32, 35, 45, 25, 48],  # 부천
    [32, 35, 12, 60, 40, 18, 45],  # 안양
]
n = len(demand_cities)  # 수요 도시 수
m = len(candidates)  # 후보 창고 수
p = 3  # 선택할 창고 수

model = cp_model.CpModel()
solver = cp_model.CpSolver()

# 결정변수
x = [model.NewBoolVar(f"x_{candidates[j]}") for j in range(m)]
y = [[model.NewBoolVar(f"y_{demand_cities[i]}_{candidates[j]}")
      for j in range(m)] for i in range(n)]

# 제약(1): 정확히 p개 창고 선택
model.Add(sum(x) == p)

# 제약(2): 각 수요 도시는 정확히 1개 창고에 할당
for i in range(n):
    model.Add(sum(y[i]) == 1)
    
# 제약(3): 선택된 창고에만 할당 가능
for i in range(n):
    for j in range(m):
        model.Add(y[i][j] <=x[j])
        
# 목적함수: 가중거리 합계 최소화
# CP-SAT는 정수형만 처리하므로 실수 거리를 그대로 정수로 사용(이미 정수 데이터)
obj_terms=[]
for i in range(n):
    for j in range(m):
        obj_terms.append(weights[i] *distances[i][j] *y[i][j])
model.Minimize(sum(obj_terms))

solver.parameters.max_time_in_seconds = 60.0
status = solver.Solve(model)

if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    tag = "최적해" if status == cp_model.OPTIMAL else "실행가능해"
    print(f"\n 풀이 상태 : {tag}")
    print(f" 목적함수값: {int(solver.ObjectiveValue()):,} (톤·km/월)")
    
    # 선택된 창고
    selected = [j for j in range(m) if solver.Value(x[j]) == 1]
    print(f"\n ▶ 선택된 창고 ({p}곳):")
    for j in selected:
        print(f" - 후보{j+1}: {candidates[j]}")
        # 할당 결과
        print(f"\n ▶ 수요 도시별 할당 창고:")
        print(f" {'수요 도시':<8} {'수요량':>7} {'배정 창고':<10} {'거리':>6} {'기여 비용':>10}")
        print(f" {'-'*50}")
        total_cost = 0
        for i in range(n):
            assigned = next(j for j in range(m) if solver.Value(y[i][j]) == 1)
            cost = weights[i] * distances[i][assigned]
            total_cost += cost
        print(f" {demand_cities[i]:<8} {weights[i]:>5}톤 {candidates[assigned]:<10} "
              f"{distances[i][assigned]:>4}km  {cost:>8,}톤·km")
        print(f" {'-'*50}")
        print(f" {'합계':<8} {sum(weights):>5}톤            {'':>4}     {total_cost:>8,}톤·km")

    # 창고별 서비스 권역 요약
    print(f"\n ▶ 창고별 서비스 권역:")
    for j in selected:
        served = [demand_cities[i] for i in range(n) if solver.Value(y[i][j]) == 1]
        load = sum(weights[i] for i in range(n) if solver.Value(y[i][j]) == 1)
        print(f"{candidates[j]}: {', '.join(served)} (총 {load}톤)")
else:
    print(" 풀이 실패: 해를 찾지 못했습니다.")
    
print(f"\n 풀이 시간: {solver.WallTime():.4f}초")
print("=" * 60)
                
# 예제 2

from ortools.sat.python import cp_model

# ── 데이터

demand_nodes=[
"수원시", "성남시", "안양시", "부천시",
"고양시", "남양주시", "안산시", "광명시",
"평택시", "의정부시"
]
candidates=[
"수원(후보A)", "성남(후보B)", "안양(후보C)", "부천(후보D)",
"고양(후보E)", "하남(후보F)", "안산(후보G)", "의정부(후보H)"
]
# 거리행렬d[i][j]: 수요지i→ 후보지j (분단위응급도달시간)
# A수원 B성남 C안양 D부천 E고양 F하남 G안산 H의정부
distances=[
[ 5, 28, 22, 38, 48, 30, 25, 55], # 수원시
[28, 5, 18, 40, 42, 15, 38, 42], # 성남시
[22, 18, 5, 30, 40, 25, 20, 50], # 안양시
[38, 40, 30, 5, 22, 42, 28, 38], # 부천시
[48, 42, 40, 22, 5, 35, 45, 20], # 고양시
[30, 15, 25, 42, 35, 5, 42, 30], # 남양주시
[25, 38, 20, 28, 45, 42, 5, 58], # 안산시
[32, 28, 18, 18, 28, 30, 22, 40], # 광명시
[30, 48, 42, 52, 68, 55, 35, 72], # 평택시
[55, 42, 50, 38, 20, 30, 58, 5], # 의정부시
]
n=len(demand_nodes)
m=len(candidates)
p=3 

# 설치할응급센터수               
                    
model =cp_model.CpModel()
solver=cp_model.CpSolver()
# 최대거리값(상한계산)
max_dist=max(distances[i][j] for i in range(n) for j in range(m))
# 결정변수
x=[model.NewBoolVar(f"x_{j}") for j in range(m)]
y=[[model.NewBoolVar(f"y_{i}_{j}") for j in range(m)] for i in range(n)]
D=model.NewIntVar(0, max_dist, "D") # 최대배정거리(최소화대상)
# 제약(1): 정확히p개센터선택
model.Add(sum(x) ==p)
# 제약(2): 각수요지는정확히1개센터에할당
for i in range(n):
    model.Add(sum(y[i]) ==1)
# 제약(3): 선택된센터에만할당가능
for i in range(n):
    for j in range(m):
        model.Add(y[i][j] <=x[j])
# 제약(4): 각수요지의배정거리가D 이하
# Σ_j d_ij* y_ij≤ D → 선택된j는y_ij=1 하나뿐이므로= d_i(assigned)
for i in range(n):
    model.Add(
        sum(distances[i][j] *y[i][j] for j in range(m)) <=D
)
# 목적함수: D 최소화(최악접근시간최소화)
model.Minimize(D)
solver.parameters.max_time_in_seconds=60.0
status=solver.Solve(model)
                    
print("=" * 65)
print(" P-Center 문제: 경기도 응급 의료센터 최적 배치 결과")
print("=" * 65)

if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    tag = "최적해" if status == cp_model.OPTIMAL else "실행가능해"
    opt_D = int(solver.ObjectiveValue())
    print(f"\n 풀이 상태 : {tag}")
    print(f" 최대 도달 시간 (D*): {opt_D}분 ← 이게 최소화된 커버리지 반경")
    
    selected = [j for j in range(m) if solver.Value(x[j]) == 1]
    print(f"\n ▶ 선택된 응급 센터 ({p}곳):")
    for j in selected:
        print(f" - {candidates[j]}")
    
    print(f"\n ▶ 수요지별 할당 결과:")
    print(f" {'수요지':<12} {'배정 센터':<16} {'도달 시간':>8} {'최악?':>5}")
    print(f" {'-'*50}")
    for i in range(n):
        assigned = next(j for j in range(m) if solver.Value(y[i][j]) == 1)
        dist = distances[i][assigned]
        worst = "★ 최악" if dist == opt_D else ""
        print(f" {demand_nodes[i]:<12} {candidates[assigned]:<16} {dist:>5}분 {worst}")
    print(f" {'-'*50}")
    print(f" {'최대 도달 시간':<28} {opt_D:>5}분")
    
    print(f"\n ▶ 센터별 서비스 권역:")
    for j in selected:
        served = [demand_nodes[i] for i in range(n) if solver.Value(y[i][j]) == 1]
        max_d = max(distances[i][j] for i in range(n) if solver.Value(y[i][j]) == 1)
        print(f" {candidates[j]}: {', '.join(served)} (최대 {max_d}분)")
else:
    print(" 풀이 실패: 해를 찾지 못했습니다.")
    
print(f"\n 풀이 시간: {solver.WallTime():.4f}초")
print("=" * 65)
                    
# 예제 3
import math
import random
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs

# 1. 가상 데이터 생성
X, _ = make_blobs(n_samples=300, centers=4, cluster_std=0.60, random_state=0)

# 2. K-Means 모델 생성 및 학습 (K=4)
kmeans = KMeans(n_clusters=5)
kmeans.fit(X)
y_kmeans = kmeans.predict(X)

# 3. 결과 시각화
plt.scatter(X[:, 0], X[:, 1], c=y_kmeans, s=50, cmap='viridis')
centers = kmeans.cluster_centers_
plt.scatter(centers[:, 0], centers[:, 1], c='red', s=200, alpha=0.5, 
marker='X')
plt.title("K-Means Clustering Result")
plt.show()

# 2. K-Means 모델생성및학습(K=4)
def get_distance(p1, p2):
    """두점사이의유클리드거리를계산(루트없이제곱합으로만비교해도무방함)"""
    return math.sqrt(sum((a-b) **2 for a, b in zip(p1, p2)))

# 설정값
k=4
max_iters=100
n_samples=len(X)
n_features=len(X[0])
# 1. 초기중심점설정: 데이터중랜덤하게k개선택
# (X가numpyarray라면X.tolist()로변환해서사용가능)
data_list=X.tolist()
centroids=random.sample(data_list, k)
                   
for iteration in range(max_iters):
    # 2. 할당(Assignment): 각 데이터를 가장가까운중심점그룹에번호로기록
    clusters=[]
    for point in data_list:
        distances=[get_distance(point, c) for c in centroids]
        cluster_idx=distances.index(min(distances))
        clusters.append(cluster_idx)
        
    # 3. 업데이트(Update): 각클러스터의평균을구해새로운중심점계산
    new_centroids=[]
    for i in range(k):
        # i번째클러스터에속한점들만모으기
        group_points=[data_list[j] for j in range(n_samples) if clusters[j] ==i]
        
        if group_points:
            # 각차원별(x, y)로합계를구해평균계산
            new_centroid=[sum(dim) /len(group_points) for dim in zip(*group_points)]
            new_centroids.append(new_centroid)
        else:
            # 만약클러스터에데이터가하나도없다면기존중심점유지
            new_centroids.append(centroids[i])
        # 4. 수렴확인: 중심점이변하지않으면중단
        if new_centroids==centroids:
            print(f"{iteration}회반복후최적의중심점에도출했습니다.")
            break
        centroids=new_centroids
# 시각화를위해결과값을다시형식에맞춰줌
y_kmeans=clusters
centers=np.array(centroids)                    
                    
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs
# 1. 가상데이터생성
X, _ = make_blobs(n_samples=300, centers=4, cluster_std=0.60, random_state=0)
# scikit-learn을활용한엘보우방법예시
sse = []
K_range = range(1, 11)
for k in K_range:
    kmeans = KMeans(n_clusters=k, random_state=0)
    kmeans.fit(X)
    sse.append(kmeans.inertia_) # 각K마다의SSE 값을리스트에저장
# 그래프그리기
plt.plot(K_range, sse, marker='o')
plt.xlabel('Number of clusters (K)')
plt.ylabel('SSE (Inertia)')
plt.title('The Elbow Method')
plt.show()\

# 실습 1 (P-Median 모델)
# 1.1

from ortools.sat.python import cp_model

demand_cities = ["강남", "강북", "인천", "수원", "성남", "고양", "부천", 
"안양"]
candidates = ["김포", "강동", "의왕", "파주", "하남", "안산", "남양주"]

# 각수요도시의월간수요량(톤)
weights = [120, 90, 150, 110, 80, 100, 95, 70]

# 거리행렬 d[i][j]: 수요 도시 i → 후보 창고 j (km)
# 김포 강동 의왕 파주 하남 안산 남양주
distances=[
    [38, 15, 22, 55, 20, 40, 28],  # 강남
    [25, 30, 40, 32, 35, 55, 25],  # 강북
    [18, 52, 48, 45, 58, 28, 62],  # 인천
    [40, 38, 15, 65, 42, 22, 50],  # 수원
    [45, 18, 16, 58, 22, 32, 30],  # 성남
    [20, 38, 50, 18, 42, 58, 38],  # 고양
    [15, 38, 32, 35, 45, 25, 48],  # 부천
    [32, 35, 12, 60, 40, 18, 45],  # 안양
]
n = len(demand_cities)  # 수요 도시 수
m = len(candidates)  # 후보 창고 수
p = 4  # 선택할 창고 수

model = cp_model.CpModel()
solver = cp_model.CpSolver()

# 결정변수
x = [model.NewBoolVar(f"x_{candidates[j]}") for j in range(m)]
y = [[model.NewBoolVar(f"y_{demand_cities[i]}_{candidates[j]}")
      for j in range(m)] for i in range(n)]

# 제약(1): 정확히 p개 창고 선택
model.Add(sum(x) == p)

# 제약(2): 각 수요 도시는 정확히 1개 창고에 할당
for i in range(n):
    model.Add(sum(y[i]) == 1)
    
# 제약(3): 선택된 창고에만 할당 가능

for i in range(n):
    for j in range(m):
        model.Add(y[i][j] <=x[j])
        
# 목적함수: 가중거리 합계 최소화
# CP-SAT는 정수형만 처리하므로 실수 거리를 그대로 정수로 사용(이미 정수 데이터)
obj_terms=[]
for i in range(n):
    for j in range(m):
        obj_terms.append(weights[i] *distances[i][j] *y[i][j])
model.Minimize(sum(obj_terms))

solver.parameters.max_time_in_seconds = 60.0
status = solver.Solve(model)

if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    tag = "최적해" if status == cp_model.OPTIMAL else "실행가능해"
    print(f"\n 풀이 상태 : {tag}")
    print(f" 목적함수값: {int(solver.ObjectiveValue()):,} (톤·km/월)")
    
    # 선택된 창고
    selected = [j for j in range(m) if solver.Value(x[j]) == 1]
    print(f"\n ▶ 선택된 창고 ({p}곳):")
    for j in selected:
        print(f" - 후보{j+1}: {candidates[j]}")
        # 할당 결과
        print(f"\n ▶ 수요 도시별 할당 창고:")
        print(f" {'수요 도시':<8} {'수요량':>7} {'배정 창고':<10} {'거리':>6} {'기여 비용':>10}")
        print(f" {'-'*50}")
        total_cost = 0
        for i in range(n):
            assigned = next(j for j in range(m) if solver.Value(y[i][j]) == 1)
            cost = weights[i] * distances[i][assigned]
            total_cost += cost
        print(f" {demand_cities[i]:<8} {weights[i]:>5}톤 {candidates[assigned]:<10} "
              f"{distances[i][assigned]:>4}km  {cost:>8,}톤·km")
        print(f" {'-'*50}")
        print(f" {'합계':<8} {sum(weights):>5}톤            {'':>4}     {total_cost:>8,}톤·km")

    # 창고별 서비스 권역 요약
    print(f"\n ▶ 창고별 서비스 권역:")
    for j in selected:
        served = [demand_cities[i] for i in range(n) if solver.Value(y[i][j]) == 1]
        load = sum(weights[i] for i in range(n) if solver.Value(y[i][j]) == 1)
        print(f"{candidates[j]}: {', '.join(served)} (총 {load}톤)")
else:
    print(" 풀이 실패: 해를 찾지 못했습니다.")
    
print(f"\n 풀이 시간: {solver.WallTime():.4f}초")
print("=" * 60)

# 1.2

from ortools.sat.python import cp_model

demand_cities = ["강남", "강북", "인천", "수원", "성남", "고양", "부천", 
"안양"]
candidates = ["김포", "강동", "의왕", "파주", "하남", "안산", "남양주"]

# 각수요도시의월간수요량(톤)
weights = [120, 90, 150, 110, 80, 100, 95, 70]

# 거리행렬 d[i][j]: 수요 도시 i → 후보 창고 j (km)
# 김포 강동 의왕 파주 하남 안산 남양주
distances=[
    [38, 15, 22, 55, 20, 40, 28],  # 강남
    [25, 30, 40, 32, 35, 55, 25],  # 강북
    [18, 52, 48, 45, 58, 28, 62],  # 인천
    [40, 38, 15, 65, 42, 22, 50],  # 수원
    [45, 18, 16, 58, 22, 32, 30],  # 성남
    [20, 38, 50, 18, 42, 58, 38],  # 고양
    [15, 38, 32, 35, 45, 25, 48],  # 부천
    [32, 35, 12, 60, 40, 18, 45],  # 안양
]
n = len(demand_cities)  # 수요 도시 수
m = len(candidates)  # 후보 창고 수
p = 3  # 선택할 창고 수

model = cp_model.CpModel()
solver = cp_model.CpSolver()

# 결정변수
x = [model.NewBoolVar(f"x_{candidates[j]}") for j in range(m)]
y = [[model.NewBoolVar(f"y_{demand_cities[i]}_{candidates[j]}")
      for j in range(m)] for i in range(n)]

# 제약(1): 정확히 p개 창고 선택
model.Add(sum(x) == p)


# 제약(2): 각 수요 도시는 정확히 1개 창고에 할당
for i in range(n):
    model.Add(sum(y[i]) == 1)
    
# 제약(3): 선택된 창고에만 할당 가능

for i in range(n):
    for j in range(m):
        model.Add(y[i][j] <=x[j])
        
# 제약(4) : 김포 창고(후보 0번)는 반드시 설치
model.Add(x[0] == 1)
        
# 목적함수: 가중거리 합계 최소화
# CP-SAT는 정수형만 처리하므로 실수 거리를 그대로 정수로 사용(이미 정수 데이터)
obj_terms=[]
for i in range(n):
    for j in range(m):
        obj_terms.append(weights[i] *distances[i][j] *y[i][j])
model.Minimize(sum(obj_terms))

solver.parameters.max_time_in_seconds = 60.0
status = solver.Solve(model)

if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    tag = "최적해" if status == cp_model.OPTIMAL else "실행가능해"
    print(f"\n 풀이 상태 : {tag}")
    print(f" 목적함수값: {int(solver.ObjectiveValue()):,} (톤·km/월)")
    
    # 선택된 창고
    selected = [j for j in range(m) if solver.Value(x[j]) == 1]
    print(f"\n ▶ 선택된 창고 ({p}곳):")
    for j in selected:
        print(f" - 후보{j+1}: {candidates[j]}")
        # 할당 결과
        print(f"\n ▶ 수요 도시별 할당 창고:")
        print(f" {'수요 도시':<8} {'수요량':>7} {'배정 창고':<10} {'거리':>6} {'기여 비용':>10}")
        print(f" {'-'*50}")
        total_cost = 0
        for i in range(n):
            assigned = next(j for j in range(m) if solver.Value(y[i][j]) == 1)
            cost = weights[i] * distances[i][assigned]
            total_cost += cost
        print(f" {demand_cities[i]:<8} {weights[i]:>5}톤 {candidates[assigned]:<10} "
              f"{distances[i][assigned]:>4}km  {cost:>8,}톤·km")
        print(f" {'-'*50}")
        print(f" {'합계':<8} {sum(weights):>5}톤            {'':>4}     {total_cost:>8,}톤·km")

    # 창고별 서비스 권역 요약
    print(f"\n ▶ 창고별 서비스 권역:")
    for j in selected:
        served = [demand_cities[i] for i in range(n) if solver.Value(y[i][j]) == 1]
        load = sum(weights[i] for i in range(n) if solver.Value(y[i][j]) == 1)
        print(f"{candidates[j]}: {', '.join(served)} (총 {load}톤)")
else:
    print(" 풀이 실패: 해를 찾지 못했습니다.")
    
print(f"\n 풀이 시간: {solver.WallTime():.4f}초")
print("=" * 60)

# 1.3

from ortools.sat.python import cp_model

demand_cities = ["강남", "강북", "인천", "수원", "성남", "고양", "부천", 
"안양"]
candidates = ["김포", "강동", "의왕", "파주", "하남", "안산", "남양주"]

# 각수요도시의월간수요량(톤)
weights = [120, 90, 150, 110, 80, 100, 95, 70]

# 거리행렬 d[i][j]: 수요 도시 i → 후보 창고 j (km)
# 김포 강동 의왕 파주 하남 안산 남양주
distances=[
    [38, 15, 22, 55, 20, 40, 28],  # 강남
    [25, 30, 40, 32, 35, 55, 25],  # 강북
    [18, 52, 48, 45, 58, 28, 62],  # 인천
    [40, 38, 15, 65, 42, 22, 50],  # 수원
    [45, 18, 16, 58, 22, 32, 30],  # 성남
    [20, 38, 50, 18, 42, 58, 38],  # 고양
    [15, 38, 32, 35, 45, 25, 48],  # 부천
    [32, 35, 12, 60, 40, 18, 45],  # 안양
]
n = len(demand_cities)  # 수요 도시 수
m = len(candidates)  # 후보 창고 수
p = 3  # 선택할 창고 수

model = cp_model.CpModel()
solver = cp_model.CpSolver()

# 결정변수
x = [model.NewBoolVar(f"x_{candidates[j]}") for j in range(m)]
y = [[model.NewBoolVar(f"y_{demand_cities[i]}_{candidates[j]}")
      for j in range(m)] for i in range(n)]

# 제약(1): 정확히 p개 창고 선택
model.Add(sum(x) == p)

# 제약(2): 각 수요 도시는 정확히 1개 창고에 할당
for i in range(n):
    model.Add(sum(y[i]) == 1)
    
# 제약(3): 선택된 창고에만 할당 가능

for i in range(n):
    for j in range(m):
        model.Add(y[i][j] <=x[j])
        
# 제약(4): 파주 창고(후보 3번)는 토지 수용 문제로 설치 불가능
model.Add(x[3] == 0)
        
# 목적함수: 가중거리 합계 최소화
# CP-SAT는 정수형만 처리하므로 실수 거리를 그대로 정수로 사용(이미 정수 데이터)
obj_terms=[]
for i in range(n):
    for j in range(m):
        obj_terms.append(weights[i] *distances[i][j] *y[i][j])
model.Minimize(sum(obj_terms))

solver.parameters.max_time_in_seconds = 60.0
status = solver.Solve(model)

if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    tag = "최적해" if status == cp_model.OPTIMAL else "실행가능해"
    print(f"\n 풀이 상태 : {tag}")
    print(f" 목적함수값: {int(solver.ObjectiveValue()):,} (톤·km/월)")
    
    # 선택된 창고
    selected = [j for j in range(m) if solver.Value(x[j]) == 1]
    print(f"\n ▶ 선택된 창고 ({p}곳):")
    for j in selected:
        print(f" - 후보{j+1}: {candidates[j]}")
        # 할당 결과
        print(f"\n ▶ 수요 도시별 할당 창고:")
        print(f" {'수요 도시':<8} {'수요량':>7} {'배정 창고':<10} {'거리':>6} {'기여 비용':>10}")
        print(f" {'-'*50}")
        total_cost = 0
        for i in range(n):
            assigned = next(j for j in range(m) if solver.Value(y[i][j]) == 1)
            cost = weights[i] * distances[i][assigned]
            total_cost += cost
        print(f" {demand_cities[i]:<8} {weights[i]:>5}톤 {candidates[assigned]:<10} "
              f"{distances[i][assigned]:>4}km  {cost:>8,}톤·km")
        print(f" {'-'*50}")
        print(f" {'합계':<8} {sum(weights):>5}톤            {'':>4}     {total_cost:>8,}톤·km")

    # 창고별 서비스 권역 요약
    print(f"\n ▶ 창고별 서비스 권역:")
    for j in selected:
        served = [demand_cities[i] for i in range(n) if solver.Value(y[i][j]) == 1]
        load = sum(weights[i] for i in range(n) if solver.Value(y[i][j]) == 1)
        print(f"{candidates[j]}: {', '.join(served)} (총 {load}톤)")
else:
    print(" 풀이 실패: 해를 찾지 못했습니다.")
    
print(f"\n 풀이 시간: {solver.WallTime():.4f}초")
print("=" * 60)

# 1.4

from ortools.sat.python import cp_model

demand_cities = ["강남", "강북", "인천", "수원", "성남", "고양", "부천", 
"안양"]
candidates = ["김포", "강동", "의왕", "파주", "하남", "안산", "남양주"]

# 각수요도시의월간수요량(톤)
weights = [120, 90, 150, 110, 80, 100, 95, 70]

# 거리행렬 d[i][j]: 수요 도시 i → 후보 창고 j (km)
# 김포 강동 의왕 파주 하남 안산 남양주
distances=[
    [38, 15, 22, 55, 20, 40, 28],  # 강남
    [25, 30, 40, 32, 35, 55, 25],  # 강북
    [18, 52, 48, 45, 58, 28, 62],  # 인천
    [40, 38, 15, 65, 42, 22, 50],  # 수원
    [45, 18, 16, 58, 22, 32, 30],  # 성남
    [20, 38, 50, 18, 42, 58, 38],  # 고양
    [15, 38, 32, 35, 45, 25, 48],  # 부천
    [32, 35, 12, 60, 40, 18, 45],  # 안양
]
n = len(demand_cities)  # 수요 도시 수
m = len(candidates)  # 후보 창고 수
p = 3  # 선택할 창고 수

model = cp_model.CpModel()
solver = cp_model.CpSolver()

# 결정변수
x = [model.NewBoolVar(f"x_{candidates[j]}") for j in range(m)]
y = [[model.NewBoolVar(f"y_{demand_cities[i]}_{candidates[j]}")
      for j in range(m)] for i in range(n)]

# 제약(1): 정확히 p개 창고 선택
model.Add(sum(x) == p)

# 제약(2): 각 수요 도시는 정확히 1개 창고에 할당
for i in range(n):
    model.Add(sum(y[i]) == 1)
    
# 제약(3): 선택된 창고에만 할당 가능

for i in range(n):
    for j in range(m):
        model.Add(y[i][j] <=x[j])

# 제약(4): 각 창고는 월 최대 300톤까지만 처리
for j in range(m):
    # j번 창고에 할당된 모든 도시(i)의 (수요량 * 할당여부) 합계
    model.Add(sum(weights[i] * y[i][j] for i in range(n)) <= 300)
        
# 목적함수: 가중거리 합계 최소화
# CP-SAT는 정수형만 처리하므로 실수 거리를 그대로 정수로 사용(이미 정수 데이터)
obj_terms=[]
for i in range(n):
    for j in range(m):
        obj_terms.append(weights[i] *distances[i][j] *y[i][j])
model.Minimize(sum(obj_terms))

solver.parameters.max_time_in_seconds = 60.0
status = solver.Solve(model)

if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    tag = "최적해" if status == cp_model.OPTIMAL else "실행가능해"
    print(f"\n 풀이 상태 : {tag}")
    print(f" 목적함수값: {int(solver.ObjectiveValue()):,} (톤·km/월)")
    
    # 선택된 창고
    selected = [j for j in range(m) if solver.Value(x[j]) == 1]
    print(f"\n ▶ 선택된 창고 ({p}곳):")
    for j in selected:
        print(f" - 후보{j+1}: {candidates[j]}")
        # 할당 결과
        print(f"\n ▶ 수요 도시별 할당 창고:")
        print(f" {'수요 도시':<8} {'수요량':>7} {'배정 창고':<10} {'거리':>6} {'기여 비용':>10}")
        print(f" {'-'*50}")
        total_cost = 0
        for i in range(n):
            assigned = next(j for j in range(m) if solver.Value(y[i][j]) == 1)
            cost = weights[i] * distances[i][assigned]
            total_cost += cost
        print(f" {demand_cities[i]:<8} {weights[i]:>5}톤 {candidates[assigned]:<10} "
              f"{distances[i][assigned]:>4}km  {cost:>8,}톤·km")
        print(f" {'-'*50}")
        print(f" {'합계':<8} {sum(weights):>5}톤            {'':>4}     {total_cost:>8,}톤·km")

    # 창고별 서비스 권역 요약
    print(f"\n ▶ 창고별 서비스 권역:")
    for j in selected:
        served = [demand_cities[i] for i in range(n) if solver.Value(y[i][j]) == 1]
        load = sum(weights[i] for i in range(n) if solver.Value(y[i][j]) == 1)
        print(f"{candidates[j]}: {', '.join(served)} (총 {load}톤)")
else:
    print(" 풀이 실패: 해를 찾지 못했습니다.")
    
print(f"\n 풀이 시간: {solver.WallTime():.4f}초")
print("=" * 60)

# 1.5

from ortools.sat.python import cp_model

demand_cities = ["강남", "강북", "인천", "수원", "성남", "고양", "부천", 
"안양"]
candidates = ["김포", "강동", "의왕", "파주", "하남", "안산", "남양주"]

# 각수요도시의월간수요량(톤)
weights = [120, 90, 150, 110, 80, 100, 95, 70]

# 거리행렬 d[i][j]: 수요 도시 i → 후보 창고 j (km)
# 김포 강동 의왕 파주 하남 안산 남양주
distances=[
    [38, 15, 22, 55, 20, 40, 28],  # 강남
    [25, 30, 40, 32, 35, 55, 25],  # 강북
    [18, 52, 48, 45, 58, 28, 62],  # 인천
    [40, 38, 15, 65, 42, 22, 50],  # 수원
    [45, 18, 16, 58, 22, 32, 30],  # 성남
    [20, 38, 50, 18, 42, 58, 38],  # 고양
    [15, 38, 32, 35, 45, 25, 48],  # 부천
    [32, 35, 12, 60, 40, 18, 45],  # 안양
]
n = len(demand_cities)  # 수요 도시 수
m = len(candidates)  # 후보 창고 수
p = 3  # 선택할 창고 수

model = cp_model.CpModel()
solver = cp_model.CpSolver()

# 결정변수
x = [model.NewBoolVar(f"x_{candidates[j]}") for j in range(m)]
y = [[model.NewBoolVar(f"y_{demand_cities[i]}_{candidates[j]}")
      for j in range(m)] for i in range(n)]

# 제약(1): 정확히 p개 창고 선택
model.Add(sum(x) == p)

# 제약(2): 각 수요 도시는 정확히 1개 창고에 할당
for i in range(n):
    model.Add(sum(y[i]) == 1)
    
# 제약(3): 선택된 창고에만 할당 가능

for i in range(n):
    for j in range(m):
        model.Add(y[i][j] <=x[j])
        
# 제약(4): 어떤 수요 도시도 배정된 창고까지의 거리가 40km를 초과할 수 없음

for i in range(n):
    # 도시 i가 배정된 창고와의 거리는 40 이하
    model.Add(sum(distances[i][j] * y[i][j] for j in range(m)) <= 40)

# 목적함수: 가중거리 합계 최소화
# CP-SAT는 정수형만 처리하므로 실수 거리를 그대로 정수로 사용(이미 정수 데이터)
obj_terms=[]
for i in range(n):
    for j in range(m):
        obj_terms.append(weights[i] *distances[i][j] *y[i][j])
model.Minimize(sum(obj_terms))

solver.parameters.max_time_in_seconds = 60.0
status = solver.Solve(model)

if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    tag = "최적해" if status == cp_model.OPTIMAL else "실행가능해"
    print(f"\n 풀이 상태 : {tag}")
    print(f" 목적함수값: {int(solver.ObjectiveValue()):,} (톤·km/월)")
    
    # 선택된 창고
    selected = [j for j in range(m) if solver.Value(x[j]) == 1]
    print(f"\n ▶ 선택된 창고 ({p}곳):")
    for j in selected:
        print(f" - 후보{j+1}: {candidates[j]}")
        # 할당 결과
        print(f"\n ▶ 수요 도시별 할당 창고:")
        print(f" {'수요 도시':<8} {'수요량':>7} {'배정 창고':<10} {'거리':>6} {'기여 비용':>10}")
        print(f" {'-'*50}")
        total_cost = 0
        for i in range(n):
            assigned = next(j for j in range(m) if solver.Value(y[i][j]) == 1)
            cost = weights[i] * distances[i][assigned]
            total_cost += cost
        print(f" {demand_cities[i]:<8} {weights[i]:>5}톤 {candidates[assigned]:<10} "
              f"{distances[i][assigned]:>4}km  {cost:>8,}톤·km")
        print(f" {'-'*50}")
        print(f" {'합계':<8} {sum(weights):>5}톤            {'':>4}     {total_cost:>8,}톤·km")

    # 창고별 서비스 권역 요약
    print(f"\n ▶ 창고별 서비스 권역:")
    for j in selected:
        served = [demand_cities[i] for i in range(n) if solver.Value(y[i][j]) == 1]
        load = sum(weights[i] for i in range(n) if solver.Value(y[i][j]) == 1)
        print(f"{candidates[j]}: {', '.join(served)} (총 {load}톤)")
else:
    print(" 풀이 실패: 해를 찾지 못했습니다.")
    
print(f"\n 풀이 시간: {solver.WallTime():.4f}초")
print("=" * 60)

# 1.6 

from ortools.sat.python import cp_model

demand_cities = ["강남", "강북", "인천", "수원", "성남", "고양", "부천", 
"안양"]
candidates = ["김포", "강동", "의왕", "파주", "하남", "안산", "남양주"]

# 각수요도시의월간수요량(톤)
weights = [120, 90, 150, 110, 80, 100, 95, 70]

# 거리행렬 d[i][j]: 수요 도시 i → 후보 창고 j (km)
# 김포 강동 의왕 파주 하남 안산 남양주
distances=[
    [38, 15, 22, 55, 20, 40, 28],  # 강남
    [25, 30, 40, 32, 35, 55, 25],  # 강북
    [18, 52, 48, 45, 58, 28, 62],  # 인천
    [40, 38, 15, 65, 42, 22, 50],  # 수원
    [45, 18, 16, 58, 22, 32, 30],  # 성남
    [20, 38, 50, 18, 42, 58, 38],  # 고양
    [15, 38, 32, 35, 45, 25, 48],  # 부천
    [32, 35, 12, 60, 40, 18, 45],  # 안양
]
n = len(demand_cities)  # 수요 도시 수
m = len(candidates)  # 후보 창고 수
p = 3  # 선택할 창고 수

model = cp_model.CpModel()
solver = cp_model.CpSolver()

# 결정변수
x = [model.NewBoolVar(f"x_{candidates[j]}") for j in range(m)]
y = [[model.NewBoolVar(f"y_{demand_cities[i]}_{candidates[j]}")
      for j in range(m)] for i in range(n)]

# 제약(1): 정확히 p개 창고 선택
model.Add(sum(x) == p)

# 제약(2): 각 수요 도시는 정확히 1개 창고에 할당
for i in range(n):
    model.Add(sum(y[i]) == 1)
    
# 제약(3): 선택된 창고에만 할당 가능

for i in range(n):
    for j in range(m):
        model.Add(y[i][j] <=x[j])

# 제약(4): 선택된 창고 각각이 담당하는 수요량은 전체 수요의 50% 이하여야 함

total_demand = sum(weights)

for j in range(m):
    # j번 창고에 할당된 물량 합계 <= (전체 수요 * 0.5)
    model.Add(sum(weights[i] * y[i][j] for i in range(n)) <= int(total_demand * 0.5))
        
# 목적함수: 가중거리 합계 최소화
# CP-SAT는 정수형만 처리하므로 실수 거리를 그대로 정수로 사용(이미 정수 데이터)
obj_terms=[]
for i in range(n):
    for j in range(m):
        obj_terms.append(weights[i] *distances[i][j] *y[i][j])
model.Minimize(sum(obj_terms))

solver.parameters.max_time_in_seconds = 60.0
status = solver.Solve(model)

if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    tag = "최적해" if status == cp_model.OPTIMAL else "실행가능해"
    print(f"\n 풀이 상태 : {tag}")
    print(f" 목적함수값: {int(solver.ObjectiveValue()):,} (톤·km/월)")
    
    # 선택된 창고
    selected = [j for j in range(m) if solver.Value(x[j]) == 1]
    print(f"\n ▶ 선택된 창고 ({p}곳):")
    for j in selected:
        print(f" - 후보{j+1}: {candidates[j]}")
        # 할당 결과
        print(f"\n ▶ 수요 도시별 할당 창고:")
        print(f" {'수요 도시':<8} {'수요량':>7} {'배정 창고':<10} {'거리':>6} {'기여 비용':>10}")
        print(f" {'-'*50}")
        total_cost = 0
        for i in range(n):
            assigned = next(j for j in range(m) if solver.Value(y[i][j]) == 1)
            cost = weights[i] * distances[i][assigned]
            total_cost += cost
        print(f" {demand_cities[i]:<8} {weights[i]:>5}톤 {candidates[assigned]:<10} "
              f"{distances[i][assigned]:>4}km  {cost:>8,}톤·km")
        print(f" {'-'*50}")
        print(f" {'합계':<8} {sum(weights):>5}톤            {'':>4}     {total_cost:>8,}톤·km")

    # 창고별 서비스 권역 요약
    print(f"\n ▶ 창고별 서비스 권역:")
    for j in selected:
        served = [demand_cities[i] for i in range(n) if solver.Value(y[i][j]) == 1]
        load = sum(weights[i] for i in range(n) if solver.Value(y[i][j]) == 1)
        print(f"{candidates[j]}: {', '.join(served)} (총 {load}톤)")
else:
    print(" 풀이 실패: 해를 찾지 못했습니다.")
    
print(f"\n 풀이 시간: {solver.WallTime():.4f}초")
print("=" * 60)
                  
# 실습 2 (P-Center 모델)
# 2.1

from ortools.sat.python import cp_model

# ── 데이터

demand_nodes=[
"수원시", "성남시", "안양시", "부천시",
"고양시", "남양주시", "안산시", "광명시",
"평택시", "의정부시"
]
candidates=[
"수원(후보A)", "성남(후보B)", "안양(후보C)", "부천(후보D)",
"고양(후보E)", "하남(후보F)", "안산(후보G)", "의정부(후보H)"
]
# 거리행렬d[i][j]: 수요지i→ 후보지j (분단위응급도달시간)
# A수원B성남C안양D부천E고양F하남G안산H의정부
distances=[
[ 5, 28, 22, 38, 48, 30, 25, 55], # 수원시
[28, 5, 18, 40, 42, 15, 38, 42], # 성남시
[22, 18, 5, 30, 40, 25, 20, 50], # 안양시
[38, 40, 30, 5, 22, 42, 28, 38], # 부천시
[48, 42, 40, 22, 5, 35, 45, 20], # 고양시
[30, 15, 25, 42, 35, 5, 42, 30], # 남양주시
[25, 38, 20, 28, 45, 42, 5, 58], # 안산시
[32, 28, 18, 18, 28, 30, 22, 40], # 광명시
[30, 48, 42, 52, 68, 55, 35, 72], # 평택시
[55, 42, 50, 38, 20, 30, 58, 5], # 의정부시
]
n=len(demand_nodes)
m=len(candidates)
p=5

# 설치할응급센터수               
                    
model =cp_model.CpModel()
solver=cp_model.CpSolver()
# 최대거리값(상한계산)
max_dist=max(distances[i][j] for i in range(n) for j in range(m))
# 결정변수
x=[model.NewBoolVar(f"x_{j}") for j in range(m)]
y=[[model.NewBoolVar(f"y_{i}_{j}") for j in range(m)] for i in range(n)]
D=model.NewIntVar(0, max_dist, "D") # 최대배정거리(최소화대상)
# 제약(1): 정확히p개센터선택
model.Add(sum(x) ==p)
# 제약(2): 각수요지는정확히1개센터에할당
for i in range(n):
    model.Add(sum(y[i]) ==1)
# 제약(3): 선택된센터에만할당가능
for i in range(n):
    for j in range(m):
        model.Add(y[i][j] <=x[j])
# 제약(4): 각수요지의배정거리가D 이하
# Σ_j d_ij* y_ij≤ D → 선택된j는y_ij=1 하나뿐이므로= d_i(assigned)
for i in range(n):
    model.Add(
        sum(distances[i][j] *y[i][j] for j in range(m)) <=D
)
# 목적함수: D 최소화(최악접근시간최소화)
model.Minimize(D)
solver.parameters.max_time_in_seconds=60.0
status=solver.Solve(model)
                    
print("=" * 65)
print(" P-Center 문제: 경기도 응급 의료센터 최적 배치 결과")
print("=" * 65)

if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    tag = "최적해" if status == cp_model.OPTIMAL else "실행가능해"
    opt_D = int(solver.ObjectiveValue())
    print(f"\n 풀이 상태 : {tag}")
    print(f" 최대 도달 시간 (D*): {opt_D}분 ← 이게 최소화된 커버리지 반경")
    
    selected = [j for j in range(m) if solver.Value(x[j]) == 1]
    print(f"\n ▶ 선택된 응급 센터 ({p}곳):")
    for j in selected:
        print(f" - {candidates[j]}")
    
    print(f"\n ▶ 수요지별 할당 결과:")
    print(f" {'수요지':<12} {'배정 센터':<16} {'도달 시간':>8} {'최악?':>5}")
    print(f" {'-'*50}")
    for i in range(n):
        assigned = next(j for j in range(m) if solver.Value(y[i][j]) == 1)
        dist = distances[i][assigned]
        worst = "★ 최악" if dist == opt_D else ""
        print(f" {demand_nodes[i]:<12} {candidates[assigned]:<16} {dist:>5}분 {worst}")
    print(f" {'-'*50}")
    print(f" {'최대 도달 시간':<28} {opt_D:>5}분")
    
    print(f"\n ▶ 센터별 서비스 권역:")
    for j in selected:
        served = [demand_nodes[i] for i in range(n) if solver.Value(y[i][j]) == 1]
        if served:
            max_d = max(distances[i][j] for i in range(n) if solver.Value(y[i][j]) == 1)
            print(f" {candidates[j]}: {', '.join(served)} (최대 {max_d}분)")
else:
    print(" 풀이 실패: 해를 찾지 못했습니다.")
    
print(f"\n 풀이 시간: {solver.WallTime():.4f}초")
print("=" * 65)

# 2.2

from ortools.sat.python import cp_model

# ── 데이터

demand_nodes=[
"수원시", "성남시", "안양시", "부천시",
"고양시", "남양주시", "안산시", "광명시",
"평택시", "의정부시"
]
candidates=[
"수원(후보A)", "성남(후보B)", "안양(후보C)", "부천(후보D)",
"고양(후보E)", "하남(후보F)", "안산(후보G)", "의정부(후보H)"
]
# 거리행렬d[i][j]: 수요지i→ 후보지j (분단위응급도달시간)
# A수원B성남C안양D부천E고양F하남G안산H의정부
distances=[
[ 5, 28, 22, 38, 48, 30, 25, 55], # 수원시
[28, 5, 18, 40, 42, 15, 38, 42], # 성남시
[22, 18, 5, 30, 40, 25, 20, 50], # 안양시
[38, 40, 30, 5, 22, 42, 28, 38], # 부천시
[48, 42, 40, 22, 5, 35, 45, 20], # 고양시
[30, 15, 25, 42, 35, 5, 42, 30], # 남양주시
[25, 38, 20, 28, 45, 42, 5, 58], # 안산시
[32, 28, 18, 18, 28, 30, 22, 40], # 광명시
[30, 48, 42, 52, 68, 55, 35, 72], # 평택시
[55, 42, 50, 38, 20, 30, 58, 5], # 의정부시
]
n=len(demand_nodes)
m=len(candidates)
p=3 

# 설치할응급센터수               
                    
model =cp_model.CpModel()
solver=cp_model.CpSolver()
# 최대거리값(상한계산)
max_dist=max(distances[i][j] for i in range(n) for j in range(m))
# 결정변수
x=[model.NewBoolVar(f"x_{j}") for j in range(m)]
y=[[model.NewBoolVar(f"y_{i}_{j}") for j in range(m)] for i in range(n)]
D=model.NewIntVar(0, max_dist, "D") # 최대배정거리(최소화대상)
# 제약(1): 정확히p개센터선택
model.Add(sum(x) ==p)
# 제약(2): 각수요지는정확히1개센터에할당
for i in range(n):
    model.Add(sum(y[i]) ==1)
# 제약(3): 선택된센터에만할당가능
for i in range(n):
    for j in range(m):
        model.Add(y[i][j] <=x[j])
# 제약(4): 각수요지의배정거리가D 이하
# Σ_j d_ij* y_ij≤ D → 선택된j는y_ij=1 하나뿐이므로= d_i(assigned)
for i in range(n):
    model.Add(
        sum(distances[i][j] *y[i][j] for j in range(m)) <=D
)
    
# 제약(5): 의정부 센터는 반드시 설치되어야함

model.Add(x[7] == 1)


# 목적함수: D 최소화(최악접근시간최소화)
model.Minimize(D)
solver.parameters.max_time_in_seconds=60.0
status=solver.Solve(model)
                    
print("=" * 65)
print(" P-Center 문제: 경기도 응급 의료센터 최적 배치 결과")
print("=" * 65)

if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    tag = "최적해" if status == cp_model.OPTIMAL else "실행가능해"
    opt_D = int(solver.ObjectiveValue())
    print(f"\n 풀이 상태 : {tag}")
    print(f" 최대 도달 시간 (D*): {opt_D}분 ← 이게 최소화된 커버리지 반경")
    
    selected = [j for j in range(m) if solver.Value(x[j]) == 1]
    print(f"\n ▶ 선택된 응급 센터 ({p}곳):")
    for j in selected:
        print(f" - {candidates[j]}")
    
    print(f"\n ▶ 수요지별 할당 결과:")
    print(f" {'수요지':<12} {'배정 센터':<16} {'도달 시간':>8} {'최악?':>5}")
    print(f" {'-'*50}")
    for i in range(n):
        assigned = next(j for j in range(m) if solver.Value(y[i][j]) == 1)
        dist = distances[i][assigned]
        worst = "★ 최악" if dist == opt_D else ""
        print(f" {demand_nodes[i]:<12} {candidates[assigned]:<16} {dist:>5}분 {worst}")
    print(f" {'-'*50}")
    print(f" {'최대 도달 시간':<28} {opt_D:>5}분")
    
    print(f"\n ▶ 센터별 서비스 권역:")
    for j in selected:
        served = [demand_nodes[i] for i in range(n) if solver.Value(y[i][j]) == 1]
        max_d = max(distances[i][j] for i in range(n) if solver.Value(y[i][j]) == 1)
        print(f" {candidates[j]}: {', '.join(served)} (최대 {max_d}분)")
else:
    print(" 풀이 실패: 해를 찾지 못했습니다.")
    
print(f"\n 풀이 시간: {solver.WallTime():.4f}초")
print("=" * 65)

# 2.3

from ortools.sat.python import cp_model

# ── 데이터

demand_nodes=[
"수원시", "성남시", "안양시", "부천시",
"고양시", "남양주시", "안산시", "광명시",
"평택시", "의정부시"
]
candidates=[
"수원(후보A)", "성남(후보B)", "안양(후보C)", "부천(후보D)",
"고양(후보E)", "하남(후보F)", "안산(후보G)", "의정부(후보H)"
]
# 거리행렬d[i][j]: 수요지i→ 후보지j (분단위응급도달시간)
# A수원B성남C안양D부천E고양F하남G안산H의정부
distances=[
[ 5, 28, 22, 38, 48, 30, 25, 55], # 수원시
[28, 5, 18, 40, 42, 15, 38, 42], # 성남시
[22, 18, 5, 30, 40, 25, 20, 50], # 안양시
[38, 40, 30, 5, 22, 42, 28, 38], # 부천시
[48, 42, 40, 22, 5, 35, 45, 20], # 고양시
[30, 15, 25, 42, 35, 5, 42, 30], # 남양주시
[25, 38, 20, 28, 45, 42, 5, 58], # 안산시
[32, 28, 18, 18, 28, 30, 22, 40], # 광명시
[30, 48, 42, 52, 68, 55, 35, 72], # 평택시
[55, 42, 50, 38, 20, 30, 58, 5], # 의정부시
]
n=len(demand_nodes)
m=len(candidates)
p=3 

# 설치할응급센터수               
                    
model =cp_model.CpModel()
solver=cp_model.CpSolver()
# 최대거리값(상한계산)
max_dist=max(distances[i][j] for i in range(n) for j in range(m))
# 결정변수
x=[model.NewBoolVar(f"x_{j}") for j in range(m)]
y=[[model.NewBoolVar(f"y_{i}_{j}") for j in range(m)] for i in range(n)]
D=model.NewIntVar(0, max_dist, "D") # 최대배정거리(최소화대상)
# 제약(1): 정확히p개센터선택
model.Add(sum(x) ==p)
# 제약(2): 각수요지는정확히1개센터에할당
for i in range(n):
    model.Add(sum(y[i]) ==1)
# 제약(3): 선택된센터에만할당가능
for i in range(n):
    for j in range(m):
        model.Add(y[i][j] <=x[j])
# 제약(4): 각수요지의배정거리가D 이하
# Σ_j d_ij* y_ij≤ D → 선택된j는y_ij=1 하나뿐이므로= d_i(assigned)
for i in range(n):
    model.Add(
        sum(distances[i][j] *y[i][j] for j in range(m)) <=D
)
    
# 제약(5): 안산 후보지가 설치 불가능

model.Add(x[6] == 0)

# 목적함수: D 최소화(최악접근시간최소화)
model.Minimize(D)
solver.parameters.max_time_in_seconds=60.0
status=solver.Solve(model)
                    
print("=" * 65)
print(" P-Center 문제: 경기도 응급 의료센터 최적 배치 결과")
print("=" * 65)

if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    tag = "최적해" if status == cp_model.OPTIMAL else "실행가능해"
    opt_D = int(solver.ObjectiveValue())
    print(f"\n 풀이 상태 : {tag}")
    print(f" 최대 도달 시간 (D*): {opt_D}분 ← 이게 최소화된 커버리지 반경")
    
    selected = [j for j in range(m) if solver.Value(x[j]) == 1]
    print(f"\n ▶ 선택된 응급 센터 ({p}곳):")
    for j in selected:
        print(f" - {candidates[j]}")
    
    print(f"\n ▶ 수요지별 할당 결과:")
    print(f" {'수요지':<12} {'배정 센터':<16} {'도달 시간':>8} {'최악?':>5}")
    print(f" {'-'*50}")
    for i in range(n):
        assigned = next(j for j in range(m) if solver.Value(y[i][j]) == 1)
        dist = distances[i][assigned]
        worst = "★ 최악" if dist == opt_D else ""
        print(f" {demand_nodes[i]:<12} {candidates[assigned]:<16} {dist:>5}분 {worst}")
    print(f" {'-'*50}")
    print(f" {'최대 도달 시간':<28} {opt_D:>5}분")
    
    print(f"\n ▶ 센터별 서비스 권역:")
    for j in selected:
        served = [demand_nodes[i] for i in range(n) if solver.Value(y[i][j]) == 1]
        max_d = max(distances[i][j] for i in range(n) if solver.Value(y[i][j]) == 1)
        print(f" {candidates[j]}: {', '.join(served)} (최대 {max_d}분)")
else:
    print(" 풀이 실패: 해를 찾지 못했습니다.")
    
print(f"\n 풀이 시간: {solver.WallTime():.4f}초")
print("=" * 65)

# 2.4

from ortools.sat.python import cp_model

# ── 데이터

demand_nodes=[
"수원시", "성남시", "안양시", "부천시",
"고양시", "남양주시", "안산시", "광명시",
"평택시", "의정부시"
]
candidates=[
"수원(후보A)", "성남(후보B)", "안양(후보C)", "부천(후보D)",
"고양(후보E)", "하남(후보F)", "안산(후보G)", "의정부(후보H)"
]
# 거리행렬d[i][j]: 수요지i→ 후보지j (분단위응급도달시간)
# A수원B성남C안양D부천E고양F하남G안산H의정부
distances=[
[ 5, 28, 22, 38, 48, 30, 25, 55], # 수원시
[28, 5, 18, 40, 42, 15, 38, 42], # 성남시
[22, 18, 5, 30, 40, 25, 20, 50], # 안양시
[38, 40, 30, 5, 22, 42, 28, 38], # 부천시
[48, 42, 40, 22, 5, 35, 45, 20], # 고양시
[30, 15, 25, 42, 35, 5, 42, 30], # 남양주시
[25, 38, 20, 28, 45, 42, 5, 58], # 안산시
[32, 28, 18, 18, 28, 30, 22, 40], # 광명시
[30, 48, 42, 52, 68, 55, 35, 72], # 평택시
[55, 42, 50, 38, 20, 30, 58, 5], # 의정부시
]
n=len(demand_nodes)
m=len(candidates)
p=3 

# 설치할응급센터수               
                    
model =cp_model.CpModel()
solver=cp_model.CpSolver()
# 최대거리값(상한계산)
max_dist=max(distances[i][j] for i in range(n) for j in range(m))
# 결정변수
x=[model.NewBoolVar(f"x_{j}") for j in range(m)]
y=[[model.NewBoolVar(f"y_{i}_{j}") for j in range(m)] for i in range(n)]
D=model.NewIntVar(0, max_dist, "D") # 최대배정거리(최소화대상)
# 제약(1): 정확히p개센터선택
model.Add(sum(x) ==p)
# 제약(2): 각수요지는정확히1개센터에할당
for i in range(n):
    model.Add(sum(y[i]) ==1)
# 제약(3): 선택된센터에만할당가능
for i in range(n):
    for j in range(m):
        model.Add(y[i][j] <=x[j])
# 제약(4): 각수요지의배정거리가D 이하
# Σ_j d_ij* y_ij≤ D → 선택된j는y_ij=1 하나뿐이므로= d_i(assigned)
for i in range(n):
    model.Add(
        sum(distances[i][j] *y[i][j] for j in range(m)) <=D
)

# 제약(5): 어떤 수요 지점도 배정된 센터까지 도달 시간이 25분 초과x
for i in range(n):
    model.Add(sum(distances[i][j] * y[i][j] for j in range(m)) <= 25)
    
# 목적함수: D 최소화(최악접근시간최소화)
model.Minimize(D)
solver.parameters.max_time_in_seconds=60.0
status=solver.Solve(model)
                    
print("=" * 65)
print(" P-Center 문제: 경기도 응급 의료센터 최적 배치 결과")
print("=" * 65)

if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    tag = "최적해" if status == cp_model.OPTIMAL else "실행가능해"
    opt_D = int(solver.ObjectiveValue())
    print(f"\n 풀이 상태 : {tag}")
    print(f" 최대 도달 시간 (D*): {opt_D}분 ← 이게 최소화된 커버리지 반경")
    
    selected = [j for j in range(m) if solver.Value(x[j]) == 1]
    print(f"\n ▶ 선택된 응급 센터 ({p}곳):")
    for j in selected:
        print(f" - {candidates[j]}")
    
    print(f"\n ▶ 수요지별 할당 결과:")
    print(f" {'수요지':<12} {'배정 센터':<16} {'도달 시간':>8} {'최악?':>5}")
    print(f" {'-'*50}")
    for i in range(n):
        assigned = next(j for j in range(m) if solver.Value(y[i][j]) == 1)
        dist = distances[i][assigned]
        worst = "★ 최악" if dist == opt_D else ""
        print(f" {demand_nodes[i]:<12} {candidates[assigned]:<16} {dist:>5}분 {worst}")
    print(f" {'-'*50}")
    print(f" {'최대 도달 시간':<28} {opt_D:>5}분")
    
    print(f"\n ▶ 센터별 서비스 권역:")
    for j in selected:
        served = [demand_nodes[i] for i in range(n) if solver.Value(y[i][j]) == 1]
        max_d = max(distances[i][j] for i in range(n) if solver.Value(y[i][j]) == 1)
        print(f" {candidates[j]}: {', '.join(served)} (최대 {max_d}분)")
else:
    print(" 풀이 실패: 해를 찾지 못했습니다.")
    
print(f"\n 풀이 시간: {solver.WallTime():.4f}초")
print("=" * 65)

# 2.5

from ortools.sat.python import cp_model

# ── 데이터

demand_nodes=[
"수원시", "성남시", "안양시", "부천시",
"고양시", "남양주시", "안산시", "광명시",
"평택시", "의정부시"
]
candidates=[
"수원(후보A)", "성남(후보B)", "안양(후보C)", "부천(후보D)",
"고양(후보E)", "하남(후보F)", "안산(후보G)", "의정부(후보H)"
]
# 거리행렬d[i][j]: 수요지i→ 후보지j (분단위응급도달시간)
# A수원B성남C안양D부천E고양F하남G안산H의정부
distances=[
[ 5, 28, 22, 38, 48, 30, 25, 55], # 수원시
[28, 5, 18, 40, 42, 15, 38, 42], # 성남시
[22, 18, 5, 30, 40, 25, 20, 50], # 안양시
[38, 40, 30, 5, 22, 42, 28, 38], # 부천시
[48, 42, 40, 22, 5, 35, 45, 20], # 고양시
[30, 15, 25, 42, 35, 5, 42, 30], # 남양주시
[25, 38, 20, 28, 45, 42, 5, 58], # 안산시
[32, 28, 18, 18, 28, 30, 22, 40], # 광명시
[30, 48, 42, 52, 68, 55, 35, 72], # 평택시
[55, 42, 50, 38, 20, 30, 58, 5], # 의정부시
]
n=len(demand_nodes)
m=len(candidates)
p=3 

# 설치할응급센터수               
                    
model =cp_model.CpModel()
solver=cp_model.CpSolver()
# 최대거리값(상한계산)
max_dist=max(distances[i][j] for i in range(n) for j in range(m))
# 결정변수
x=[model.NewBoolVar(f"x_{j}") for j in range(m)]
y=[[model.NewBoolVar(f"y_{i}_{j}") for j in range(m)] for i in range(n)]
D=model.NewIntVar(0, max_dist, "D") # 최대배정거리(최소화대상)
# 제약(1): 정확히p개센터선택
model.Add(sum(x) ==p)
# 제약(2): 각수요지는정확히1개센터에할당
for i in range(n):
    model.Add(sum(y[i]) ==1)
# 제약(3): 선택된센터에만할당가능
for i in range(n):
    for j in range(m):
        model.Add(y[i][j] <=x[j])
# 제약(4): 각수요지의배정거리가D 이하
# Σ_j d_ij* y_ij≤ D → 선택된j는y_ij=1 하나뿐이므로= d_i(assigned)
for i in range(n):
    model.Add(
        sum(distances[i][j] *y[i][j] for j in range(m)) <=D
)
    
# 제약(5): 선택된 센터 중 적어도 1개는 고양/의정부, 적어도 1개는 수원/안산에 배치

model.Add(x[4] + x[7] >= 1)
model.Add(x[0] + x[6] >= 1)

# 목적함수: D 최소화(최악접근시간최소화)
model.Minimize(D)
solver.parameters.max_time_in_seconds=60.0
status=solver.Solve(model)
                    
print("=" * 65)
print(" P-Center 문제: 경기도 응급 의료센터 최적 배치 결과")
print("=" * 65)

if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    tag = "최적해" if status == cp_model.OPTIMAL else "실행가능해"
    opt_D = int(solver.ObjectiveValue())
    print(f"\n 풀이 상태 : {tag}")
    print(f" 최대 도달 시간 (D*): {opt_D}분 ← 이게 최소화된 커버리지 반경")
    
    selected = [j for j in range(m) if solver.Value(x[j]) == 1]
    print(f"\n ▶ 선택된 응급 센터 ({p}곳):")
    for j in selected:
        print(f" - {candidates[j]}")
    
    print(f"\n ▶ 수요지별 할당 결과:")
    print(f" {'수요지':<12} {'배정 센터':<16} {'도달 시간':>8} {'최악?':>5}")
    print(f" {'-'*50}")
    for i in range(n):
        assigned = next(j for j in range(m) if solver.Value(y[i][j]) == 1)
        dist = distances[i][assigned]
        worst = "★ 최악" if dist == opt_D else ""
        print(f" {demand_nodes[i]:<12} {candidates[assigned]:<16} {dist:>5}분 {worst}")
    print(f" {'-'*50}")
    print(f" {'최대 도달 시간':<28} {opt_D:>5}분")
    
    print(f"\n ▶ 센터별 서비스 권역:")
    for j in selected:
        served = [demand_nodes[i] for i in range(n) if solver.Value(y[i][j]) == 1]
        max_d = max(distances[i][j] for i in range(n) if solver.Value(y[i][j]) == 1)
        print(f" {candidates[j]}: {', '.join(served)} (최대 {max_d}분)")
else:
    print(" 풀이 실패: 해를 찾지 못했습니다.")
    
print(f"\n 풀이 시간: {solver.WallTime():.4f}초")
print("=" * 65)

# 2.6

from ortools.sat.python import cp_model

# ── 데이터

demand_nodes=[
"수원시", "성남시", "안양시", "부천시",
"고양시", "남양주시", "안산시", "광명시",
"평택시", "의정부시"
]
candidates=[
"수원(후보A)", "성남(후보B)", "안양(후보C)", "부천(후보D)",
"고양(후보E)", "하남(후보F)", "안산(후보G)", "의정부(후보H)"
]
# 거리행렬d[i][j]: 수요지i→ 후보지j (분단위응급도달시간)
# A수원B성남C안양D부천E고양F하남G안산H의정부
distances=[
[ 5, 28, 22, 38, 48, 30, 25, 55], # 수원시
[28, 5, 18, 40, 42, 15, 38, 42], # 성남시
[22, 18, 5, 30, 40, 25, 20, 50], # 안양시
[38, 40, 30, 5, 22, 42, 28, 38], # 부천시
[48, 42, 40, 22, 5, 35, 45, 20], # 고양시
[30, 15, 25, 42, 35, 5, 42, 30], # 남양주시
[25, 38, 20, 28, 45, 42, 5, 58], # 안산시
[32, 28, 18, 18, 28, 30, 22, 40], # 광명시
[30, 48, 42, 52, 68, 55, 35, 72], # 평택시
[55, 42, 50, 38, 20, 30, 58, 5], # 의정부시
]
n=len(demand_nodes)
m=len(candidates)
p=3 

# 설치할응급센터수               
                    
model =cp_model.CpModel()
solver=cp_model.CpSolver()
# 최대거리값(상한계산)
max_dist=max(distances[i][j] for i in range(n) for j in range(m))
# 결정변수
x=[model.NewBoolVar(f"x_{j}") for j in range(m)]
y=[[model.NewBoolVar(f"y_{i}_{j}") for j in range(m)] for i in range(n)]
D=model.NewIntVar(0, max_dist, "D") # 최대배정거리(최소화대상)
total_dist = sum(distances[i][j] * y[i][j] for i in range(n) for j in range(m))

# 제약(1): 정확히p개센터선택
model.Add(sum(x) ==p)
# 제약(2): 각수요지는정확히1개센터에할당
for i in range(n):
    model.Add(sum(y[i]) ==1)
# 제약(3): 선택된센터에만할당가능
for i in range(n):
    for j in range(m):
        model.Add(y[i][j] <=x[j])
# 제약(4): 각수요지의배정거리가D 이하
# Σ_j d_ij* y_ij≤ D → 선택된j는y_ij=1 하나뿐이므로= d_i(assigned)
for i in range(n):
    model.Add(
        sum(distances[i][j] *y[i][j] for j in range(m)) <=D
)

# 제약(5): 최악도달시간 D <= 30분 보장

for i in range(n):
    model.Add(sum(distances[i][j] * y[i][j] for j in range(m)) <= 30)
    
# 목적함수: 전체 도달 시간의 합계 최소화
model.Minimize(total_dist)
solver.parameters.max_time_in_seconds=60.0
status=solver.Solve(model)
                    
print("=" * 65)
print(" P-Center 문제: 경기도 응급 의료센터 최적 배치 결과")
print("=" * 65)

if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    tag = "최적해" if status == cp_model.OPTIMAL else "실행가능해"
    opt_D = int(solver.ObjectiveValue())
    print(f"\n 풀이 상태 : {tag}")
    print(f" 최대 도달 시간 (D*): {opt_D}분 ← 이게 최소화된 커버리지 반경")
    
    selected = [j for j in range(m) if solver.Value(x[j]) == 1]
    print(f"\n ▶ 선택된 응급 센터 ({p}곳):")
    for j in selected:
        print(f" - {candidates[j]}")
    
    print(f"\n ▶ 수요지별 할당 결과:")
    print(f" {'수요지':<12} {'배정 센터':<16} {'도달 시간':>8} {'최악?':>5}")
    print(f" {'-'*50}")
    for i in range(n):
        assigned = next(j for j in range(m) if solver.Value(y[i][j]) == 1)
        dist = distances[i][assigned]
        worst = "★ 최악" if dist == opt_D else ""
        print(f" {demand_nodes[i]:<12} {candidates[assigned]:<16} {dist:>5}분 {worst}")
    print(f" {'-'*50}")
    print(f" {'최대 도달 시간':<28} {opt_D:>5}분")
    
    print(f"\n ▶ 센터별 서비스 권역:")
    for j in selected:
        served = [demand_nodes[i] for i in range(n) if solver.Value(y[i][j]) == 1]
        max_d = max(distances[i][j] for i in range(n) if solver.Value(y[i][j]) == 1)
        print(f" {candidates[j]}: {', '.join(served)} (최대 {max_d}분)")
else:
    print(" 풀이 실패: 해를 찾지 못했습니다.")
    
print(f"\n 풀이 시간: {solver.WallTime():.4f}초")
print("=" * 65)    