OPERATIONS = {}


def operation(symbol):
    def register(function):
        OPERATIONS[symbol] = function
        return function

    return register


@operation("+")
def add(a, b):
    return a + b


@operation("*")
def multiply(a, b):
    return a * b


stack = []
for word in input("RPN> ").split():
    if word in OPERATIONS:
        b, a = stack.pop(), stack.pop()
        stack.append(OPERATIONS[word](a, b))
    else:
        stack.append(float(word))
print(stack)
