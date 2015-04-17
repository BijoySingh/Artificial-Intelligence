not([0],1).
not([1],0).

and([1,1],1).
and([0,1],0).
and([1,0],0).
and([0,0],0).

or([0,0],0).
or([0,1],1).
or([1,0],1).
or([1,1],1).

/* Forces that A has value if it is connected into something by that value */
/*value(A,V) :- input(A).*/
value(A,V) :- value_set(A,V).
value(A,V) :- connected(O,A), value(O,V).

connector(X):- value(A,V1), value(A,V2), not(V1 = V2),!,fail.
/* Checks if connector is not inputed from 2*/
connector(X):-connected(Y1,X),connected(Y2,X),not(Y1=Y2),!,fail.
/* Checks if connector is an input */
connector(X):-input(X).
/* Checks if connector is an output*/
connector(X):-output(X).
/* Checks if connector is an input to gate and connected by something*/
connector(X):-gate_input(G,X), connected(Y,X).
/* Checks if connector is an output of gate and connected to something*/
connector(X):-gate_output(G,X), connected(X,Y).


/* and gate */
and_gate(G):-
	gate_input(G,X), gate_input(G,Y),
	not(X = Y), gate_output(G,Z), 
	not(X = Z), not(Y = Z),
	value(X,A), value(Y,B), and([A,B],C),
	asserta(value_set(Z,C)).

/* or gate */
or_gate(G):-
	gate_input(G,X), gate_input(G,Y),
	not(X = Y), gate_output(G,Z), 
	not(X = Z), not(Y = Z),
	value(X,A), value(Y,B),	or([A,B],C), 
	asserta(value_set(Z,C)).

/* not gate */
not_gate(G):-
	gate_input(G,X), gate_output(G,Y), 
	not(X = Y),	value(X,A),	not([A],B),
	asserta(value_set(Y,B)).
