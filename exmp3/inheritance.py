class Tutor:
    def __init__(self, age, name):
        self.age = age
        self.name = name
    def person(self):
        return self.age, self.name
class Person(Tutor):
    pass
a = Person(43, "kashida")
print(a.person())