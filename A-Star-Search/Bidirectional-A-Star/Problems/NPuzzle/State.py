from StateBase import StateBase
import math

#DEFINE THE CUSTOM TRANSFORMATION FUNCTION BASED ON THE PROBLEM
def hueristic_1(state,goal):
    count = 0
    for i in range(0,len(state)):
        if(state[i] == 0):
            continue
        if(state[i] != goal[i]):
            count+=1;
    return count

def manhattan_distance(i,j,sz):
    r1 = int(i/sz)
    r2 = int(j/sz)
    c1 = int(i%sz)
    c2 = int(j%sz)
    count = 0
    if(r1 > r2):
        count += (r1 - r2)
    else:
        count += (r2 - r1)
        
    if(c1 > c2):
        count += (c1 - c2)
    else:
        count += (c2 - c1)
    return count

def call_hueristic(state,goal,sz,hueristic,scale=1):
	if(hueristic == 0):
		return 0
	if(hueristic == 1):
		return scale*hueristic_1(state,goal)	
	if(sz != 3 or hueristic == 2):
		return scale*hueristic_2(state,goal,sz)	
	if(hueristic == 3):
		return scale*hueristic_3(state,goal,sz)	
	if(hueristic == 4):
		return scale*hueristic_4(state,goal,sz)	

def hueristic_2(state,goal,sz):
    pos = 0
    count = 0
    for i in state:
        pos_2 = goal.index(i)
        if(i != 0):
            count += manhattan_distance(pos,pos_2,sz)
        pos += 1
    return count

def RC_distance(i,j,sz):
    r1 = int(i/sz)
    r2 = int(j/sz)
    c1 = int(i%sz)
    c2 = int(j%sz)
    count = 0
    if(r1 != r2):
        count += 1
    if(c1 != c2):
        count += 1
    return count

#Row column distance (better than h1 but worse than h2)
def hueristic_3(state,goal,sz):
    pos = 0
    count = 0
    for i in state:
        pos_f = goal.index(i)
        if(i != 0):
            count += RC_distance(pos,pos_f,sz)
        pos += 1
    return count

def hueristic_4(state,goal,sz):
    pos = 0
    blank = 0
    blank_g = 0
    candidates = dict()
    for i in state:
        pos_f = goal.index(i)
        if(i != 0):
            if(pos != pos_f):
                candidates[pos_f] = pos
        else:
            blank = pos
            blank_g = pos_f
        pos += 1

    count = 0
    while(len(candidates.keys()) != 0):
        #print(candidates)
        #print(str(blank) + " : " + str(blank_g))
        count += 1
        if(blank == blank_g):
            #any random candidate
            pos_f, pos = list(candidates.items())[0]
            #new place of candidate is the position of blank
            candidates[pos_f] = blank
            #blank goes to position
            blank = pos
            continue
        #current place of blank
        tmp = blank
        #whatever needs to be on blanks current position
        blank = candidates[blank]
        #pop whatever is now replaced by blank
        candidates.pop(tmp)
    return count    


class State(StateBase):
  
   #Inherited constructor
    def __init__(self, value, g_score, parent, goal,scale=1):
        StateBase.__init__(self,value,g_score,parent)
        self.n = int(math.sqrt(len(value)))
        self.h_score = self.hueristic(value,goal,scale)

    def hueristic(self,value,goal,scale=1):
    	return call_hueristic(value,goal,self.n,1,scale)

    def print_val(self):
        str_res = ""
        for i in range(0,self.n):
            lst = self.value[i*self.n:i*self.n+self.n]
            if(0 in lst):
                lst[lst.index(0)] = " "
            for item in lst:
                str_res += "|  " + str(item) + "\t"
            str_res += "|\n"
        return str_res
        
    #Over load the validity
    def is_valid(self,value):
        if(value == None):
            return False
        return True

    def swap(self,val,pos1,pos2):
        tmp = val[pos1]
        val[pos1] = val[pos2]
        val[pos2] = tmp
        return val
        
    def move(self,val,direction):
        pos_empty = val.index(0)
        '''
            0,1,2.....,n-1
            n,........,2n-1
            ..............
            .............
            n*(n-1)...........n^n-1
            
        '''
        
        if(direction == "U" and pos_empty > self.n-1):
            return self.swap(val,pos_empty,pos_empty-self.n)
        elif(direction == "D" and pos_empty < self.n*(self.n-1)):
            return self.swap(val,pos_empty,pos_empty+self.n)
        elif(direction == "L" and pos_empty%self.n != 0):
            return self.swap(val,pos_empty,pos_empty-1)
        elif(direction == "R" and pos_empty%self.n != self.n-1):
            return self.swap(val,pos_empty,pos_empty+1)
        return None
        
    def get_children(self):
        #gets the children of the current node
        possibilities = []
        
        v = self.value[:]
        move_u  = self.move(v,"U")

        v = self.value[:]
        move_d  = self.move(v,"D")
        
        v = self.value[:]
        move_l  = self.move(v,"L")
        
        v = self.value[:]
        move_r  = self.move(v,"R")

        possibilities.append(move_u)
        possibilities.append(move_d)
        possibilities.append(move_l)
        possibilities.append(move_r)
        
        children = []
        for child in possibilities:
            if(self.is_valid(child)):
                children.append([child,1])
        return children
