class AgeException(Exception):
    def __init__(self, msg):
        self.msg = msg

    def print_exception(self):
        print('User defined exception:', self.msg)

class Person():
    def __init__(self, age, name):
        self.age = age
        self.name = name
    
    def age_check(self):
        if self.age < 18:
            raise AgeException('Sorry your too young.')
        else:
            print("Verified!")

    def display_person(self):
        print(self.name)
        print(self.age)
    
p = Person(17, 'Andrew')

try:
    p.age_check()
except AgeException as e:
    print('Error:', e)
