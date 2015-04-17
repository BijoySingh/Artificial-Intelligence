output(o).
input(a).
input(b).
input(c).

connected(a,i1).
connected(b,i2).
connected(o1,i3).
connected(c,i4).
connected(o2,o).

gate_input(g1,i1).
gate_input(g1,i2).
gate_input(g2,i3).
gate_input(g2,i4).
gate_output(g1,o1).
gate_output(g2,o2).

and3([I1,I2,I3],O):-
	asserta(value_set(a,I1)),
	asserta(value_set(b,I2)),
	asserta(value_set(c,I3)),
	and_gate(g1),
	and_gate(g2),
	value(o,O),
	connector(a), connector(b), connector(c),
	connector(i1), connector(i2), connector(o1),
	connector(i4), connector(i3), connector(o2),
	connector(o),
	retractall(value_set(A,B)).
