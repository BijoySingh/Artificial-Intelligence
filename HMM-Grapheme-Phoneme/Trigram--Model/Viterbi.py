import copy

def viterbi(transition_table, states, observation):
	start_symbol = "@"
	blank_reach_here_prob = dict()
	reach_here_prob = dict()
	empty_probability = 0.0000000

	start_states = []
	for x1 in states:
		for x2 in states:
			start_states.append((x1,x2))
	# print(start_states)

	for x in start_states:
		blank_reach_here_prob[x] = (empty_probability,[])
		reach_here_prob[x] = (empty_probability,[])
		# print(str(x) + ">" + str(reach_here_prob[x]))
	reach_here_prob[(start_symbol,start_symbol)] = (1,[])

	for obs in observation:
		new_reach_here_prob = copy.deepcopy(blank_reach_here_prob)

		# print(">>>>" + obs)
		for nextlevel in states:
			best_prob_to_reach_nl = -1
			best_prevstate_to_reach_nl = (start_symbol,start_symbol)
			for prevlevel in start_states:
				prob_to_reach_prevlevel = reach_here_prob[prevlevel][0]
				prob_to_reach_from_prevlevel = transition_table[(prevlevel[0],prevlevel[1],nextlevel,obs)]
				prob = prob_to_reach_prevlevel * prob_to_reach_from_prevlevel
				# if(prob > 0):
					# print(str(prevlevel[0]) + ":" + str(prevlevel[1]) + ">>" +  str(nextlevel) + "::" + str(prob_to_reach_from_prevlevel))
				if(prob > best_prob_to_reach_nl):
					best_prob_to_reach_nl = prob
					best_prevstate_to_reach_nl = prevlevel

			# print(str((best_prevstate_to_reach_nl[1],nextlevel)) + " : " + str(best_prob_to_reach_nl))
			new_reach_here_prob[(best_prevstate_to_reach_nl[1],nextlevel)] = (best_prob_to_reach_nl,
				reach_here_prob[best_prevstate_to_reach_nl][1] +
			 [best_prevstate_to_reach_nl[1]])
		
		reach_here_prob =  copy.deepcopy(new_reach_here_prob)
	
	best_last_state_prob = 0
	best_last_state = (start_symbol, start_symbol)
	for state in start_states:
		if(reach_here_prob[state][0] > best_last_state_prob):
			best_last_state_prob = reach_here_prob[state][0]
			best_last_state = state

	# print(best_last_state)
	reach_here_prob[best_last_state] = (best_last_state_prob,reach_here_prob[best_last_state][1] + [best_last_state[1]])
	# print(reach_here_prob[best_last_state])

	return reach_here_prob[best_last_state]
