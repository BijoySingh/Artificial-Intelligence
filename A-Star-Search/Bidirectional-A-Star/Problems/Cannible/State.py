from StateBase import StateBase

def call_hueristic(value,hu):
    if(hu == 0):
        return 0
    elif(hu == 1):
        return hueristic_1(value)
    elif(hu == 2):
        return hueristic_2(value)
    else:
        return 0
    
def hueristic_1(value):
    count = value[0] + value[1]
    if(count == 0):
        return count
    return count - 1

def hueristic_2(value):
    count = value[0] + value[1]
    if(count == 0):
            return 0
    if(value[2] == 0):
        if(count <= 2):
            return 1
        else:
            return 2*(count - 1) - 1
    else:
        if(count == 0):
            return 0
        else:
            count += 1
            if(count <= 2):
                return 2
            else:
                return 2*(count - 1)

#DEFINE THE CUSTOM TRANSFORMATION FUNCTION BASED ON THE PROBLEM
class State(StateBase):

    #Inherited constructor
    def __init__(self, value, g_score, parent, goal,scale=1):
        StateBase.__init__(self,value,g_score,parent)
        self.h_score = scale*self.hueristic(value,goal)

    def hueristic(self,value,goal):
        return call_hueristic(value,2)
        
    #Over load the validity
    def is_valid(self,value):
        max_num = 3
        if((value[0] >= value[1] or value[0] == 0) and (max_num-value[0] >= max_num - value[1] or value[0] == max_num)):
            return True

        return False

    def get_children(self):
        #gets the children of the current node
        possibilities = []
        v = self.value[:]
        
        #on first side
        if(v[2] == 0):
            possibilities.append([v[0]-1,v[1],1])
            possibilities.append([v[0]-2,v[1],1])
            possibilities.append([v[0]-1,v[1]-1,1])
            possibilities.append([v[0],v[1]-2,1])
            possibilities.append([v[0],v[1]-1,1])

        #on other side
        elif(v[2] == 1):  
            possibilities.append([v[0]+1,v[1],0])
            possibilities.append([v[0]+2,v[1],0])
            possibilities.append([v[0]+1,v[1]+1,0])
            possibilities.append([v[0],v[1]+2,0])
            possibilities.append([v[0],v[1]+1,0])
            #possibilities.append([v[0],v[1],0])

        children = []
        for child in possibilities:
            if(self.is_valid(child)):
                children.append([child,1])
        return children
