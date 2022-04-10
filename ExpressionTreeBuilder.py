import re # Регулярные выражения

priorities = {'||': 1, '&&': 2, '==': 3, '!=': 3, '>': 4, '>=': 4, '<': 4, '<=': 4, '+': 5, '-': 5, '*': 6, '/': 6, 'sin': 7, 'max': 7, 'minus': 7, '^': 8, ')': 9, '(': 10}

# Разделитель параметров функции
SEPARATOR = ';'

def IsLowerPriority(op1, op2):
    return priorities[op1] < priorities[op2]
    
def IsOperator(token):
    return (token in priorities)
    
SPLIT_TO_TOKENS_PATTERN = "\\d+(?:[\\.]\\d+)?|;|\\+|-|\\*|\\/|\\^|>=|>|<=|<|==|!=|&&|\\|\\||!|\\(|\\)|[A-z1-9_]+"

# Класс узла дерева. Хранит родительский узел, дочерние узлы или листья, используемый оператор
class Node:
    def __init__(self, parent, tokens):
        self.parent = parent
        lowestPriorityToken = None
        lowestPriorityTokenIndex = -1
        openingParenthesisCounter = 0
        # Ищем внешний оператор с наименьшим приоритетом. Для начала работы цикла, пока не нашли оператор, используем доп.условие (lowestPriorityTokenIndex == -1)
        for i, token in enumerate(tokens):
            if (token == '('): openingParenthesisCounter+=1
            elif (token == ')'): openingParenthesisCounter-=1
            
            if (IsOperator(token) and 
            (
                (lowestPriorityTokenIndex == -1) or (openingParenthesisCounter == 0) and IsLowerPriority(token, lowestPriorityToken)
            )):
                lowestPriorityToken = token
                lowestPriorityTokenIndex = i
                
        # Если не нашли оператор, значит работаем с листом дерева. Завершаем итерационных обход ветви
        if (lowestPriorityTokenIndex == -1):
            self.operator = None
            self.children = tokens[0]
            return
        
        # Рекурсивно создаем дочерние узлы
        self.children = []
        # Если найденный оператор - закрывающая скобка, разбиваем содержимое внешних скобок на отдельные параметры по внешним разделителям SEPARATOR=";"
        if (lowestPriorityToken == ")"):
            self.operator = "()"
            argumentTokens = []
            openingParenthesisCounter = 0
            for token in tokens[1:-1]:
                if (token == '('): openingParenthesisCounter+=1
                elif (token == ')'): openingParenthesisCounter-=1
                
                if (token == SEPARATOR and openingParenthesisCounter == 0):
                    self.children.append(Node(self, argumentTokens))
                    argumentTokens.clear()
                else: argumentTokens.append(token)
            self.children.append(Node(self, argumentTokens))
            argumentTokens.clear()
        # Во всех остальных случаях разбиваем последовательность токенов на две части при их существовании: слева и справа от оператора
        else:
            self.operator = lowestPriorityToken
            if (lowestPriorityTokenIndex > 0):
                self.children.append(Node(self, tokens[0:lowestPriorityTokenIndex]))
            
            if (lowestPriorityTokenIndex < len(tokens)):
                self.children.append(Node(self, tokens[lowestPriorityTokenIndex+1:]))
            
    def ToString(self):
        if (self.operator == None): 
            return self.children
        else:
            return self.operator + "[" + ",".join([x.ToString() for x in self.children])+ "]"
            
    def Print(self, depth = 0):
        if (self.operator == None): 
            print("\t" * depth + self.children)
        else:
            print("\t" * depth + self.operator + "[")
            for child in self.children:
                child.Print(depth + 1)
            print("\t" * depth + "]")


inputString = "sin 4221 ^ 69 - (1 + 2) * ((-3)) / max(x; y; z)".lower();
tokens = re.findall(SPLIT_TO_TOKENS_PATTERN, inputString)
# Находим унарные минусы и заменяем их на функцию minus
for i, token in enumerate(tokens):
    if (token == "-" and (i == 0 or IsOperator(tokens[i - 1]))):
        tokens[i] = "minus"

print(inputString)
#print(tokens)
n = Node(None, tokens)
print(n.ToString())
n.Print()
