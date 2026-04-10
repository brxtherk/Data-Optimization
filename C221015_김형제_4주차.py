# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 17:01:18 2026

@author: redti
"""

from ortools.linear_solver import pywraplp
import numpy as np
import matplotlib.pyplot as plt
import platform

if platform.system() == 'Windows':
    plt.rcParams['font.family'] = 'Malgun Gothic'
elif platform.system() == 'Darwin':
    plt.rcParams['font.family'] = 'Apple Gothic'
plt.rcParams['axes.unicode_minus'] = False

# [1] 최적화 모델링 & 원문제 풀이
# 목적함수: Max Z = 40x1 + 50x2 + 60x3 (총 이익 최대화)
# 제약조건:
#   1) 2x1 + 1x2 + 3x3 <= 120 (원자재 제약: kg)
#   2) 1x1 + 2x2 + 2x3 <= 80  (노동력 제약: 시간)
#   3) 1x1 + 3x2 + 1x3 <= 100 (기계 가용량: 시간)
#   4) x1, x2, x3 >= 0 (비음 조건)

def solve_primal_pqr():
    solver = pywraplp.Solver.CreateSolver('GLOP')
    
    # 변수: 제품 P, Q, R의 생산량
    x1 = solver.NumVar(0, solver.infinity(), 'P')
    x2 = solver.NumVar(0, solver.infinity(), 'Q')
    x3 = solver.NumVar(0, solver.infinity(), 'R')
    
    # 제약 조건
    c1 = solver.Add(2*x1 + 1*x2 + 3*x3 <= 120)
    c2 = solver.Add(1*x1 + 2*x2 + 2*x3 <= 80)
    c3 = solver.Add(1*x1 + 3*x2 + 1*x3 <= 100)
    
    # 목적 함수
    solver.Maximize(40*x1 + 50*x2 + 60*x3)
    
    solver.Solve()
    
    print(" [1] 원문제(Primal) 최적화 결과 ")
    print(f" > 제품 P(x1) 생산량: {x1.solution_value():.4f} 개")
    print(f" > 제품 Q(x2) 생산량: {x2.solution_value():.4f} 개")
    print(f" > 제품 R(x3) 생산량: {x3.solution_value():.4f} 개")
    print(f" > 최대 이익 (Z*): {solver.Objective().Value():.2f} 만원")
    
    # Slack(여유분)
    s1 = 120 - (2*x1.solution_value() + x2.solution_value() + 3*x3.solution_value())
    s2 = 80 - (x1.solution_value() + 2*x2.solution_value() + 2*x3.solution_value())
    s3 = 100 - (x1.solution_value() + 3*x2.solution_value() + x3.solution_value())
    print(f" > 여유분(Slack): 원자재={abs(s1):.2f}, 노동력={abs(s2):.2f}, 기계={s3:.2f}")

# [2] 쌍대문제

# 목적함수: Min W = 120y1 + 80y2 + 100y3 (자원 총 가치 최소화)
# 제약조건:
#   1) 2y1 + 1y2 + 1y3 >= 40 (제품 P의 단위이익 보전)
#   2) 1y1 + 2y2 + 3y3 >= 50 (제품 Q의 단위이익 보전)
#   3) 3y1 + 2y2 + 1y3 >= 60 (제품 R의 단위이익 보전)
#   4) y1, y2, y3 >= 0 (잠재가격 비음 조건)

def solve_dual_pqr():
    solver = pywraplp.Solver.CreateSolver('GLOP')
    
    # 변수: 자원(원자재, 노동력, 기계)의 잠재가격(Shadow Price)
    y1 = solver.NumVar(0, solver.infinity(), 'y1')
    y2 = solver.NumVar(0, solver.infinity(), 'y2')
    y3 = solver.NumVar(0, solver.infinity(), 'y3')
    
    # 제약 조건
    solver.Add(2*y1 + 1*y2 + 1*y3 >= 40)
    solver.Add(1*y1 + 2*y2 + 3*y3 >= 50)
    solver.Add(3*y1 + 2*y2 + 1*y3 >= 60)
    
    # 목적 함수
    solver.Minimize(120*y1 + 80*y2 + 100*y3)
    
    solver.Solve()
    
    print(" \n [2] 쌍대문제(Dual) 최적화 결과 ")
    print(f" > y1 (원자재 잠재가격): {y1.solution_value():.4f} 만원/kg")
    print(f" > y2 (노동력 잠재가격): {y2.solution_value():.4f} 만원/h")
    print(f" > y3 (기계 잠재가격)  : {y3.solution_value():.4f} 만원/h")
    print(f" > 최소 자원비용 (W*): {solver.Objective().Value():.2f} 만원")

solve_primal_pqr()
solve_dual_pqr()

# [3] 민감도 분석 시각화

def get_z_value(c1, c2, c3, b1=120, b2=80, b3=100):
    solver_s = pywraplp.Solver.CreateSolver('GLOP')
    x1 = solver_s.NumVar(0, solver_s.infinity(), 'P')
    x2 = solver_s.NumVar(0, solver_s.infinity(), 'Q')
    x3 = solver_s.NumVar(0, solver_s.infinity(), 'R')
    solver_s.Add(2*x1 + 1*x2 + 3*x3 <= b1)
    solver_s.Add(1*x1 + 2*x2 + 2*x3 <= b2)
    solver_s.Add(1*x1 + 3*x2 + 1*x3 <= b3)
    solver_s.Maximize(c1*x1 + c2*x2 + c3*x3)
    solver_s.Solve()
    return solver_s.Objective().Value()

# 3.1 제품 P, Q, R 가격 변화 그래프
p_range = np.linspace(20, 100, 50)
fig1, axes1 = plt.subplots(1, 3, figsize=(18, 5))

# [제품 P]
z_p = [get_z_value(p, 50, 60) for p in p_range]
axes1[0].plot(p_range, z_p, lw=2, color='C0')
axes1[0].axvline(40, color='red', ls='--', label='현재 가격: 40')
axes1[0].set_title('제품 P 가격 변화 민감도', fontweight='bold')
axes1[0].set_xlabel('단위 이익 (만원)'); axes1[0].set_ylabel('총 이익 (Z*)')
axes1[0].grid(True, alpha=0.3); axes1[0].legend()

# [제품 Q]
z_q = [get_z_value(40, p, 60) for p in p_range]
axes1[1].plot(p_range, z_q, lw=2, color='C1')
axes1[1].axvline(50, color='red', ls='--', label='현재 가격: 50')
axes1[1].set_title('제품 Q 가격 변화 민감도', fontweight='bold')
axes1[1].set_xlabel('단위 이익 (만원)'); axes1[1].set_ylabel('총 이익 (Z*)')
axes1[1].grid(True, alpha=0.3); axes1[1].legend()

# [제품 R]
z_r = [get_z_value(40, 50, p) for p in p_range]
axes1[2].plot(p_range, z_r, lw=2, color='C2')
axes1[2].axvline(60, color='red', ls='--', label='현재 가격: 60')
axes1[2].set_title('제품 R 가격 변화 민감도', fontweight='bold')
axes1[2].set_xlabel('단위 이익 (만원)'); axes1[2].set_ylabel('총 이익 (Z*)')
axes1[2].grid(True, alpha=0.3); axes1[2].legend()

plt.suptitle('3.1 제품별 가격(Price) 민감도 분석', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.show()

# 3.2 원자재, 노동력, 기계 가용량 변화 그래프
b_range = np.linspace(40, 160, 50)
fig2, axes2 = plt.subplots(1, 3, figsize=(18, 5))

# [원자재]
z_b1 = [get_z_value(40, 50, 60, b1=b) for b in b_range]
axes2[0].plot(b_range, z_b1, lw=2, color='C3')
axes2[0].axvline(120, color='red', ls='--', label='현재 가용량: 120')
axes2[0].set_title('원자재 가용량 변화 민감도', fontweight='bold')
axes2[0].set_xlabel('자원 가용량 (kg)'); axes2[0].set_ylabel('총 이익 (Z*)')
axes2[0].grid(True, alpha=0.3); axes2[0].legend()

# [노동력]
z_b2 = [get_z_value(40, 50, 60, b2=b) for b in b_range]
axes2[1].plot(b_range, z_b2, lw=2, color='C4')
axes2[1].axvline(80, color='red', ls='--', label='현재 가용량: 80')
axes2[1].set_title('노동력 가용량 변화 민감도', fontweight='bold')
axes2[1].set_xlabel('자원 가용량 (시간)'); axes2[1].set_ylabel('총 이익 (Z*)')
axes2[1].grid(True, alpha=0.3); axes2[1].legend()

# [기계]
z_b3 = [get_z_value(40, 50, 60, b3=b) for b in b_range]
axes2[2].plot(b_range, z_b3, lw=2, color='C5')
axes2[2].axvline(100, color='red', ls='--', label='현재 가용량: 100')
axes2[2].set_title('기계 가용량 변화 민감도', fontweight='bold')
axes2[2].set_xlabel('자원 가용량 (시간)'); axes2[2].set_ylabel('총 이익 (Z*)')
axes2[2].grid(True, alpha=0.3); axes2[2].legend()

plt.suptitle('3.2 자원 가용량(RHS) 민감도 분석', fontsize=16, fontweight='bold')
plt.tight_layout() 
plt.show()