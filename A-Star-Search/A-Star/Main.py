from AStar import *
import math 

def MainRuntime(start,goal):
    n = math.sqrt(len(start))
    if(not checkGamePossibility(start,goal,n)):
        print("NOT REACHABLE")
        return 
    aStar = AStar(start,goal)

    loop = True
    while(loop):
        res_data = aStar.step()
        loop = res_data[0]
        if(not loop):
            if(res_data[1] == None):
                print("NOT REACHED FROM ALGORITHM")
            else:
                print_data(res_data,goal)
            
            

def inversion_pairs(lst):
    count = 0
    for i in range(0,len(lst)):
        for j in range(i+1,len(lst)):
            if(lst[j] < lst[i]):
                count += 1
    #print(str(lst) + " : " + str(count))
    return count

def parity(val):
    return val%2

def checkGamePossibility(start,end,sz):
    start_st = start[:]
    goal_st = end[:]

    start_blank = start_st.index(0)
    goal_blank = start_st.index(0)
    
    start_st.remove(0)
    goal_st.remove(0)
    
    start_ip = inversion_pairs(start_st)
    goal_ip = inversion_pairs(goal_st)

    if(sz%2 == 1):
        return (parity(start_ip) == parity(goal_ip))
    else:
        return (parity(start_ip + int(start_blank/sz)) ==
                parity(goal_ip + int(goal_blank/sz)))
            
    return True
    	
#STARTING THE PROGRAM
# start_node = [5,6,7,4,0,8,3,2,1]
# start_node = [2,8,1,0,4,3,7,6,5]
start_node = [2,1,4,7,8,3,5,6,0]
# end_node = [1,2,3,8,0,4,7,6,5]
end_node = [1,2,3,4,5,6,7,8,0]

#start_node = [1,2,3,4,5,6,0,8,9,10,7,11,13,14,15,12]
#end_node = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,0]

MainRuntime(start_node,end_node)
