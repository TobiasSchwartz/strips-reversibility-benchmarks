#const horizon=1.
#const a="del-all".

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Horizon, must be defined externally
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

time(0..horizon+1).
{final(T) : time(T)} = 1.

%%%%%%%% guess action to check for reversability %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 1 {chosen(A) : action(action(A))} 1.
chosen(a).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Establish initial state
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

holds(V, Val, 0) :- chosen(A), precondition(action(A), variable(V), value(variable(V), Val)).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Opposites
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

opposites(B1, B2) :- boolean(B1), boolean(B2), B1 != B2.
affected(A, V) :- postcondition(action(A), _, variable(V), _).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Guess a reverse plan
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

occurs(A, 1) :- chosen(A).
applied(0). % needed as a starting point
0 {occurs(A, T) : action(action(A))} 1 :- time(T), T > 1.
plan(A, T - 1) :- occurs(A, T), T > 1.

%%%%%%%%%%%%%%%%%%%%%%%
% check for all states
%%%%%%%%%%%%%%%%%%%%%%%
holds(V, Val1, 0) | holds(V, Val2, 0) :- variable(variable(V)), opposites(Val1, Val2), Val1 < Val2.
holds(V, Val, T) :- reversePlan, contains(variable(V), value(variable(V), Val)), time(T).
:- not reversePlan.

% Apply effects
applicable(A, T) :- 
	occurs(A, T),
	applied(T - 1),
	holds(V, Val, T - 1) : precondition(action(A), variable(V), value(variable(V), Val)).
applied(T) :- applicable(_, T).
holds(V, Val, T) :- applicable(A, T), postcondition(action(A), Effect, variable(V), value(variable(V), Val)).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Inertia and Opposite rules
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

holds(V, Value, T) :- holds(V, Value, T - 1), occurs(A, T), applied(T), not affected(A, V).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Verify that goal is met
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% we have a reverse plan (for the current state), if the plan works
same(V) :- holds(V, Val, 0), holds(V, Val, horizon + 1).
samestate :- same(V) : variable(variable(V)).

planvalid :- applied(H + 1), final(H).

reversePlan :- occurs(A,1), planvalid, final(H),
	holds(V, Val, H + 1) : precondition(action(A), variable(V), value(variable(V), Val)).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

#minimize {T : final(T)}.

#show chosen/1.
#show plan/2.
#show final/1.
