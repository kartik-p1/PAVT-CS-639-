from z3 import *
import argparse
import json
import sys

sys.path.insert(0, '../KachuaCore/')

from sExecutionInterface import *
import z3solver as zs
from irgen import *
from interpreter import *
import ast

def example(s):
    # To add symbolic variable x to solver
    s.addSymbVar('x')
    s.addSymbVar('y')
    # To add constraint in form of string
    s.addConstraint('Implies(x==5+y,x==5)')
    s.addConstraint('And(x==y,x>5)')
    # s.addConstraint('Implies(x==4,y==x+8')
    # To access solvers directly use s.s.<function of z3>()
    print("constraints added till now",s.s.assertions())
    # To assign z=x+y
    s.addAssignment('z','x+y')
    # To get any variable assigned
    print("variable assignment of z =",s.getVar('z'))


def checkEq(args,ir):

    file1 = open("../Submission/testData1.json","r+")
    testData1=json.loads(file1.read())
    file1.close()

    file2 = open("../Submission/testData2.json","r+")
    testData2=json.loads(file2.read())
    file2.close()

    #print("Sdasd")

    s = zs.z3Solver()

    testData1 = convertTestData(testData1)
    # print(testData1)

    
    testData2 = convertTestData(testData2)
    # print(testData2)
    # TODO: write code to check equivalence


    params_keys = []

    # Add keys from testData1
    for value in testData1.values():
        params_keys += list(value['params'].keys())

    # Add keys from testData2
    for value in testData2.values():
        params_keys += list(value['params'].keys())

    # Remove duplicates
    params_keys = list(set(params_keys))


    # s.addSymbVar(params_keys)
    # print(params_keys)
    
    for key in params_keys:
        s.addSymbVar(key)

    mapping = {chr(i): f'o{i-96}' for i in range(97, 123)}
    # print("mapping", mapping)
    
    # Initialize lists for parameters and symbolic encodings
    parameters = []
    Symb1 = []
    
    # Extract parameters and symbolic encodings
    for key, value in testData2.items():
        parameters.append(value.get("params"))
        Symb1.append(value.get("symbEnc"))

    # Perform variable substitution
    substituted_outputs = []

    for i in range(len(parameters)):
        output_dict = Symb1[i]
        input_dict = parameters[i]
        substituted_output = []

        for key, value in output_dict.items():
            for var, var_value in input_dict.items():
                if var in value:
                    value = value.replace(var, str(var_value))

            # Create the substituted expression
            expression = f"{key}=={value}"
            substituted_output.append(expression)

        substituted_outputs.append(substituted_output)

    substituted_outputs = [[expr.replace(" ", "") for expr in expr_list] for expr_list in substituted_outputs]
    # Print the list of substituted expressions
    # print(substituted_outputs)
    list_output = []
    for inner_list in substituted_outputs:
       
        s1 = zs.z3Solver()
        for key in params_keys:
            
            s.addSymbVar(key)
            for expression in inner_list:
                s.addConstraint(expression)

        res = s.s.check()
        # print(s.s.assertions())
        # print("res ",res)
        if str(res)=="sat":
            m = s.s.model()
            #print("model printing",m)
            list_output.append(m)
            s.s.reset()
    # print("L")
    print(parameters)
    # print(Symb1)
    print("list_output")
    print(list_output)
    # print("l")
    
    
    
    constparams = []
    for key, value in testData1.items():
        constparams.append(value.get("constparams"))
        break
    constparams = constparams[0]
    
    print("constparams")    
    constparams = [param[1:] for param in constparams]
    print(constparams)
    # print(type(constparams[0][0]))
    symbEnc = []
    
    for key, value in testData1.items():
        symbEnc.append(value.get("symbEnc"))
    
    # print(symbEnc)

    
    
    # print(symbEnc)

    processed_symbEnc = []
    for symb_dict in symbEnc:
        # print(symb_dict)

        processed_symb_list = [f"{key}=={value}" for key, value in symb_dict.items()]

        processed_symb_list = [item for item in processed_symb_list if item.split("==")[0] not in constparams]

        processed_symbEnc.append(eval(str(processed_symb_list)))

    # Print the processed symbEnc
    processed_symbEnc = [[expr.replace(" ", "") for expr in expr_list] for expr_list in processed_symbEnc]
    print("SymbEnc")
    print(processed_symbEnc)

    constraints = []
    for key, value in testData1.items():
        constraint_strings = value.get("constraints")
        for constraint_string in constraint_strings:
            # Split the string using ', ' only if it's present
            split_constraints = [c.strip() for c in constraint_string.split(', ')]
            constraints.append(split_constraints)

    # Print the processed constraints
    # print(constraints)

    x = Int('x')
    y = Int('y')
    z = Int('z')
    c1 = Int('c1')
    c2 = Int('c2')
    c3 = Int('c3')
    # x1 = Int('x1')
    # for key, value in mapping.items():
    #     if isinstance(value, str):
            
    #         exec(f"{value} = Int('{value}')")
    #         s.addSymbVar(eval(value) == 0)    
    s.addSymbVar('o1')
    o1 = Int('o1')
    s.addSymbVar('o2')
    o2 = Int('o2')
    s.addSymbVar('o3')
    o3 = Int('o3')

    s1 = Solver()

    And_expr=[]
    expr=[]
    for i in processed_symbEnc:
        A=True
        expr1={}
        for j in i:
            
            print(j) 
            # print("hwllo")
            
            
            temp = ""
            if str(j)[0] == 'x':
                temp = "o2" + str(j)[1:]
                expr1["o2"] = str(j)[3:]
            elif str(j)[0] == 'z':
                temp = "o3" + str(j)[1:]
                expr1["o3"] = str(j)[3:]
            else:
                temp = "o1" + str(j)[1:]
                expr1["o1"] = str(j)[3:]

            A = And(A,eval(temp))
        And_expr.append(A)
        expr.append(expr1)
    print("Expr", expr)

    And_cons=[]
    for i in constraints:
        #print(i)
        A=True
        for j in i:
            A = And(A,eval(str(j)))
        And_cons.append(A)
    # print("And_Expr")
    # print(And_expr)
    print("And_Cons")
    print(And_cons)
    I = True
    j=True
    And_J=[]

    for i in range(0,len(And_cons)):
        I = Implies(And_cons[i] , And_expr[i])
        j = And(j,I)
        And_J.append(eval(str(I)))
    # print("lalala")
    # print(j)
    # print("And_J", And_J)
    pc = j


    

    # for i in l1:
    #     A=True
    #     for j in i:
    #         A = And(A,j)
    #     And_l1.append(A)
    # print("sadsad")
    # print(And_l1)
   

    l1=[]
    for i in parameters:
        l=[]
        for k,v in i.items():
            if str(k) in constparams:
                continue
            l.append(eval(str(k) + "==" + str(v)))
        l1.append(l)
    # print(l1)

    And_l1=[]

    for i in l1:
        A=True
        for j in i:
            A = And(A,j)
        And_l1.append(A)
    print("sadsad")
    print(And_l1)
    And_ip = And_l1

    # print(type(parameters[0]))
    # print(list_output)
    
    outputs = []
    outputs_string = []
    
    for i in list_output:
        temp = []
        temp1 = {}
        for d in i.decls():
            if str(d) in constparams:
                continue
            if(str(d) == 'y'):
                temp1['o1'] = str(i[d])
            elif(str(d) == 'x'):
                temp1['o2'] = str(i[d])
            elif(str(d) == 'z'):
                temp1['o3'] = str(i[d])
            # else:
            #     temp1['o4'] = str(i[d])
        for d in i.decls():
            if str(d) in constparams:
                continue
            if(str(d) == 'y'):
                temp.append(eval('o1' + "==" + str(i[d])))
            elif(str(d) == 'x'):
                temp.append(eval('o2' + "==" + str(i[d])))
            elif(str(d) == 'z'):
                temp.append(eval('o3' + "==" + str(i[d])))
            else:
                temp.append(eval(str(d) + "==" + str(i[d])))
            #print(d,i[d])
        outputs.append(temp)
        outputs_string.append(temp1)
    print("opopopopop")
    print(outputs)
    print(outputs_string)

    # Expr [{'o2': 'x', 'o1': 'x+c1+20'}, {'o2': 'x', 'o1': 'x+c1'}, {'o2': 'x', 'o1': 'x+c2'}]
    # outputs_string [{'o1': '40', 'o2': '5'}, {'o1': '40', 'o2': '25'}, {'o1': '68', 'o2': '43'}]
    expression = []
    for i in range(len(outputs_string)):
        # print(outputs_string[i])
        # print(expr[i])
        # temp = {}
        temp2 = []
        for k1,v1 in expr[i].items():
            for k2,v2 in outputs_string[i].items():
                if k1 == k2:
                    # print(k1, k2)
                    temp_str = v1 + "==" + v2
                    temp2.append(eval(str(temp_str)))
                    # temp[v1] = v2
        expression.append(temp2)
    
    print("expression",expression)





    # new_op = []
    # for i in range 
    # for i in range(len(expr)):
    #     expr_list = expr[i]
    #     outputs_list = outputs_string[i]
    
    And_op=[]

    for i in outputs:
        A=True
        for j in i:
            A = And(A,j)
        And_op.append(A)
    # print("op")
    # print(And_op)
    

    s2 = Solver()
    x = Int('x')
    y = Int('y')
    z = Int('z')
    c1 = Int('c1')
    c2 = Int('c2')
    c3 = Int('c3')
    o1 = Int('o1')
    o2 = Int('o2')
    o3 = Int('o3')

    print("And_ip", And_ip)
    print("And_cons", And_cons)
    print("And_op", And_op)
    print("constraints", constraints)

    for i in range(0, len(And_ip)):
        
        for j in range(len(constraints)):
            
            s1.reset()

            s1.add(And_ip[i])
            s1.add(And_cons[j])
            # for k in range(len(constraints[j])):
            #     s1.add(eval(str(constraints[j][k])))
            
            if s1.check() == sat:
                # print("\n",Implies(And(And_op[i],And_ip[i]),And_expr[j]))

                s2.add(Implies((And_op[i]),And(And_expr[j],And_ip[i])))

                
                # for k in expression[i]:
                #     s2.add(k)
        
        
        

        # for j in range(0, len(And_cons)):

        #     s1.reset()
        #     s1.add((Implies(And_ip[i], And_cons[j])))
        #     result = s1.check()

        #     if result == sat:
        #         print("CID")
        #         print(Implies(And(And_op[i],And_ip[i]),And_expr[j]))
        #         s2.add(Implies(And(And_op[i],And_ip[i]),And_expr[j]))
    print(s2)
    result = s2.check()
    print("res",result)
    if result == sat:
        # If the formula is satisfiable, retrieve the satisfying model
        model = s2.model()
        print("model",model)
        print(model.eval(c1))
        x_value = model[x]
        y_value = model[y]
        z_value = model[z]
        c1_value = model[c1]
        c2_value = model[c2]
        c3_value = model[c3]

        print("Satisfying values:")
        print("x =", x_value)
        print("y =", y_value)
        print("z =", z_value)
        print("c1 =", c1_value)
        print("c2 =", c2_value)
        print("c3 =", c3_value)
                


    # print("pc", pc)
    # s.s.reset()
    # for i in range(0, len(outputs)):
    #     # print("lolo")
    #     temp = And(pc, And_op[i])
    #     # print(pc)
    #     # print("hello")
    #     print((Implies(And_l1[i], temp)))
    #     s1.add((Implies(And_l1[i], temp)))


    # else:
    #     # If the formula is unsatisfiable, no satisfying values exist
    #     print("No satisfying values found.")

    # res = s.s.check()
    # print(s.s.assertions())
    # # print("res ",res)
    # if str(res)=="sat":
    #     m = s.s.model()
    #     print("model printing",m)
    # else: print("unsat")
    
    # hello

    # s.addConstraint(str(And(Implies(And(And(And(And(True, x == 5), y == 100),),
    #             ),
    #         And(And(And(True,
    #                     Implies(And(And(True, x <= 42),
    #                                 Not(False)),
    #                             And(And(And(And(True, x == x),
    #                                         y == x + c1),
    #                                     ),
    #                                 ))),
    #                 Implies(And(True, Not(x <= 42)),
    #                         And(And(And(And(True, x == x),
    #                                     y == x + c2),
    #                                 ),
    #                             ))),
    #             And(And(True, y == 45), x == 5)))),
    # (Implies(And(And(And(And(True, x == 43), y == 100),),
    #             ),
    #         And(And(And(True,
    #                     Implies(And(And(True, x <= 42),
    #                                 Not(False)),
    #                             And(And(And(And(True, x == x),
    #                                         y == x + c1),
    #                                     ),
    #                                 ))),
    #                 Implies(And(True, Not(x <= 42)),
    #                         And(And(And(And(True, x == x),
    #                                     y == x + c2),
    #                                 ),
    #                             ))),
    #             And(And(True, y == 65), x == 43))))))
    # Create a simple function declaration

    # res = s.s.check()
    # print(s.s.assertions())
    # # print("res ",res)
    # if str(res)=="sat":
    #     m = s.s.model()
    #     print("model printing",m)
    # else: print("unsat")


 


       
       



    
    


    
    # for key, value in testData1.items():
    #     symbEnc_data1 = value.get("symbEnc", {})
    #     all_keys.update(symbEnc_data1.keys())

    # for key, value in testData2.items():
    #     symbEnc_data2 = value.get("symbEnc", {})
    #     all_keys.update(symbEnc_data2.keys())
    
    # equation_strings = []

    # for key1, value1 in testData1.items():
    #     constraints1 = value1["constraints"]

    #     for key2, value2 in testData2.items():
    #         constraints2 = value2.get("constraints", [])

    #         # Compare constraints
    #         if set(constraints1) == set(constraints2):
    #             symbEnc_data1 = value1.get("symbEnc", {})
    #             symbEnc_data2 = value2.get("symbEnc", {})

    #             # Loop through keys in symbEnc_data
    #             for key in symbEnc_data1.keys():
    #                 if key in symbEnc_data2:
    #                     val1 = symbEnc_data1[key]
    #                     val2 = symbEnc_data2[key]
    #                     equation = f"{val1} == {val2}"
    #                     equation_strings.append(equation)

    # for key1, value1 in testData1.items():
        
    #     constraints1 = value1["constraints"]
    #     symbEnc_data1 = value1.get("symbEnc", {})
        
        
        
    #     for key2, value2 in testData2.items():
    #         constraints2 = value2.get("constraints", [])
    #         symbEnc_data2 = value2.get("symbEnc", "{}")


    #         if set(constraints1) == set(constraints2):

    # Iterate through all keys in testData1
    # for key1, value1 in testData1.items():
    #     constraints1 = value1["constraints"]  # Extract constraints from testData1

    #     # Iterate through all keys in testData2
    #     for key2, value2 in testData2.items():
    #         constraints2 = value2.get("constraints", [])  # Extract constraints from testData2
    #         #print("sdasdasdsa")
    #         if set(constraints1) == set(constraints2):
    #             #   print("lalala")
    #             
    #             symbEnc_data1[key1] = value1["symbEnc"]# Extract symbEnc from testData1
    #             symbEnc_data2[key2] = value2.get("symbEnc", "{}")  # Extract symbEnc from testData2

                # print(f"symbEnc_data1: {symbEnc_data1}")
                # print(f"symbEnc_data2: {symbEnc_data2}")

                
                

    
                # symbEnc_strings1 = set(f'{k}=={v}' for data in [symbEnc_data1] for key, value in data.items() for k, v in value.items())
                # symbEnc_strings2 = set(f'{k}=={v}' for data in [symbEnc_data2] for key, value in data.items() for k, v in value.items())





                # print("hello")
                # print(symbEnc_strings)

                    

                
    # print("Stored Equations:")
    # for eq in equation_strings:
    #     print(eq)

    # for constraint_string in equation_strings:
    #     constraint_string = constraint_string.replace(' ', '')
    #     # print(constraint_string)
    #     s.addConstraint(constraint_string)
    
    # res = s.s.check()
    # # print(s.s.assertions())
    # # print("res ",res)
    # if str(res)=="sat":
    #     m = s.s.model()
    #     print("model printing",m)

    # Define a function to extract and solve symbolic equations
# Initialize dictionary for results   
    # print("symbEnc_strings") 
    # print(symbEnc_strings)
   

    #s.addConstraint(symbEnc_strings)
    #print(params_keys)

    

    
    
    

   


if __name__ == '__main__':
    cmdparser = argparse.ArgumentParser(
        description='symbSubmission for assignment Program Synthesis using Symbolic Execution')
    cmdparser.add_argument('progfl')
    cmdparser.add_argument(
        '-b', '--bin', action='store_true', help='load binary IR')
    cmdparser.add_argument(
        '-e', '--output', default=list(), type=ast.literal_eval,
                            help="pass variables to kachua program in python dictionary format")
    args = cmdparser.parse_args()
    ir = loadIR(args.progfl)
    checkEq(args,ir)
    exit()
