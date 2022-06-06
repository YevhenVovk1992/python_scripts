#all exceptions must include in BaseExeptions
class NonPositiveError(Exception):
    pass

#inherit class list
class PositiveList(list):
    #create a method for the class
    def append(self, args):
        if args > 0:
            super(PositiveList, self).append(args)
            return self
        else:
            raise NonPositiveError

#checking
a = [2, -4, 4, 5, -1]
a.append(-2) #add any int(number)
b = PositiveList(a)
b.append(-3)# add only positive int(number)
print(b)#__main__.NonPositiveError

#create an exception handler
def AddNeg(list, args):
    try:
        OP = list.append(args)
        return OP
    except NonPositiveError:
        return list.append(abs(args))

#function AddNeg can add any number to PositiveList
LST = PositiveList([1, 34, 56, 6, 3])
print(AddNeg(LST, -300)) #take the absolute value of a number and add to LST
print(AddNeg(LST, 300)) #add 300 to LST