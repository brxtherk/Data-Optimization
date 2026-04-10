# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 15:29:53 2026

@author: redti
"""

#예제1
from ortools.linear_solver import pywraplp

def LinearProgrammingExample():
    solver=pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        return
    
    x= solver.NumVar(0,solver.infinity(),'x')
    y= solver.NumVar(0,solver.infinity(),'y')
 
    solver.Add(4*x+2*y<= 30)
    solver.Add(2*x+6*y<= 40)
    
    solver.Maximize(500*x+400*y)
    
    status=solver.Solve()
    
    if status == pywraplp.Solver.OPTIMAL:
        print('OPTIMAL')
        print('목적함수값=%.1f'%(solver.Objective().Value()))
        print('x=%.1f'%(x.solution_value()))
        print('y=%.1f'%(y.solution_value()))
        
    else:
        print('The problem does not have an optimal solution.')

LinearProgrammingExample()

def LinearProgrammingExample():
    solver=pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        return
    x= solver.NumVar(0,solver.infinity(),'x')
    y= solver.NumVar(0,solver.infinity(),'y')

    solver.Add(4*x+2*y<= 30)
    solver.Add(2*x+6*y<= 45)
    
    solver.Maximize(500*x+400*y)
    
    status=solver.Solve()
    
    if status == pywraplp.Solver.OPTIMAL:
        print('OPTIMAL')
        print('목적함수값=%.1f'%(solver.Objective().Value()))
        print('x=%.1f'%(x.solution_value()))
        print('y=%.1f'%(y.solution_value()))
        
    else:
        print('The problem does not have an optimal solution.')

LinearProgrammingExample()

# 예제 2

from ortools.linear_solver import pywraplp

solver=pywraplp.Solver.CreateSolver('SCIP')

data={}
data['constraint_coeffs']=[
    [10,0,20,20,10,20],
    [0,10,30,10,30,20]
]
data['supply']=[50,60]
data['prices']=[350,300,500,340,270,400]
data['num_vars']=6
data['num_constraints']=2

infinity = solver.infinity()

x={}    
for j in range(data['num_vars']):
    x[j]=solver.NumVar(0,solver.infinity(),'x[%i]'%j)

for i in range(data['num_constraints']):
    con=[data['constraint_coeffs'][i][l]*x[l] for l in range(data['num_vars'])]
    solver.Add(sum(con)>=data['supply'][i])
    
obj=[data['prices'][j]*x[j] for j in range(data['num_vars'])]
solver.Minimize(sum(obj))
status= solver.Solve()

if status==pywraplp.Solver.OPTIMAL:
    print(solver.Objective().Value())
    for j in range(data['num_vars']):
        print(x[j].solution_value())
        
else:
    print("The problem does not have an optimal solution.")    
    
# 예제 3

from ortools.linear_solver import pywraplp

solver=pywraplp.Solver.CreateSolver('SCIP')

data={}
data['constraint_coeff']=[[15,10,6,2],
                          [1,6,10,14]]
data['supply']=[750,250]
data['prices']=[2,3,4,5]
data['n_var']= 4
data['n_con']= 2

x={}
for i in range(data['n_var']):
    x[i]=solver.NumVar(0,solver.infinity(),'x[%i]'%i)

for i in range(data['n_con']):
    con_f= [data['constraint_coeff'][i][j]*x[j]/16 for j in range(data['n_var'])]
    solver.Add(sum(con_f)<=data['supply'][i])

#목적함수 생성
obj_f= [data['prices'][i]*x[i] for i in range(data['n_var'])]
solver.Maximize(sum(obj_f))

status= solver.Solve()
if status == pywraplp.Solver.OPTIMAL:
    print(f'총 이익 : {solver.Objective().Value()}')
    for i in range(data['n_var']):
        print(f'{x[i]} : {x[i].solution_value()}')
        
# 실습 1

from ortools.linear_solver import pywraplp
from or2_4_data import *
solver=pywraplp.Solver.CreateSolver('SCIP')

foods = [solver.NumVar(0.0,solver.infinity(),item[0]) for item in data]
print('Number of variables = ',solver.NumVariables())

constraints=[]

for i, nutrient in enumerate(nutrients):
    constraints.append(solver.Constraint(nutrient[1],solver.infinity()))
    for j, item in enumerate(data):
        constraints[i].SetCoefficient(foods[j],item[i+3])
print('Number of constraints = ',solver.NumConstraints())

objective = solver.Objective()
for food in foods:
    objective.SetCoefficient(food, 1)

objective.SetMinimization()

status = solver.Solve()

nutrients_result = [0] * len(nutrients)
print("\nAnnual Foods:")
for i, food in enumerate(foods):
    if food.solution_value() > 0.0:
        print("{}: ${}".format(data[i][0], 365.0 * food.solution_value()))
        for j, _ in enumerate(nutrients):
            nutrients_result[j] += data[i][j + 3] * food.solution_value()
print("\nOptimal annual price: ${:.4f}".format(365.0 * objective.Value()))

print("\nNutrients per day:")
for i, nutrient in enumerate(nutrients):
    print(
        "{}: {:.2f} (min {})".format(nutrient[0], nutrients_result[i], nutrient[1])
)