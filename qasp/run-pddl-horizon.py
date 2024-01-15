#!/usr/bin/env python3
# python3 /tools/run-pddl-horizon.py qasp/inst2.pddl 2 > inst2.pddl.qasp

import argparse
import os

parser = argparse.ArgumentParser(description='Transform PDDL domain into qasp reverse check with horizon n.')

parser.add_argument('pddlfile', type=open, help='PDDL file')
parser.add_argument('n', type=int, help='horizon')

args = parser.parse_args()

print("%@exists")
print(f"time(0..{args.n+1}).")
print(f"horizon({args.n}).")
print('''
%%% Guess action to check for reversability.
{ chosen(A) } :- action(action(A)).
:- #count{A:chosen(A)} != 1.

%%% Guess plan. First action is the chosen one, the others will be the reverse plan (if it does reverse).
occurs(A, 1) :- chosen(A).
{occurs(A, T)} :- action(action(A)), time(T), T > 1.
:- #count{A:occurs(A, T)}!=1,time(T), T > 1.
plan(A, T - 1) :- occurs(A, T), T > 1.
''')
print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
print(f"% begin plasp output for {args.pddlfile.name}",flush=True)
os.system(f"plasp translate {args.pddlfile.name}")
print(f"% end plasp output for {args.pddlfile.name}")
print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
print('''
%@forall

%%% Establish necessary bits of the initial state: preconditions of the to-be-reversed action must hold.
holds(V, Val, 0) :- chosen(A), precondition(action(A), variable(V), value(variable(V), Val)).

%%% For all initial states...
{holds(V,Val,0)} :- contains(variable(V),value(variable(V),Val)).
:- #count{Val:holds(V,Val,0)} != 1, variable(variable(V)).


% Action effects.
caused(V, Val, T) :-
	occurs(A, T),
	postcondition(action(A), E, variable(V), value(variable(V), Val)).

%%% Inertia rules

modified(V, T) :- caused(V, _, T).
holds(V, Val, T) :- caused(V, Val, T).
holds(V, Val, T) :- holds(V, Val, T - 1), not modified(V, T), time(T).


%@constraint

%%% Plan that does not reverse the chosen action?
:- holds(V, Val, 0), not holds(V, Val, H+1), horizon(H).
:- holds(V, Val, H+1), not holds(V, Val, 0), horizon(H).

%%% Unmet preconditions?
:- occurs(A, T), precondition(action(A), variable(V), value(variable(V), Val)), not holds(V, Val, T - 1).
''')
