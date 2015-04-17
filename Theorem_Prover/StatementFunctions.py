import copy
from Statement import *
from ProvedTheorems import *

'''
def loadProvedStatements():
    prevProvedPatterns = []
    for strStmt in proved_theorems:
        stmt = Statement(None,None,'>',None)
        stmt.loadFromPattern(strStmt)
        prevProvedPatterns.append(stmt)
    return prevProvedPatterns

prevProvedPatterns = loadProvedStatements()
print(prevProvedPatterns[0].pattern)
'''

def StartSolving(accumulator):
    seen_dict = dict()
    exhausted = []
    queue = [[e.negation(),1] for e in accumulator]
    for stmt in accumulator:
        if(stmt.value == False):
            return [True,stmt]
    print("..BackTracking")

    while(len(queue) > 0):
        n_hyp_p = queue.pop(0)
        o_hyp = copy.deepcopy(n_hyp_p)
        n_hyp = n_hyp_p[0]
        depth = n_hyp_p[1]

        # print("TRYING : " + n_hyp.getValue() + " : " + str(depth))
        # print(n_hyp.getProof())

        # n_hyp.addProof(n_hyp.getValue(),"TRYING TO SOLVE")
        
        #proof finished
        #generate proof
        if(n_hyp.getValue() in seen_dict.keys()):
            continue

        seen_dict[n_hyp.getValue()] = True

        if(n_hyp.hasFormOfAxiom2()):
            n_stmt = n_hyp.convertToAxiom2()
            queue.append([n_stmt,depth+1])

        if(n_hyp.value == False):
            continue
        if(n_hyp.isTrue()):
            return [True,n_hyp]
        if(n_hyp.isTrueForHypothesisSet(accumulator)):
            n_hyp.addProof(n_hyp.getValue()," is a Hypothesis",1)
            return [True,n_hyp]
        if(n_hyp.isStatement()):
            n_stmt = copy.deepcopy(n_hyp.right)
            n_stmt.copyProofs(n_hyp)
            if(n_stmt.isTrue()):
                return [True,n_stmt]
            if(n_stmt.isTrueForHypothesisSet(accumulator)):
                n_stmt.addProof(
                    n_hyp.getValue(),
                    "D)",1)
                n_stmt.addProof(
                    Statement(n_hyp.right, n_hyp, '>').getValue(),
                    "C) Apply Axiom 1",1)
                n_stmt.addProof(
                    n_hyp.right.getValue(),
                    "Hypothesis",1)
                return [True,n_stmt]
        if(n_hyp.isStatement()):
            n_stmt = n_hyp.left.negation()
            n_stmt.copyProofs(n_hyp)
            if(n_stmt.isTrue()):                
                return [True,n_stmt]
            if(n_stmt.isTrueForHypothesisSet(accumulator)):
                n_stmt.addProof(
                    n_hyp.getValue(),
                    "vi) Apply Contrapositve",1)
                tmp = n_hyp.contrapositive()
                n_stmt.addProof(
                    tmp.getValue(),
                    "v) Modus Ponens",1)
                n_stmt.addProof(
                    Statement(tmp.right,tmp,'>').getValue(),
                    "iv) Apply Axiom 1",1)
                n_stmt.addProof(
                    (tmp.right).getValue(),
                    "iii) Modus Ponens",1)          
                return [True,n_stmt]

        found_something = False
        for hyp in accumulator:
            if(n_hyp == hyp.right):
                #left in queue
                n_stmt = copy.deepcopy(hyp.left)
                n_stmt.copyProofs(n_hyp)
                n_stmt.copyProofs(hyp)
                n_stmt.addProof(
                    n_hyp.getValue(),
                    "Modes Ponens On " + hyp.left.getValue() + ", " + hyp.getValue(), 1)
                queue.append([n_stmt,depth+1])
                found_something = True
            
            elif(n_hyp.isStatement() and n_hyp.right == hyp.right):
                #lhs of hyp in queue
                n_stmt = copy.deepcopy(hyp.left)
                n_stmt.copyProofs(n_hyp)
                # n_stmt.copyProofs(hyp)
                n_stmt.addProof(
                    n_hyp.getValue(),
                    "D)",1)
                n_stmt.addProof(
                    Statement(n_hyp.right, n_hyp, '>').getValue(),
                    "C) Apply Axiom 1",1)
                n_stmt.addProof(
                    hyp.getValue(),
                    "B)",1)
                n_stmt.addProof(
                    hyp.left.getValue(),
                    n_hyp.getValue() + "(A)",1)
                queue.append([n_stmt,depth+1])
                found_something = True

            elif(n_hyp.isStatement() and n_hyp.left.negation() == hyp.right):
                #lhs in queue
                n_stmt = copy.deepcopy(hyp.left)
                n_stmt.copyProofs(n_hyp)
                n_stmt.copyProofs(hyp)
                n_stmt.addProof(
                    n_hyp.getValue(),
                    "vi) Apply Contrapositve",1)
                tmp = n_hyp.contrapositive()
                n_stmt.addProof(
                    tmp.getValue(),
                    "v) Modus Ponens",1)
                n_stmt.addProof(
                    Statement(tmp.right,tmp,'>').getValue(),
                    "iv) Apply Axiom 1",1)
                n_stmt.addProof(
                    (tmp.right).getValue(),
                    "iii) Modus Ponens",1)
                n_stmt.addProof(
                    hyp.getValue(),
                    "ii)",1)
                n_stmt.addProof(
                    (hyp.left).getValue(),
                    "i)",1)
                queue.append([n_stmt,depth+1])
                found_something = True

        # if(not found_something):
        exhausted.append(o_hyp)

    return [False,exhausted,accumulator]

def removeDuplicates(lst):
    seen = set()
    seen_add = seen.add
    return [ x for x in lst if not (x.value in seen or seen_add(x.value))]    

def repeatedContapostiveAppend(lst):
    while(True):
        intial_sz = len(lst)
        contra = [elem.contrapositive() for elem in lst]
        lst += contra
        lst = removeDuplicates(lst)
        if(len(lst) == intial_sz):
            return lst



def recursiveModusPones(stmt_lst):
    checked_list = []
    unchecked_list = stmt_lst
    tmp_checked_list = []
    tmp_unchecked_list = []    
    seen_dict = dict()
    while(True):
        #contrapositive in unchecklist
        '''
        contra = [elem.contrapositive() for elem in unchecked_list]
        unchecked_list += contra
        unchecked_list = removeDuplicates(unchecked_list)
        '''
        unchecked_list = repeatedContapostiveAppend(unchecked_list)

        #iterate over unchecklist 
        while(len(unchecked_list) > 0):
            stmt = unchecked_list.pop()

            #to see MP in checklist and unchecklist
            for stm in unchecked_list:
                #add every new to tmp_unchecked_list
                tmp_unchecked_list += stmt.modusPones(stm)
            for stm in checked_list:
                #add every new to tmp_unchecked_list
                tmp_unchecked_list += stmt.modusPones(stm)
        #after all are done this to tmp_checked
            tmp_checked_list.append(stmt)


        #move tmp_checked to checked
        checked_list = checked_list + tmp_checked_list

        checked_lst = removeDuplicates(checked_list)
        #if tmp_unchecked == [] break
        #else add to unchecked
        if(len(tmp_unchecked_list) == 0):
            break
        else:
            unchecked_list = []
            for i in tmp_unchecked_list:
                if(i not in checked_list):
                    unchecked_list.append(i)
            # unchecked_list = tmp_unchecked_list
            tmp_unchecked_list = []

    return removeDuplicates(checked_list)
    # return checked_list
