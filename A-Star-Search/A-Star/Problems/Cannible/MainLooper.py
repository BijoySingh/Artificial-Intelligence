from AStar import *

def MainRuntime(start,goal):
    for i in range(1,30):
        loop = True
        aStar = AStar(start,goal,i)
        while(loop):
            
            res_data = aStar.step()
            loop = res_data[0]
            if(not loop):
                if(res_data[1] == None):
                    print("NOT REACHED FROM ALGORITHM")
                else:
                    print_data(res_data,goal,2,i)
            
#STARTING THE PROGRAM
start_node = [3,3,0]
end_node = [0,0,1]

MainRuntime(start_node,end_node)
