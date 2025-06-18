# # thisdict = {
# #     "brand" : "aston martin",
# #     "model" : "db11",
# #     "year" : 2020,
# # }
# # thisdict.pop("model")
# # print(thisdict)
# # thisdict.popitem()
# # print(thisdict)
# # del(thisdict["brand"])
# # print(thisdict)
# # this = {
# #     "brand" : "aston martin",
# #     "model" : "db11",
# #     "year" : 2020,
# #     "color" : "red",
# #     "engine" : "v8",
# #     "horsepower" : 503,
# #     "torque" : 498,
# #     "weight" : 3855,
# #     "top_speed" : 208,
# # }
# # this.copy()
# # thisdict = {
# #     "brand" : "aston martin",
# #     "model" : "db11",
# #     "year" : 2020,
# # }
# # thisdict.clear()
# # print(thisdict)
# # this.items()
# # print(this)
# # this.fromkeys(thisdict)
# # print(this)
# # car = {
# #     "brand" : "aston martin",
# #     "model" : "db11",
# #     "year" : 2020,
# #     "color" : "red",
# # }
# # mydict = car.copy()
# # print(mydict)
# # qwerty = {
# #     "brand" : "aston martin",
# #     "model" : "db11",
# #     "year" : 2020,
# #     "color" : "red",
# #     "engine" : ["v8", "v12"],
# #     "horsepower" : 503,
# #     "weight" : 3855,
# #     "top_speed" : 208,
# #     "acceleration" : 0.0,
# #     "braking" : 0.0,
# #     "handling" : 0.0,
# #     "comfort" : 0.0,
# # }
# # qwerty.fromkeys("engine")
# # print(qwerty)
# # returnq = {
# #     "name" : "agrim ",
# #     "second_name" : "jain",
# #     "age" : 20,
# # }
# # returnq.popitem()
# # print(returnq)  
# # returnq.pop("name")
# # print(returnq)
# # \
# # def my_function():
# #     return 3 * 2
# # print(my_function())

# # my_list = [1,2,3,4,5]
# # my_list.pop(2)
# # print(my_list)
# # my_list.pop(0)
# # print(my_list)
# # my_list.pop
# # print(my_list)

# # print(my_list[-1])

# # list = ["agrim" , "jain" , "20" , "28 ", "june" , "2005"]
# # print(list[2:6]     )
# # def my_function(f_name , last_name):
# #     name_1 = f_name.title()
# #     name_2 = last_name.title()
# #     return f"hello {name_1} {name_2}"
# # print(my_function("agrim" , "jain"))
# # def function_1(text):
# #     return text + text
# # def function_2(text):
# #     return text.title()
# # output  = function_2(function_1("agrim"))
# # print(output)

# #Functions with Outputs
# def format_name(f_name, l_name):
#   if f_name == "" or l_name == "":
#     return "You didn't provide valid inputs."
#   formated_f_name = f_name.title()
#   formated_l_name = l_name.title()
#   f"Result: {formated_f_name} {formated_l_name}"

# #Storing output in a variable
# formatted_name = format_name(input("Your first name: "), input("Your last name: "))
# print(formatted_name)
# #or printing output directly
# print(format_name(input("What is your first name? "), input("What is your last name? ")))

# #Already used functions with outputs.
# length = len(formatted_name)

# #Return as an early exit
# def format_name(f_name, l_name):
#   """Take a first and last name and format it 
#   to return the title case version of the name."""
#   if f_name == "" or l_name == "":
#     return "You didn't provide valid inputs."
#   formated_f_name = f_name.title()
#   formated_l_name = l_name.title()
#   return f"Result: {formated_f_name} {formated_l_name}"


def function_1(text):
    return text + text
def funtion_2(text):
    return text.title()
print(function_1("agrim"))
print(funtion_2("agrim"))




""" code of calculator """

def add(n1 , n2):
    return n1 + n2
def subtract(n1 , n2):
    return n1 - n2
def multiply (n1 , n2):
    return n1 * n2
def divide(n1 , n2):
    return n1 / n2 
