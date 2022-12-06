import doctest

# NO ADDITIONAL IMPORTS ALLOWED!
# You are welcome to modify the classes below, as well as to implement new
# classes and helper functions as necessary.


class Symbol:
    def __pow__(self,other):            #These functions allow for use of their operator
        return Pow(self,other)
    def __rpow__(self, other):
        return Pow(other, self)
    def __add__(self, other):
        return Add(self, other)
    def __radd__(self, other):
        return Add(other, self)
    def __sub__(self, other):
        return Sub(self, other)
    def __rsub__(self, other):
        return Sub(other, self)
    def __mul__(self, other):
        return Mul(self, other)
    def __rmul__(self, other):
        return Mul(other, self)
    def __truediv__(self, other):
        return Div(self, other)
    def __rtruediv__(self, other):
        return Div(other, self)
    def deriv(self, var):                       #Check type of val and return accordingly
        if self.opname == 'val':
            return Num(0)
        if self.opname == 'var' and self.name != var:
            return Num(0)
        elif self.opname == 'var' and self.name == var:
            return Num(1)
        elif self.opname == 'Add':
            return self.left.deriv(var) + self.right.deriv(var)
        elif self.opname == 'Sub':
            return self.left.deriv(var) - self.right.deriv(var)
        elif self.opname == 'Mul':
            return self.left * self.right.deriv(var) + self.right * self.left.deriv(var)
        elif self.opname == 'Div':
            return (self.right * self.left.deriv(var) - self.left * self.right.deriv(var))/(self.right*self.right)
        elif self.opname == 'Pow':
            return self.right * self.left**(self.right-1)* self.left.deriv(var)
        else:
            raise ValueError("Derivative did not follow the rules")
            return None


class Var(Symbol):
    def __init__(self, n):
        """
        Initializer.  Store an instance variable called `name`, containing the
        value passed in to the initializer.
        """
        self.name = n
        self.opname = 'var'


    def __str__(self):
        return self.name

    def __repr__(self):
        return "Var(" + repr(self.name) + ")"
    def simplify(self):                             #Already simplified
        return self
    def eval(self, mapping):                        #Returns the mapped value from dictionary
        return Num(mapping[self.name])

class Num(Symbol):
    def __init__(self, n):
        """
        Initializer.  Store an instance variable called `n`, containing the
        value passed in to the initializer.
        """
        self.n = n
        self.opname = 'val'

    def __str__(self):
        return str(self.n)

    def __repr__(self):
        return "Num(" + repr(self.n) + ")"
    def simplify(self):                     #Similar to var
        return self
    def eval(self, mapping):
        return self
class BinOp(Symbol):
    def __init__(self, left, right):
        if isinstance(left, str):                       #Need to create correct type for each side
            self.left = Var(left)
        elif isinstance(left, int) or isinstance(left, float):
            self.left = Num(left)
        else:
            self.left = left
        if isinstance(right, str):
            self.right = Var(right)
        elif isinstance(right, int) or isinstance(right, float):
            self.right = Num(right)
        else:
            self.right = right
        self.op = {
                'Add': '+',
                'Sub': '-',
                'Div': '/',
                'Mul': '*',
                'Pow': '**',
        }
        self.PEMDAS = {
            'var': 7,
            'val': 7,
            'Par': 6,
            'Pow': 5,
            'Mul': 4,
            'Div': 4,
            'Add': 2,
            'Sub': 2,
        }
    def __str__(self):
        left_side = str(self.left)              #Many different rules to use parenthesis
        right_side = str(self.right)
        if self.PEMDAS[self.left.opname] < self.PEMDAS[self.opname]:
            left_side = '(' + str(self.left) + ')'
        if self.PEMDAS[self.right.opname] < self.PEMDAS[self.opname]:
            right_side = '(' + str(self.right) + ')'
        elif self.opname == 'Sub' or self.opname == 'Div':
            if self.PEMDAS[self.right.opname] == self.PEMDAS[self.opname]:
                right_side = '(' + str(self.right) + ')'
        return (left_side + " " + self.op[self.opname] + " " + right_side)
    def __repr__(self):
        return self.opname + '(' + repr(self.left) + ', ' + repr(self.right) + ')'




class Add(BinOp):
    def __init__(self, left, right):
        BinOp.__init__(self, left, right)
        self.opname = 'Add'
    def simplify(self):                 #First left and right side must be as simole as possible (ints or vars)
        left = self.left.simplify()
        right = self.right.simplify()

        if isinstance(left, Num) and isinstance(right, Num):
            left = left.n
            right = right.n
            return Num(left + right)
        if isinstance(left, Num):
            if left.n == 0:
                return right
        if isinstance(right, Num):
            if right.n == 0:
                return left
        return left + right
    def eval(self, mapping):
        left = self.left.eval(mapping)          #Eval both sides to ensure that only values are left
        right = self.right.eval(mapping)
        return Add(left, right).simplify().n
class Sub(BinOp):
    def __init__(self, left, right):
        BinOp.__init__(self, left, right)
        self.opname = 'Sub'
    def simplify(self):
        left = self.left.simplify()
        right = self.right.simplify()               #Same idea for simplify
        if isinstance(left, Num) and isinstance(right, Num):
            left = left.n
            right = right.n
            return Num(left - right)
        if isinstance(right, Num):
            if right.n == 0:
                return left
        return left - right
    def eval(self, mapping):
        left = self.left.eval(mapping)
        right = self.right.eval(mapping)
        return Sub(left, right).simplify().n
