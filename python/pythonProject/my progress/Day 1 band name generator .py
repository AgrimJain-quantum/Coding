# band name generator
city = input("what is the name of the city ?")
print(city)
name = input("what is your name ?")
print(name)
print("your band name is " + city + " "+ name)



print("hello world \nhello world")
print("hello" + " " + "world")
print("hello",end=" ")
print("world")
bmi = 84 / (1.8 ** 2)
print(bmi)
print(int(bmi))
print(round(bmi))
print(round(bmi,2))
print(f"your bmi is {bmi}")
print("your bmi is " + str(bmi))    
print("your bmi is " + str(int(bmi)))
print("your bmi is " + str(round(bmi)))
print("your bmi is " + str(round(bmi,2)))



if bmi < 18.5:
    print("underweight")
elif bmi < 25:
    print("normal weight")  
elif bmi < 30:
    print("overweight")
elif bmi < 35:
    print("obese")
else:
    print("clinically obese")

def fun(a,b):
    c = a + b
    return c
def fun1(a,b):
    c = a - b
    return c    
a = 10
b = 20
print(fun(a,b))
print(fun1(a,b))
def fun2(a,b):
    c = a * b
    return c  
print(fun2(a,b))
