import tkinter 
window = tkinter.Tk()
window.title("My First GUI Program")
window.minsize(width=500, height=300)

#label
my_label = tkinter.Label(text="I am a label", font=("Arial", 24, "bold", "italic"))
my_label.pack(expand = True)


def add(*args):
    print(args[1])
    sum = 0
    for n in args:
        sum += n
    return sum
print(add(1, 2, 3))













# import turtle
# tur = turtle.Turtle()
# tur.write("some text ", font=("Arial", 24, "bold", "italic"))



window.mainloop()
    