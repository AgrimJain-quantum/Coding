thisdict = {
    "brand" : "aston martin",
    "model" : "db11",
    "year" : 2020,
}
thisdict.pop("model")
print(thisdict)
thisdict.popitem()
print(thisdict)
del(thisdict["brand"])
print(thisdict)
this = {
    "brand" : "aston martin",
    "model" : "db11",
    "year" : 2020,
    "color" : "red",
    "engine" : "v8",
    "horsepower" : 503,
    "torque" : 498,
    "weight" : 3855,
    "top_speed" : 208,
}
this.copy()
thisdict = {
    "brand" : "aston martin",
    "model" : "db11",
    "year" : 2020,
}
thisdict.clear()
print(thisdict)
this.items()
print(this)
this.fromkeys(thisdict)
print(this)
car = {
    "brand" : "aston martin",
    "model" : "db11",
    "year" : 2020,
    "color" : "red",
}
mydict = car.copy()
print(mydict)
