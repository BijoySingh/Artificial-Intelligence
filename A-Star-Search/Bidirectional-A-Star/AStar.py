from Heap import Heap
from State import State


def get_print_data(graph,parent,up=True):
    move_count = 0
    res_string = ""
    while(parent != None):
        move_count += 1
        node = graph[str(parent)]
        parent = node.parent
        if(res_string != "" and up):
            res_string = node.print_val() + "\n TO \n\n" + res_string
        elif(res_string != "" and not up):
            res_string = res_string + "\n TO \n\n" + node.print_val()
        else:
            res_string = node.print_val()
    return (move_count,res_string)


def print_data(data,mode=1,scale=1):
    expand_count = data[1]
    cl_forward = data[2]
    cl_backward = data[3]
    is_final = data[4]
    parent_node = data[5]
    move_count = 0
    move_path = ""

    res_data_forward = get_print_data(cl_forward,parent_node,True)
    res_data_backward = get_print_data(cl_backward,parent_node,False)

    move_count += res_data_forward[0] + res_data_backward[0] - 1
    move_path += res_data_forward[1] + "\n --TO-- \n\n" + res_data_backward[1]

    if(mode == 1):
        print("EXPANSIONS : " + str(expand_count))
        print("MOVES : " + str(move_count))
        print("PATH : \n" + move_path)
    else:
        print(str(expand_count) + "," + str(move_count) + "," +str(scale))

            

class AStar(object):
    def __init__(self,start,goal,scale=1):
        super(AStar, self).__init__()
        #The open list
        self.OL_forward = Heap()
        self.OL_backward = Heap()

        self.scale = scale
        #The goal value
        self.start = start
        self.goal = goal
        
        #Setting up the open list with start state
        start_state = State(start, 0, None,self.goal,True,self.scale)
        self.OL_forward.insert(start_state)
        goal_state = State(goal, 0, None,self.start,False,self.scale)
        self.OL_backward.insert(goal_state)

        #The closed list
        self.CL = dict()
        self.CL_forward = dict()
        self.CL_backward = dict()
        
        self.log = []
        self.expand_count = 0


    def put_in_closed_list(self,state):
        if(state.direction):
            self.CL_forward[str(state.value)] = state
        self.CL_backward[str(state.value)] = state

    def get_from_closed_list(self,key,direction):
        if(direction):
            return self.CL_forward[key]
        return self.CL_backward[key]


    def remove_recursively(self,queue):      
        if(len(queue) == 0):
            return
        front = queue.pop(0)
        best_state = front[0]
        child = front[1]
        weight = front[2]

        old_state = self.get_from_closed_list(str(child),best_state.direction)        
        
        if(old_state.g_score > best_state.g_score + weight):
            if(best_state.direction):
                n_state = State(child,best_state.g_score + weight,best_state.value,self.goal,best_state.direction,self.scale)
            else:
                n_state = State(child,best_state.g_score + weight,best_state.value,self.start,best_state.direction,self.scale)
            
            self.put_in_closed_list(n_state)
            new_values = n_state.get_children()
            for edge in new_values:
                n_child = edge[0]
                n_weight = edge[1]
                if(self.OL.is_contained(n_child)):
                    self.OL.update(n_child,n_weight+n_state.g_score,n_state.value,n_state.direction)
                elif(str(n_child) in self.CL.keys()):
                    queue.append((n_state,n_child,n_weight))
                else:
                    print("LOGICAL ERROR OCCURED")
        
        self.remove_recursively(queue)

    def step(self):
        #The best state to be now transformed into the closed list
        best_state_forward = self.OL_forward.pop_top()
        best_state_backward = self.OL_backward.pop_top()

        if(best_state_forward == None or best_state_backward == None):
            return [False,None,None]
        
        self.CL_forward[str(best_state_forward.value)] = best_state_forward
        self.CL_backward[str(best_state_backward.value)] = best_state_backward

        self.expand_count += 2

        #End of the program. the goal is found
        if(best_state_forward.value == self.goal):
            return [False,self.expand_count,self.CL_forward,self.CL_backward,True,self.goal]

        elif(best_state_backward.value == self.start):
            return [False,self.expand_count,self.CL_forward,self.CL_backward,True,self.start]

        if(str(best_state_forward.value) in self.CL_backward.keys()):
            return [False,self.expand_count,self.CL_forward,self.CL_backward,False,best_state_forward.value]

        elif(str(best_state_backward.value) in self.CL_forward.keys()):
            return [False,self.expand_count,self.CL_forward,self.CL_backward,False,best_state_backward.value]

        else:
            for edge in best_state_forward.get_children():
                child = edge[0]
                weight = edge[1]

                if(str(child) in self.CL_forward.keys()):
                    child_state = self.CL_forward[str(child)]
                    self.remove_recursively([(best_state_forward,child,weight)])
                    continue

                elif(self.OL_forward.is_contained(child)):
                    self.OL_forward.update(child,weight+best_state_forward.g_score,best_state_forward.value,best_state_forward.direction)

                else:
                    new_state = None
                    new_state = State(child,best_state_forward.g_score + weight,best_state_forward.value,self.goal,best_state_forward.direction,self.scale)
                    self.OL_forward.insert(new_state)


            for edge in best_state_backward.get_children():
                child = edge[0]
                weight = edge[1]

                if(str(child) in self.CL_backward.keys()):
                    child_state = self.CL_backward[str(child)]
                    self.remove_recursively([(best_state_backward,child,weight)])
                    continue

                elif(self.OL_backward.is_contained(child)):
                    self.OL_backward.update(child,weight+best_state_backward.g_score,best_state_backward.value,best_state_backward.direction)

                else:
                    new_state = None
                    new_state = State(child,best_state_backward.g_score + weight,best_state_backward.value,self.start,best_state_backward.direction,self.scale)
                    self.OL_backward.insert(new_state)

        return [True,None,None]
