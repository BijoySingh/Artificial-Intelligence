verify(full_adder,A,B):-full_adder(A,B).

full_adder([A,B,C], O) :-
	or([I_1_or_1,I_1_or_2],O),
	and([I_9_and_1,I_9_and_2],O_9_and),
	connected(C,I_9_and_2),
	connected(A,I_9_and_1),
	or([I_2_or_1,I_2_or_2],O_2_or),
	and([I_6_and_1,I_6_and_2],O_6_and),
	connected(C,I_6_and_2),
	connected(B,I_6_and_1),
	and([I_3_and_1,I_3_and_2],O_3_and),
	connected(B,I_3_and_2),
	connected(A,I_3_and_1),
	connected(O_6_and,I_2_or_2),
	connected(O_3_and,I_2_or_1),
	connected(O_9_and,I_1_or_2),
	connected(O_2_or,I_1_or_1).


