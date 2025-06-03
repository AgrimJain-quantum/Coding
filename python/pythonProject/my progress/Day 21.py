class Animal:
    def __init__(self):
        self.num_eyes = 2
    def breathe(self):
        print("Inhale, Exhale")
    def eat(self):
        print("Nom, Nom")
    def sleep(self):
        print("Zzz, Zzz")
        
        
class Fish(Animal):
    def __init__(self):
        super().__init__()  # Call the constructor of the parent class
    def swim(self):
        print("Swim, Swim")
nemo = Fish()
nemo.breathe()  # Inhale, Exhale
nemo.swim()     # Swim, Swim
nemo.eat()      # Nom, Nom
