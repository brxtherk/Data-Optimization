# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from ortools.linear_solver import pywraplp

def LinearProgrammingExample():
    solver = pywraplp.Solver.CreateSolver("SCIP")
    if not solver:
        return
    
    x=solver.IntVar(0,solver.infinity(),'x')
    y=solver.IntVar(0,solver.infinity(),'y')
    print("Number of variables =", solver.NumVariables())
    
    solver.Add(x+2*y <=13.0)
    solver.Add(3*x-y>=0.0)
    solver.Add(x-y<=2.0)
    print("Number of constraints =", solver.NumConstraints())

    solver.Maximize(3 * x + 4 * y)
    print(f'solving with {solver.SolverVersion()}')
    status = solver.Solve()

    if status==pywraplp.Solver.OPTIMAL:
        print("Solution:")
        print(f"Objective value = {solver.Objective().Value():0.1f}")
        print(f"x = {x.solution_value():0.1f}")
        print(f"y = {y.solution_value():0.1f}")
    else:
        print("The problem does not have an optimal solution.")
    print("\nAdvanced usage:")
    print(f"Problem solved in {solver.wall_time():d} milliseconds")
    print(f"Problem solved in {solver.iterations():d} iterations")
    
LinearProgrammingExample()