class Mul(BinOp):
    def __init__(self, left, right):
        BinOp.__init__(self, left, right)
        self.opname = 'Mul'
    def simplify(self):
        left = self.left.simplify()
        right = self.right.simplify()
        if isinstance(left, Num) and isinstance(right, Num):
            left = left.n
            right = right.n
            return Num(left * right)
        if isinstance(left, Num):
            if left.n == 0:
                return Num(0)
            elif left.n == 1:
                return right
        if isinstance(right, Num):
            if right.n == 0:
                return Num(0)
            elif right.n == 1:
                return left
        return left * right
    def eval(self, mapping):
        left = self.left.eval(mapping)
        right = self.right.eval(mapping)
        return Mul(left, right).simplify().n
class Div(BinOp):
    def __init__(self, left, right):
        BinOp.__init__(self, left, right)
        self.opname = 'Div'
    def simplify(self):
        left = self.left.simplify()
        right = self.right.simplify()
        if isinstance(left, Num) and isinstance(right, Num):
            left = left.n
            right = right.n
            return Num(left / right)
        if isinstance(left, Num):
            if left.n == 0:
                return Num(0)
        if isinstance(right, Num):
            if right.n == 1:
                return left
        return left / right
    def eval(self, mapping):
        left = self.left.eval(mapping)
        right = self.right.eval(mapping)
        return Div(left, right).simplify().n
class Pow(BinOp):                       #Initialize it similarly to other functions
    def __init__(self, left, right):
        BinOp.__init__(self, left, right)
        self.opname = 'Pow'
    def __str__(self):
        left_side = str(self.left)              #Include old rules plus new ones
        right_side = str(self.right)
        if self.PEMDAS[self.left.opname] <= self.PEMDAS['Pow']:
            left_side = '(' + left_side + ')'
        if self.PEMDAS[self.left.opname] < self.PEMDAS[self.opname]:
            left_side = '(' + str(self.left) + ')'
        if self.PEMDAS[self.right.opname] < self.PEMDAS[self.opname]:
            right_side = '(' + str(self.right) + ')'
        elif self.opname == 'Sub' or self.opname == 'Div':
            if self.PEMDAS[self.right.opname] == self.PEMDAS[self.opname]:
                right_side = '(' + str(self.right) + ')'
        return (left_side + " " + self.op[self.opname] + " " + right_side)
    def simplify(self):
        left = self.left.simplify()
        right = self.right.simplify()
        if isinstance(left, Num) and isinstance(right, Num):
            left = left.n
            right = right.n
            return Num(left ** right)
        if isinstance(right, Num):
            if right.n == 0:
                return Num(1)
            elif right.n == 1:
                return left
        if isinstance(left, Num):
            if left.n == 0:
                return Num(0)
        return left ** right
    def eval(self, mapping):
        left = self.left.eval(mapping)          #All same as other funtions
        right = self.right.eval(mapping)
        return Pow(left, right).simplify().n

def expression(string):
    tokens = tokenize(string)           #returns parsed verison of a string
    return parse(tokens)

def tokenize(string):
    digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    list = []
    append = ''
    for i in range(len(string)):            #Need to keep digits representing the same number together
        if string[i] in digits or string[i] == '-':
            append += string[i]
        elif string[i] == '*':
            if string[i+1] == '*':          #Need to represent ** as pow and as a single token
                append += string[i:i+2]
                continue
            if string[i-1] != '*':
                list.append(string[i])
        elif len(append) > 0:
             list.append(append)
             list.append(string[i])
             append = ''
        else:
            list.append(string[i])
    list.append(append)
    return list
def parse(tokens):                      #Takes the token and returns parsing
    invalids = [')', '+', '-', '/', '*', ' ', '**']
    ops = ['+', '-', '/', '*', '**']
    def parse_expression(index):            #Need to recurse until values on left and right are either a num or a vala
        if index >= len(tokens):
            return None, index
        if tokens[index].lstrip('-').strip('.').isdigit():
            return Num(int(tokens[index])),index + 1
        elif str.isalpha(tokens[index]):
            return Var(tokens[index]), index + 1
        else:
            left = parse_expression(index+1)
            right_index = left[1] + 1
            op_index = left[1]
            while tokens[right_index] in invalids and right_index <len(tokens)-1:
                right_index += 1
            right = parse_expression(right_index)
            while tokens[op_index] not in ops and op_index < len(tokens)-1:
                op_index += 1
            if tokens[op_index] == '+':
                return Add(left[0], right[0]), right[1]         #Take into account each type of function
            elif tokens[op_index] == '-':
                return Sub(left[0], right[0]), right[1]
            elif tokens[op_index] == '*':
                return Mul(left[0], right[0]), right[1]
            elif tokens[op_index] == '/':
                return Div(left[0], right[0]), right[1]
            elif tokens[op_index] == '**':
                return Pow(left[0], right[0]), right[1]

    parsed_expression, next_index = parse_expression(0)
    return parsed_expression

if __name__ == "__main__":
    doctest.testmod()

