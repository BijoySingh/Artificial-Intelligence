output(o).
input(a).
input(b).

connected(a,i1).
connected(b,i3).
connected(a,i4).
connected(b,i6).
connected(o1,i2).
connected(o2,i5).
connected(o4,i8).
connected(o3,i7).
connected(o5,o).

gate_input(g1,i1).
gate_input(g2,i6).
gate_input(g3,i2).
gate_input(g3,i3).
gate_input(g4,i4).
gate_input(g4,i5).
gate_input(g5,i7).
gate_input(g5,i8).

gate_output(g1,o1).
gate_output(g2,o2).
gate_output(g3,o3).
gate_output(g4,o4).
gate_output(g5,o5).

xor([I1,I2],O):-
	asserta(value_set(a,I1)),
	asserta(value_set(b,I2)),
	not_gate(g1),
	not_gate(g2),
	and_gate(g3),
	and_gate(g4),
	or_gate(g5),
	value(o,O),
	connector(a), connector(b),
	connector(i1),
	connector(i2),
	connector(i3),
	connector(i4),
	connector(i5),
	connector(i6),
	connector(i7),
	connector(i8),
	connector(o1),
	connector(o2),
	connector(o3),
	connector(o4),
	connector(o5),
	connector(o),
	retractall(value_set(A,B)).

verify(xor,A,B):- xor(A,B).