def calculator():
    art = r"""                                   ...::::....                                           
                    .=++***********************************************++++=:                     
                  +*#############*###**********#*******************************=                  
                 +***=----====++==+++=====+++=+++++++++++=++++=++=========-=+#*+=                 
                 +**.      -   =   .    . .   .         : . : .      .   :   -*+=                 
                .+**       -   =   : .                  . . : -      :   :   :*+-                 
                .+#*               -          .             : .              .*+-                 
                .*#*               -   .                    : : -            .*+-                 
                .*#*      . :      =   .                    . : -   . .       *+-                 
                .*%*         -:  --      .-   -.      ::  .:  .:       :      ##=                 
                .#@@%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#%%%%#################%%*.                
                :#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@*.                
                .*####################################**************************=.                
                :***************+++++++###********##****************************+:                
                -***=::::::::::::::::::*+ -.. ..       .=*=-+=:=--**+........:**+=                
                -***=::::::::::::::::::**=-:==-=---:-===+*==+---=-**+.. ... ..**++                
                =*##################*#*******************************=-:::::-=**++                
                +*##########################************************************++                
                +*##**-=.=:=*####* +:=++**##*+::  .:-*****=:.=.:*****+.:=.:-:+**++                
                ***#*++. : -*####* .-==+**###+...:.--+*##*=-:.-***#*#+ =  =:=+***+                
                ****#%%%%%%%%####%%%%%%%%####%%%%%%%%##*#%%%%%%%%#***%%%%%%%##***+                
                **************###**************************##*##*****************+.               
                ****:        :*#-        .+#+         =*#****.+***#***+= .+******+:               
                ****:        :*#-        .+#+         =##***+ =***#*##++..=+*****+-               
                ****:        -*#-        .+#+         =###%%%%%%%#***#%%%%%%%#***+=               
                **##=--------+##*=========*#*=--------*#*****##*#****************++               
                **#*=--=====-+##+---====-=*#*=--------+*#***-. =*****#++---+*****++               
                **#*.        -*#:        .+#+         =###**:..-*****%*++-::+****++               
                **#+.        -*#:        .+#+         -**#%%%%#####**#%%#######**+=               
               .***+.        =*#:        .+#+         -**************************+=               
               :**#*-::::::::+##+::::::::-*#*=-::::---+****++=++***#***+=-::-+***+=               
               :****+++++++++*##+=========*#*+++++++==**##*********#*%*+: +*******=.              
               -**#-         +##.        .+#+.        :**#@@%%%%@@#**#%@%%%%%%#***=:              
               =*##-         +##.        .+#+.        :******#********************=-              
               +*##:         +##.        .+#+.        :+***********#**#+++++******==              
               +*##+=======+=###++++++++++*##+===++++++*#**+*******#*#+++++*******==              
               **##=:::::::::*#*=::::::::-**+-::::::..=*##*++- +***#*#*++----+****==              
               **##:         +##          +#+         :*##*=.   :****#*+=   .-****==              
               **##:         +##         .+#+         .+##*+++.+*****##++++++*****=-              
               **##:         *##          +#+.        .+*#*++++*******%+++++******+-              
               **##-.........*##:........:+#*:........:+*#%#**####%#**#%**********=-              
               ++*##################################*****************************+::              
                *%%####################*#####***********************************+-=               
                 .*####%%%%%%%%%%%%%%%%%#####################%%%%%%%%%%%%%%###%#+:                
                         .:-==++++++******###############*****++++====-.          """
    print(art)
    print("welcome to th calculator")
    print("please select operation")
    print("1. add")
    print("2. subtract")
    print("3. multiply")
    print("4. divide")
    operation = input("please select operation: ")
    n1 = float(input("please enter first number: "))
    n2 = float(input("please enter second number: "))
    if operation == "1":
        print(add(n1 , n2))
    elif operation == "2":
        print(subtract(n1 , n2))
    elif operation == "3":
        print(multiply(n1 , n2))
    elif operation == "4":
        print(divide(n1 , n2))
    else:
        print("invalid operation")
calculator()