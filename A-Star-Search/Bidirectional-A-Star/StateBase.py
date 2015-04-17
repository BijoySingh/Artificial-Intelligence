class StateBase(object):
	#Constructor
    def __init__(self, value, g_score, parent,direction):
        super(StateBase, self).__init__()
        self.value = value
        self.g_score = g_score
        self.parent = parent
        self.h_score = 0
        self.direction = direction

    def hueristic(self,value,goal):
        return 0
        
    #returns the f_Score
    def f_score(self):
        return self.g_score + self.h_score

    def print_val(self):
        return str(self.value)
        
    #To update in case of new instance
    #(never really used this :P wrote this class before the others)
    def update(self,new_instance):
        if(new_instance.f_score() < f_score()):
            self.g_score = new_instance.g_score
            self.h_score = new_instance.h_score
            self.parent = new_instance.parent

   	#Checks Less Than.. did not see if I could overload the operator
    def less_than(self,state):
        return (self.f_score() < state.f_score() or 
            (self.f_score() == state.f_score() and self.h_score < state.h_score))

    def lessThan(self,state):
        return self.less_than(state)

    #Checks if a state is a valid one
    #Used in transformation 
    #	like to see if cannibles exceed missionaries in the transformation
    def is_valid(self,value):
    	return True

    #To get the children to a given state from all transformations
    def get_children(self):
        return []        
