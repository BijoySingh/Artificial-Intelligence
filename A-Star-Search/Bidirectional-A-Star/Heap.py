#Heap Class for the State Type
class Heap(object):
    def __init__(self):
        super(Heap, self).__init__()
        self.i_list = []
        self.i_dict = dict()

    #Move up the current node
    def moveup(self,pos):
        if(pos == 0):
            return
        size = pos+1
        parent = int(size/2)
        if(self.i_list[size-1].lessThan(self.i_list[parent-1])):
            self.swap(parent-1,size-1)
            self.moveup(parent-1)

    def print_i_list(self):
        res_s = ""
        for state in self.i_list:
            res_s += str(state.f_score()) + ":"
        print(res_s)

    #Swap Position in the heap_list
    def swap(self,pos1,pos2):
        tmp = self.i_list[pos1]
        self.i_list[pos1] = self.i_list[pos2]
        self.i_list[pos2] = tmp
        self.i_dict[str(self.i_list[pos1].value)] = pos1
        self.i_dict[str(self.i_list[pos2].value)] = pos2

    def movedown(self,pos):
        if(2*(pos+1) > len(self.i_list)):
            return
        elif(2*(pos+1) + 1 > len(self.i_list)):
            if(self.i_list[2*(pos+1) - 1].lessThan(self.i_list[pos])):
                self.swap(pos,2*(pos+1) - 1)
                return
        else:
            child_1 = 2*(pos+1) - 1
            child_2 = 2*(pos+1)
            v = self.i_list[pos]
            v1 = self.i_list[child_1]
            v2 = self.i_list[child_2]
            
            #v < v1
            if(v.lessThan(v1)):
                if(v.lessThan(v2)):
                    return
                elif(v2.lessThan(v)):
                    self.swap(pos,child_2)
                    self.movedown(child_2)
                    return
                else:
                    return
            elif(v1.lessThan(v)):
                if(v.lessThan(v2)):
                    self.swap(pos,child_1)
                    self.movedown(child_1)
                    return
                elif(v2.lessThan(v)):
                    if(v2.lessThan(v1)):
                        self.swap(pos,child_2)
                        self.movedown(child_2)
                        return
                    else:
                        self.swap(pos,child_1)
                        self.movedown(child_1)
                        return
                #v = v2 , v1 < v
                else:
                    self.swap(pos,child_1)
                    self.movedown(child_1)
                    return
            #v = v1
            else:
                if(v2.lessThan(v)):
                    self.swap(pos,child_2)
                    self.movedown(child_2)
                    return
                else:
                    return

    def insert(self,state):
        self.i_list.append(state)
        self.i_dict[str(state.value)] = len(self.i_list) - 1
        size = len(self.i_list)
        self.moveup(size - 1)
        
    def pop_top(self):
        if(len(self.i_list) == 0):
            return None
        
        self.swap(0,len(self.i_list)-1)
        state = self.i_list.pop(len(self.i_list)-1)
        self.i_dict.pop(str(state.value))
        self.movedown(0)
        return state

    def deleteByValue(self,value):
        pos = self.i_dict[str(value)]
        self.moveup(pos)
        self.movedown(pos)

    def getByValue(self,value):
        pos = self.i_dict[str(value)]
        return self.i_list[pos]

    def is_contained(self,value):
        if str(value) in self.i_dict.keys():
            return True
        return False

    def update(self,value,n_gscore,n_parent,n_direction):
        pos = self.i_dict[str(value)]
        if(n_gscore < self.i_list[pos].g_score):
            self.i_list[pos].g_score = n_gscore
            self.i_list[pos].parent = n_parent
            self.i_list[pos].direction = n_direction
            self.moveup(pos)
