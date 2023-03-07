#Python multiple inheritance experiments
import time
class A:
    def __init__(self):
        print('A')
        if dir:
            super().__init__()

        


class B(A):
    def __init__(self):
        print('B')
        super().__init__()

    def callIdiot(self):
        print("im going to call...")
        time.sleep(1)
        print("im calling... " + self.contact)

    def createIdiot(self):
        if self.contact:
            return self.contact
        return self.new_contact
    

class X:
    def __init__(self):
        print('X')
        if not dir:
            super().__init__()
        
    def callIdiot(self):
        print("im going to call...")
        time.sleep(1)
        print("im calling... " + self.contact)

        
class Forward(B, X):
    def __init__(self):
        self.contact = None
        self.new_contact = 'avanti'
        print('Forward')
        super().__init__()
        
        self.contact = self.createIdiot()
        self.callIdiot()
        

class Backward(X, B):
    def __init__(self):
        self.contact = 'indietro'
        print('Backward')
        super().__init__()
        self.callIdiot()



class FirstShit:
    def __init__(self, word_one) -> None:
        print(word_one)
        super().__init__()
        
class SecondShit:
    def __init__(self) -> None:

        
        print(self.word_two)


class Shit( FirstShit, SecondShit):
    def __init__(self, word_one, word_two) -> None:
        self.word_two = word_two
        super().__init__(word_one)


class Status:
    def __init__(self) -> None:
        self.status = {'status': 'ok'}
        super().__init__()
    
    def test(self):
        status = self.status
        status['status'] = 'not ok'

    def test2(self):
        print(self.status)
    def sum(self, a,b):
        return a+b

dir = True #True = forward, False = backward
test = Status()
test.test()
test.test2()
tup = (4,5)
print(test.sum(*tup))


Forward()
Backward()


Shit('Roma è figa', 'rome è grande')