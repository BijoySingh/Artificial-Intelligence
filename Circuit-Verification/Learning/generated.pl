verify(xor,A,B):-xor(A,B).
xor([A,B], O) :- not([B],T4) , and([A,T4],T2) , not([A],T3) , and([T3,B],T1) , or([T1,T2],O).
verify(full_adder,A,B):-full_adder(A,B).
full_adder([A,B,C], O) :- or([T1,T2],O) , and([A,C],T2) , or([T3,T4],T1) , and([B,C],T4) , and([A,B],T3).
verify(half_adder,A,B):-half_adder(A,B).
half_adder([A,B], O) :- xor([A,B],O).
