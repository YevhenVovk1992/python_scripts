class ExtendedStack(list):
    
    def sum(self):
        # операция сложения
        top1 = self.pop()
        top2 = self.pop()
        return self.append(top1 + top2)
    
    def sub(self):
        # операция вычитания
        top1 = self.pop()
        top2 = self.pop()
        return self.append(top1 - top2)
    
    def mul(self):
        # операция умножения
        top1 = self.pop()
        top2 = self.pop()
        return self.append(top1*top2)
    
    def div(self):
        # операция целочисленного деления
        top1 = self.pop()
        top2 = self.pop()
        return self.append(top1//top2)

    
q = ExtendedStack([1, 2, 4, 5, 6, 5, 5, 8])
q.div()
print('div', q)
q.mul()
print('mul', q)
q.sub()
print('sub', q)
