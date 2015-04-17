def viterbi(transition_table, states, observation):
	start_symbol = "@"
	reach_here_prob = dict()
	for x in states:
		reach_here_prob[x] = (0,[])
	reach_here_prob[start_symbol] = (1,[])

	for obs in observation:
		new_reach_here_prob = dict()
		for nextlevel in states:
			best_prob_to_reach_nl = 0
			best_prevstate_to_reach_nl = start_symbol			
			for prevlevel in states:
				prob_to_reach_prevlevel = reach_here_prob[prevlevel][0]
				prob_to_reach_from_prevlevel = transition_table[(prevlevel,nextlevel,obs)]
				prob = prob_to_reach_prevlevel * prob_to_reach_from_prevlevel
				if(prob > best_prob_to_reach_nl):
					best_prob_to_reach_nl = prob
					best_prevstate_to_reach_nl = prevlevel
			new_reach_here_prob[nextlevel] = (best_prob_to_reach_nl,
				reach_here_prob[best_prevstate_to_reach_nl][1] +
			 [best_prevstate_to_reach_nl])
		reach_here_prob = new_reach_here_prob 
	
	best_last_state_prob = 0
	best_last_state = start_symbol
	for state in states:
		if(reach_here_prob[state][0] > best_last_state_prob):
			best_last_state_prob = reach_here_prob[state][0]
			best_last_state = state
	reach_here_prob[best_last_state] = (best_last_state_prob,reach_here_prob[best_last_state][1] + [best_last_state])
	
	return reach_here_prob[best_last_state]
