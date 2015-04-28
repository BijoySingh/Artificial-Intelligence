from ParseInput import *
from Statement import *
from StatementFunctions import *
from ProvedTheorems import *
import copy

def genHypoList(stmt, acc=[]):
    if(stmt.operator == None):
        if(stmt.value == False):
            return acc
        stmtN = Statement(None,None,None,False)
        acc.append(Statement(stmt, stmtN,'>',
            "(" + str(stmt.value) + ")>(False)"))
        return acc
    acc.append(stmt.left)
    return genHypoList(stmt.right,acc)

def equal(stmt1, stmt2):
    if(stmt1.value == stmt2.value):
        return True
    if(stmt1.operator == None):
        if(stmt2.operator != None):
            return False
        return (stmt1.value == stmt2.value)
    if(stmt2.operator == None):
        return False
    return (equal(stmt1.left,stmt2.left) 
        and equal(stmt1.right, stmt2.right))

def updateProvedStatements():
    theorem_file = open("ProvedTheorems.py","w")
    theorem_file.write("proved_theorems = " + str(proved_theorems))
    theorem_file.close()

str_display = "Propositional Calculus Theorem Prover\n"
str_display += "120050006   Manik Dhar\n"
str_display += "120050068   Sai Kiran Mudulkar\n"
str_display += "120050087   Bijoy Singh Kochar\n\n"

str_display += "--- F           : symbol reserved for False\n"
str_display += "--- a,b,c,p,q   : variables\n"
str_display += "---  >          : implication\n"
str_display += "--- ( )         : parenthesis\n"
str_display += "--- ~           : not\n"
str_display += "--- .           : and\n"
str_display += "--- |           : or\n\n"

str_display += "Please Enter Input Propositional Statement"

print(str_display)
# input_str = str(input())
# input_str = "(((~a)>b)>((a>b)>b))"
# input_str = "(a>(b>a))"
# input_str = "((p>q)>((~p>q)>q))"
# input_str = "((p.q)>(p|q))"
# input_str = "((A>(B>C))>(D>((A>B)>(A>C))))"
# input_str = "(((A>B)>(A>C))>(D>(A>(B>C))))"
# input_str = "(F>F)"
# input_str = "(A>(B>(C>(D>E))))"

#DeMorgan's :Law 1
# input_str = "((~(A|B))>((~A).(~B)))"
# input_str = "((~(A.B))>((~A)|(~B)))"
# input_str = "(((~A)|(~B))>(~(A.B)))"
# input_str = "(((~A).(~B))>(~(A|B)))"

#Special TestCase
input_str = "(((p>q)>((r>s)>t))>((u>((r>s)>t))>((p>u)>(s>t))))"
# input_str = "(((p>q)>A)>((~p)>A))"
# input_str = "(((p>A).((~p)>A))>A)"


print("\n<< PARSING >>")
# print("++++++++++")
stmt = parse_input(input_str)
print(stmt.value)
# print("++++++++++")
print("\n..Done..")


print("\n<< DEDUCING >>")
accumulator = genHypoList(stmt)
for obj in accumulator:
    obj.setHypothesis()
    print(obj.value)
print("\n..Done..")

print("\n<< MODES PONES >>")
accumulator = recursiveModusPones(accumulator)
for obj in accumulator:
    print(obj.value)
print("\n..Done..")

print("\n<< THEROEM PROVING >>")

recurse_mode = False
recurse_list = []

while(True):
    added_hypotheses = []
    n_accumulator = copy.deepcopy(accumulator)
    if(recurse_mode):
        if(len(recurse_list) > 0):
            added_hypotheses = recurse_list.pop(0)
            for st in added_hypotheses:
                print("Proving " + st.getValue())
                n_accumulator = genHypoList(st,n_accumulator)
                # n_accumulator.append(st)
            if(len(removeDuplicates(n_accumulator)) == len(removeDuplicates(accumulator))):
                #Same
                print("Useless Addition")
                continue
            n_accumulator = recursiveModusPones(n_accumulator)
        else:
            recurse_mode = False
    result = StartSolving(n_accumulator)

    if(result[0]):
        for st in added_hypotheses:
            print("\n\n\nProve Till Here Requiring " + st.getValue())
            print(st.getProof())

        print("Final Node :" + result[1].getValue() + "\n")
        print(result[1].getProof())
        if(result[1].value != False):
            print(result[1].getValue() + " |- False")
        '''
        if(stmt.getValue() not in proved_theorems):
            proved_theorems.append(stmt.getValue())
        updateProvedStatements()
        '''
        break

    else:
        if(not recurse_mode):
            print("Could Not Prove. Choose a new Hypothesis from the following")
            print(str(-1) + ") Add a new Hypothesis")
            print(str(0) + ") Try them on automatically")
            i = 1
            for stmt in result[1]:
                print(str(i) + ") " + stmt[0].getValue())
                i+=1
        pos = 0
        if(not recurse_mode):
            pos = int(input("Enter Option\n"))

        if(pos == 0):
            recurse_mode = True
            append_to_recurse_list = []
            for st in result[1]:
                copied_added_hyp = copy.deepcopy(added_hypotheses)
                copied_added_hyp.append(st[0])
                append_to_recurse_list.append(copied_added_hyp)
            recurse_list = recurse_list + append_to_recurse_list
        elif(pos == -1):
            input_str = str(raw_input("Enter New Hypothesis\n"))
            stmt_new = parse_input(input_str)
            accumulator.append(stmt_new)

            for obj in accumulator:
                obj.setHypothesis()
                print(obj.getValue())
            accumulator = recursiveModusPones(accumulator)
                
        else:
            stmt_new = result[1][pos-1][0]
            print(stmt_new.getProof())
            # accumulator.append(stmt_new)

            print("Prove Till Requiring " + stmt_new.getValue())
            print(stmt_new.getProof())
            accumulator = genHypoList(stmt_new,accumulator)
            accumulator = recursiveModusPones(accumulator)
print("\n..Done..")

