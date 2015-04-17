from Heap import Heap
from State import State

def print_data(data,goal,mode=1,scale=1):
    if(mode==1):
        print("MOVES : " + str(data[1]))
        print("REINCARNATIONS : " + str(data[3]))
    graph = data[2]
    move_count = 0
    parent = goal
    res_string = ""
    while(parent != None):
        move_count += 1
        node = graph[str(parent)]
        parent = node.parent
        if(res_string != ""):
            res_string = node.print_val() + "\n TO \n\n" + res_string
        else:
            res_string = node.print_val()
    if(mode==1):
        print("SHORTEST PATH : " + str(move_count))
        print(res_string)
    else:
        print("(" + str(scale) + "," + str(data[1]) + "," + str(move_count) + ")")
    
class AStar(object):
    def __init__(self,start,goal,scale=1):
        super(AStar, self).__init__()
        #The open list
        self.OL = Heap()
        self.scale = scale
        #The goal value
        self.goal = goal
        
        #Setting up the open list with start state
        start_state = State(start, 0, None,self.goal,self.scale)
        self.OL.insert(start_state)

        #The closed list
        self.CL = dict()
        self.log = []
        self.expand_count = 0
        self.reincarnation_expand_count = 0

    def remove_recursively(self,queue):      
        if(len(queue) == 0):
            return
        front = queue.pop(0)
        best_state = front[0]
        child = front[1]
        weight = front[2]

        old_state = self.CL[str(child)]        
        
        if(old_state.g_score > best_state.g_score + weight):
            #print("Reincarnated")
            #print(self.OL.print_i_list())
            #best_state.print_val()

            n_state = State(child,best_state.g_score + weight,best_state.value,self.goal,self.scale)
            
            #self.log.append(n_state)
            self.reincarnation_expand_count += 1
            
            self.CL[str(child)] = n_state
            new_values = n_state.get_children()
            for edge in new_values:
                n_child = edge[0]
                n_weight = edge[1]
                if(self.OL.is_contained(n_child)):
                    self.OL.update(n_child,n_weight+n_state.g_score,n_state.value)
                elif(str(n_child) in self.CL.keys()):
                    queue.append((n_state,n_child,n_weight))
                else:
                    print("LOGICAL ERROR OCCURED")
        self.remove_recursively(queue)

    def step(self):
        #The best state to be now transformed into the closed list
        best_state = self.OL.pop_top()
        if(best_state == None):
            return [False,None,None]
        
        self.CL[str(best_state.value)] = best_state
        #self.log.append(best_state)
        self.expand_count += 1

        #End of the program. the goal is found
        if(best_state.value == self.goal):
            return [False,self.expand_count,self.CL,self.reincarnation_expand_count]

        #Not the end of the program
        else:
            #Get the next children based of the transformation
            for edge in best_state.get_children():
                #The child value
                child = edge[0]
                #The cost for the transformation
                weight = edge[1]

                #Already in the closed list.
                if(str(child) in self.CL.keys()):
                    '''

                    # Check if need to update
                    # Make a queue of to_remove states 
                    # For the top node
                    # go through children and see which need updatiion and in quue if they were closed


                    '''
                    self.remove_recursively([(best_state,child,weight)])
                    continue

                #Might have to update the child already in the open list
                elif(self.OL.is_contained(child)):
                    self.OL.update(child,weight+best_state.g_score,best_state.value)

                #Adding the new node to the open list.
                else:
                    new_state = State(child,best_state.g_score + weight,best_state.value,self.goal,self.scale)
                    self.OL.insert(new_state)

        #Recursive Loop
        return [True,None,None]
