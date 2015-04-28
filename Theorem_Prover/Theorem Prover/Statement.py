import copy

def removeStringDuplicates(lst):
    seen = set()
    seen_add = seen.add
    return [ x for x in lst if not (x in seen or seen_add(x))]    

class Statement(object):
    def __init__(self,left=None,right=None,
        operator=None,value=None):
        super(Statement, self).__init__()
        '''
            operator = '>' : Implication
            operator = None : Implies terminal
            left : left child
            right : right child
            value : string interpretation
        '''
        self.pattern = dict()
        self.left = copy.deepcopy(left)
        self.operator = operator
        self.right = copy.deepcopy(right)
        if(value==None and left != None and right != None):
            self.value = "(" + left.getValue() + ")>(" + right.getValue() + ")"
        else:
            self.value = value

        if(left == None and operator == None and right == None and value == "F"):
            self.value = False

        self.proof = []
        self.antiproof = []

    def __eq__(self, other):
        if isinstance(other, Statement):
            if((self.isStatement() and other.isStatement()) or 
                (not (self.isStatement() or other.isStatement()))):
                return self.value == other.value
            return False
        return False
    
    def __ne__(self, other):
        result = self.__eq__(other)
        return not result

    '''
        DEALING WITH NEGATION
        Next Few functions will deal with NEGATION
        false_node : Creates a node which is false
        negate : Negates a Statement
        remove_top_negation : removes the negation at the topmost level
        remove_not_rec : removes negation recursively till the bottom
    '''
    def false_node(self):
        false_stmt = Statement(None,None,None,False)
        return false_stmt

    def negation(self,proof_type=0):
        stmt = None
        if(not self.isStatement()):
            stmt = Statement(self,self.false_node(),'>')    

        elif(self.right.value == False):
            stmt = copy.deepcopy(self.left)

        else:
            stmt = Statement(self,self.false_node(),'>','('+ self.getValue() + ')>(False)')

        stmt.copyProofs(self)
        # stmt.addProof(stmt.value,"NEGATING",proof_type)
        return stmt           

    def loadFromPattern(self,string):
        pos = string.find(">")
        if(pos != -1):
            i=0
            count = 0
            for char in string:
                i+=1
                if(char == "("):
                    count+=1
                if(char == ")"):
                    count-=1
                if(count == 0):
                    break
                
            left = string[1:i-1]
            right = string[i+2  :-1]
            print("L >>> " + left)
            print("R >>> " + right)
            
            self.left = Statement(None,None,'>',None)
            self.left.loadFromPattern(left)
            self.right = Statement(None,None,'>',None)
            self.right.loadFromPattern(right)
            self.genValue()
        else:
            self.operator = None
            self.value = string
            self.genValue()

        self.loadIntoPattern()

    def loadIntoPattern(self,state=""):
        if(self.getValue() in self.pattern.keys()):
            self.pattern[self.getValue()].append(state)
        else:
            self.pattern[self.getValue()] = [state]

        if(self.isStatement()):
            left_pattern = self.left.loadIntoPattern(state+"0")
            right_pattern = self.right.loadIntoPattern(state+"1")
            for pattern,positions in left_pattern.items():
                if(pattern in self.pattern.keys()):
                    self.pattern[pattern] += positions
                else:
                    self.pattern[pattern] = positions

            for pattern,positions in right_pattern.items():
                if(pattern in self.pattern.keys()):
                    self.pattern[pattern] += positions
                else:
                    self.pattern[pattern] = positions
        for pattern,lst in self.pattern.items():
            lst = removeStringDuplicates(lst)
            self.pattern[pattern] = lst
        return self.pattern

    def matchesPattern(self,pattern):
        return

    def copyProofs(self,stmt):
        self.proof += stmt.proof
        self.antiproof = self.antiproof + stmt.antiproof

    def remove_top_negation(self):
        if(self.right.value == False and self.left.isStatement()
            and self.left.right.value == False):
            self.value = self.left.value
            self.operator = self.left.operator
            self.right = copy.deepcopy(self.left.right)
            self.left = copy.deepcopy(self.left.left)
            return True
        return False

    def remove_not_rec(self):
        if(not self.isStatement()):
            return
        if(self.remove_top_negation()):
            self.remove_not_rec()        
        else:
            if(self.isStatement() and self.left.isStatement()):
                self.left.remove_not_rec()
            if(self.isStatement() and self.right.isStatement()):
                self.right.remove_not_rec()


    '''
    PROOF functions
        setHypothesis : sets the current hypothesis as a hypothesis
        addProof : adds a Statement to the proof set
        getProof : gets proof out of the statement set
    '''

    def removeProofDuplicates(self):
        # return
        final_proof = []
        for step in self.proof:
            if (step in final_proof):
                continue
            else:
                final_proof.append(step)
        self.proof = final_proof

        final_proof = []
        for step in self.antiproof:
            if (step in final_proof):
                continue
            else:
                final_proof.append(step)
        self.antiproof = final_proof

    def setHypothesis(self):
        self.addProof(self.value,"Hypothesis")

    def addProof(self,proof_string,proof_reason = "",proof_type = 0):
        if(proof_type == 0):
            self.proof.append([proof_string,proof_reason])
        elif(proof_type == 1):
            self.antiproof.insert(0,[proof_string,proof_reason])
        elif(proof_type == 2):
            self.antiproof.append([proof_string,proof_reason])

    def getProof(self):
        self.removeProofDuplicates()
        proof_string = ""
        for proof_pair in self.proof:
            proof_string += str(proof_pair[0]) + "\t\t... " + str(proof_pair[1]) + "\n"

        for proof_pair in self.antiproof:
            proof_string += str(proof_pair[0]) + "\t\t... " + str(proof_pair[1]) + "\n"
        proof_string = proof_string.replace("(False)","F")
        return proof_string

    '''
        Print Function to Print a Statement
    '''
    def custom_print(self,count=0):
        tab_start = ""
        for i in range(count):
            tab_start += "\t"
        print(tab_start + "V >> " + self.getValue())
        if(self.isStatement()):
            print(tab_start + "LEFT >>")
            self.left.custom_print(count+1)
            print(tab_start + "RIGHT >>")
            self.right.custom_print(count+1)

    def preprocess(self):

        # print("PREPROSESSING" + str(self.value))
        if(self.operator == '.'):
            stmt = Statement(
                copy.deepcopy(self.right),
                self.false_node(),">",
                "("+ self.right.getValue() +")>(False)")
            
            n_right_stmt = Statement(
                copy.deepcopy(self.left),
                stmt,">")
            self.left = copy.deepcopy(n_right_stmt)
            self.operator = ">"
            self.right = self.false_node()
            self.value = "(" + self.left.getValue() + ")>(False)"

        elif(self.operator == '|'):
            print("VALUE  >>>> " + self.getValue())
            stmt = Statement(
                copy.deepcopy(self.left),
                self.false_node(),">",
                "("+ self.left.getValue()+")>(False)")
            self.left = stmt
            # self.left.negation()
            self.value = "(" + self.left.getValue() +")>(" + self.right.getValue() +")"

        # self.remove_not_rec()
        self.genValue()
        
    def isTrueForHypothesisSet(self,hyp_set):
        if(self in hyp_set):
            return True
        return False

    def isTrue(self):
        return self.isPimpliesP() or self.isAxiom1() or self.isAxiom2() or self.isFimpliesA()

    def isFimpliesA(self):
        if(self.isStatement() and self.left.value == False):
            self.addProof(self.getValue(),"F -> A provable",1)
            return True
        return False
        
    def isPimpliesP(self):
        if(self.isStatement() and self.left == self.right):
            self.addProof(self.getValue(),"P -> P provable",1)
            return True
        return False

    def isStatement(self):
        return (self.operator != None)

    def isAxiom1(self):
        #A>(B>A)
        if(not (self.isStatement() and self.right.isStatement())):
            return False
        if(self.left == self.right.right):
            self.addProof(self.getValue(),"Axiom 1",1)
            return True
        return False

    def isAxiom2(self):
        #(A>(B>C))>((A>B)>(A>C))
        if(self.isStatement() and self.left.isStatement() and self.left.right.isStatement() and
            self.right.isStatement() and self.right.left.isStatement() and
            self.right.right.isStatement()):
            if(self.left.left == self.right.left.left and 
                self.left.left == self.right.right.left and
                self.left.right.left == self.right.left.right and
                self.left.right.right == self.right.right.right):
                self.addProof(self.getValue(),"Axiom 2",1)
                return True
        return False


    def contrapositive(self):
        if(self.isStatement()):
            stmt = Statement(self.right.negation(),self.left.negation(),'>')
            stmt.copyProofs(self)
            stmt.addProof(stmt.value,"Contrapositive")
            return stmt
        else:
            return self

    def getValue(self):
        return str(self.value)

    def modusPones(self,stmt):
        reslist = []
        if(stmt == self.left):
            n_stmt = self.right
            n_stmt.copyProofs(self)
            n_stmt.copyProofs(stmt)

            n_stmt.addProof(n_stmt.value,"Modes Pones On (" + stmt.getValue() + "), (" + self.getValue() + ")")
            reslist.append(self.right)
        if(self == stmt.left):
            n_stmt = stmt.right
            n_stmt.copyProofs(self)
            n_stmt.copyProofs(stmt)
            n_stmt.addProof(n_stmt.value,"Modes Pones On (" + self.getValue() + "), (" + stmt.getValue() +")")
            reslist.append(stmt.right)
        return reslist

    def genValue(self):
        if(self.operator == None):
            if(self.value == "F"):
                self.value = False
            return self.getValue()
        self.value = "(" + self.left.genValue() + ")>(" + self.right.genValue() + ")"
        return self.getValue()

        if(n_hyp.hasFormOfAxiom2()):
            n_stmt = n_hyp.convertToAxiom2()

    def convertToAxiom2(self):
        #(A>(B>C))>((A>B)>(A>C))
        stmt = Statement(self.left.left,Statement(self.left.right,self.right.right,'>'),'>')
        stmt.copyProofs(self)
        stmt.addProof(stmt.getValue(),"Applying Axiom 2 and Modes Pones",1)

    def hasFormOfAxiom2(self):
        #(A>(B>C))>((A>B)>(A>C))
        if(self.isStatement() and self.left.isStatement() and self.right.isStatement() 
            and self.left.left == self.right.left):
            return True
        return False

