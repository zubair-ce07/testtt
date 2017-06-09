import operator

class User(object):
    def __init__(self, name, age):
        self.name = name
        self.age = age



a=User('hammad', 20)
b=User('aslam', 30)
c=User('arshad', 25)
d=User('shamsheer', 30)

dic={'key1':a, 'key2':b, 'key3':c ,'key4':d}

user=max(dic.values(), key=operator.attrgetter('age'))
print(user.name)
