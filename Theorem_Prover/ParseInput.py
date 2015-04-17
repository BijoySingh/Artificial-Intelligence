from Statement import Statement

input_stack = []

def retrieve_from_stack():
    global input_stack
    iterator = len(input_stack) - 1

    stmt = Statement()
    current_input = ""
    total_input = ""
    current_input_type = False
    operator_found = False

    while(iterator != -1):
        last_element_pair = input_stack.pop()

        last_element_type = last_element_pair[0]
        last_element = last_element_pair[1]
        # print("PROCESSING")
        # print(last_element)
        if(last_element_type):
            total_input = "(" + last_element.value + ")" + total_input
        else:
            total_input = last_element + total_input

        if(last_element_type):
            current_input = last_element
            current_input_type = True

        elif(last_element == '('):    
            total_input = total_input[1:]
            if(not current_input_type):
                stmt.left = Statement()
                stmt.left.value = current_input
            else:
                stmt.left = current_input        
            break

        elif(last_element == '>' or 
            last_element == '.' or
            last_element == '|'):

            stmt.operator = last_element
            stmt.right = current_input
            if(not current_input_type):
                stmt.right = Statement(None,None,None,current_input)

            current_input = ""
            current_input_type = False
            operator_found = True

        elif(last_element == '~'):
            st = current_input
            if(not current_input_type):
                st = Statement(None,None,None,current_input)
            
            current_input = st.negation()
            current_input_type = True

        else:
            current_input = last_element + current_input

        iterator-=1

    if(not operator_found):
        if(current_input_type):
            stmt = current_input
        else:
            stmt = Statement(None,None,None,current_input)
            # return 

    stmt.value = total_input
    stmt.preprocess()
    
    st = stmt

    if(len(input_stack) > 0):
        if(input_stack[len(input_stack) - 1] == '~'):
            input_stack.pop()
            st = stmt.negation()

    input_stack.append((True,st))

def print_stack():
    string_to_print = ""
    for obj in input_stack:
        if(obj[0]):
            string_to_print += ":: STMT : " +obj[1].value
            # print(obj[1].custom_print())
        else:
            string_to_print += ":: " +str(obj[1])
    print(string_to_print)

def parse_input(inp):
    global input_stack
    input_stack = []
    if(inp[0] != '(' or inp[len(inp) - 1] != ')'):
        inp = '(' + inp + ')'
    # inp.replace(" ","")
    for char in inp:
        # print_stack()
        if(char == ')'):
            retrieve_from_stack()
        else:
            input_stack.append((False,char))

    # input_stack[0][1].custom_print()    
    return input_stack[0][1]