# _*_ coding:utf-8 _*_
import re

from factor.basics import basic_strings

def Replace(r_string):
    for i in basic_strings:
        if i in r_string:
            r_string = r_string.replace(i, i+"()")
    return r_string
        

def repair(r_string):
    #r_string = String.lower()
    r_string = r_string.replace('highday', 'argmax')
    r_string = r_string.replace('lowday', 'argmin')
    r_string = r_string.replace('adv(', 'mean(volume,')
    #r_string = r_string.replace('returns', 'returns()')
    
    #r_string = r_string.replace('oldpositions', 'oldpositions()')
    #r_string = r_string.replace('newpositions', 'newpositions()')
    #r_string = r_string.replace('close' ,'close()')
    #r_string = r_string.replace('Open', 'Opened()')
    #r_string = r_string.replace('high', 'high()')
    #r_string = r_string.replace('low', 'low()')
    #r_string = r_string.replace('volume', 'volume()')
    #r_string = r_string.replace('money', 'money()')
    #r_string = r_string.replace('avg', 'avg()')
    #r_string = r_string.replace('pb', 'pb()')
    #r_string = r_string.replace('reason', 'reason()')
    #r_string = r_string.replace('marketvalue' ,'marketvalue()')
    #r_string = r_string.replace('dealamount', 'dealamount()')
    #r_string = r_string.replace('turnoverrate','turnoverrate()')
    #r_string = r_string.replace('turnovervalue','turnovervalue()')
    #r_string = r_string.replace('turnovervolume','turnovervolume()')
    #r_string = r_string.replace('mean', 'tsmean')
    r_string = r_string.replace('exp' ,'exponential')
    r_string = r_string.replace('sum', 'summation')
    r_string = r_string.replace('max', 'maximum')
    r_string = r_string.replace('min', 'minimum')
    
    r_string = r_string.replace('coviance', 'cov')
    r_string = r_string.replace('prod', 'product')
    r_string = r_string.replace('log', 'logarithm')
    r_string = r_string.replace('abs', 'absolute') 
    r_string = r_string.replace('count', 'counttt')
    #r_string = r_string.replace('isst', 'isst()')
    #r_string = r_string.replace('tradestatus','tradestatus()')
    r_string = Replace(r_string)
    return r_string

SUPPORT_SIGN = {'[': 99, '^': 50, '*': 30, '%': 30, '/': 30, '-': 20, '+': 20, '>': 10, '<': 10, '>=': 10,
                '<=': 10, '==': 5, '!=': 5, '&&': 3, '||': 3}

first_sign = ['!', '&', '=', '>', '<', '|']

NUMBER_PATTERN = re.compile('[!a-zA-Z0-9.]')
ignore_list = [' ','_']
#ignore_list = [" "]

# ??????????????????????????????????????????
def check(string):
    flag1 = Stack()
    flag2 = Stack()
    for char in string:
        if char == '(':
            flag1.push('(')
        elif char == ')':
            if flag1.peek() != '(':
                raise TypeError
            else:
                flag1.pop()
        elif char == '[':
            flag2.push('[')
        elif char == ']':
            if flag2.peek() != '[':
                raise TypeError
            else:
                flag2.pop()
    if not flag1.empty() or not flag2.empty():
        print("??????????????????")
        raise TypeError

def init(expression):
    check(expression)
    expression = expression.replace('pi', '3.14159')
    for i in ignore_list:
        expression = expression.replace(i, '')
    return expression

# ????????????????????? ??????????????????
def body(expression):
    expression = init(expression)
    expression = chang_allcondition(expression)
    expression = to_suffix(expression)
    return text_neg(expression)

# ???condition??????????????????????????????????????????????????????
def to_suffix(expression):
    # check type
    sign_stack = Stack()
    result = []
    pre_char = None  # ?????????????????????????????????
    flag = 0
    i = 0
    jump_signal = 0
    # jump_signal ???????????????????????????????????????????????????
    if not isinstance(expression, str):
        raise TypeError
    if search_point(expression) == 0:
        for char in expression:
            if not jump_signal:
                if flag:
                    result[-1] += char
                    if char == '(':
                        flag += 1
                    if char == ')':
                        flag -= 1
                        if flag == 0:
                            list_exp = extract(result[-1])
                            result[-1] = list_exp[0] + '(' + to_suffix(list_exp[1]) + ')'
                            # print(result[-1])
                    i += 1
                    continue
                if char in first_sign:
                    if text_double(expression, i):
                        char = char + expression[i + 1]
                        jump_signal = 1
                        # print(jump_signal)
                if char in SUPPORT_SIGN:
                    pre_sign = sign_stack.peek()
                    while pre_sign and SUPPORT_SIGN[char] <= SUPPORT_SIGN[pre_sign]:
                        if pre_sign == '[':
                            break
                        result.append(sign_stack.pop())
                        pre_sign = sign_stack.peek()
                    sign_stack.push(char)
                elif char == ']':
                    pre_sign = sign_stack.peek()
                    while pre_sign != '[':
                        pre_sign = sign_stack.pop()
                        result.append(pre_sign)  # ?????????result??????
                        pre_sign = sign_stack.peek()
                    sign_stack.pop()  # ?????????????????????
                elif NUMBER_PATTERN.match(char):
                    if pre_char and NUMBER_PATTERN.match(pre_char):  # ??????pre_char????????????????????????????????????????????????
                        result[-1] += char  # ????????????????????????
                    else:
                        result.append(char)
                elif char == '(':
                    if len(result) == 0:
                        result.append(char)
                    else:
                        if NUMBER_PATTERN.match(pre_char):
                            result[-1] += char
                        else:
                            result.append(char)
                    flag = 1
                else:
                    print(char)
                    raise TypeError
                pre_char = char
                i += 1
            else:
                jump_signal = 0
                pre_char = expression[i]
                i += 1
        while not sign_stack.empty():
            result.append(sign_stack.pop())
        # print(result)
        return text_neg(count(result))
    else:
        point_div = search_point(expression)
        return to_suffix(point_div[0]) + ',' + to_suffix(point_div[1])

def text_brackets(string):
    check(string)
    if string[0] != '(' or string[-1] != ')':
        return False
    else:
        flag = 0
        mark = 1
        for i in string:
            if i == '(':
                flag += 1
            if i == ')':
                flag -= 1
            if flag == 0 and mark != len(string):
                return False
            mark += 1
    return True

# ?????????????????????????????????
def count(suffix):
    count_stack = []
    i = len(suffix)
    for sen in suffix:
        if sen in list(SUPPORT_SIGN):
            if sen == "+":
                oprator1 = count_stack.pop()
                oprator2 = count_stack.pop()
                count_stack.append('plus' + '(' + oprator2 + ',' + oprator1 + ')')
            elif sen == "*":
                oprator1 = count_stack.pop()
                oprator2 = count_stack.pop()
                count_stack.append('multiply' + '(' + oprator2 + ',' + oprator1 + ')')
            elif sen == "%" or sen == "/":
                oprator1 = count_stack.pop()
                oprator2 = count_stack.pop()
                count_stack.append('divide' + '(' + oprator2 + ',' + oprator1 + ')')
            elif sen =='^':
                oprator1 = count_stack.pop()
                oprator2 = count_stack.pop()
                count_stack.append('power' + '(' + oprator2 + ',' + oprator1 + ')')
            elif sen == '>=':
                oprator1 = count_stack.pop()
                oprator2 = count_stack.pop()
                count_stack.append('greaterorequal' + '(' + oprator2 + ',' + oprator1 + ')')
            elif sen == '<=':
                oprator1 = count_stack.pop()
                oprator2 = count_stack.pop()
                count_stack.append('lessorequal' + '(' + oprator2 + ',' + oprator1 + ')')
            elif sen == '<':
                oprator1 = count_stack.pop()
                oprator2 = count_stack.pop()
                count_stack.append('lessthan' + '(' + oprator2 + ',' + oprator1 + ')')
            elif sen == '>':
                oprator1 = count_stack.pop()
                oprator2 = count_stack.pop()
                count_stack.append('greaterthan' + '(' + oprator2 + ',' + oprator1 + ')')
            elif sen == '&&':
                oprator1 = count_stack.pop()
                oprator2 = count_stack.pop()
                count_stack.append('also' + '(' + oprator2 + ',' + oprator1 + ')')
            elif sen == '||':
                oprator1 = count_stack.pop()
                oprator2 = count_stack.pop()
                count_stack.append('oror' + '(' + oprator2 + ',' + oprator1 + ')')
            elif sen == '!=':
                oprator1 = count_stack.pop()
                oprator2 = count_stack.pop()
                count_stack.append('notequal' + '(' + oprator2 + ',' + oprator1 + ')')
            elif sen == '==':
                oprator1 = count_stack.pop()
                oprator2 = count_stack.pop()
                count_stack.append('equal' + '(' + oprator2 + ',' + oprator1 + ')')
            elif sen == "-":
                if len(count_stack) > 1:
                    if len(count_stack) == 2 and i == 2:
                        count_stack[-1] = '-' + count_stack[-1]
                        i -= 1
                        continue
                    else:
                        oprator1 = count_stack.pop()
                        oprator2 = count_stack.pop()
                        count_stack.append('subtract' + '(' + oprator2 + ',' + oprator1 + ')')
                else:
                    count_stack.append('-' + count_stack.pop())
        else:
            if sen[0] == '!':
                sen = 'negative' + '(' + sen[1:] + ')'
                count_stack.append(sen)
            elif text_brackets(sen):
                count_stack.append(sen[1:len(sen ) -1])
            else:
                count_stack.append(sen)
        i -= 1
    return ''.join(count_stack)

# ????????????????????????????????????????????? ?????????????????????????????????
def extract(string):
    first = string.find("(")
    last = string.rfind(")")
    return [string[:first], string[first+1:last]]

# ???????????????????????????????????????????????????????????????????????????????????????????????????
def search_point(string):
    flag = 0
    i = 0
    for char in string:
        if char == "(":
            flag += 1
        if char == ")":
            flag -= 1
        if char == ',' and flag == 0:
            return [string[:i], string[ i +1:]]
        i += 1
    return 0

# ???????????????????????????
def text_double(expression, i):
    if (expression[i] + expression[ i +1]) in list(SUPPORT_SIGN):
        return 1
    else:
        return 0

# ???????????????condition?????????
def search(expression, i):
    '''

    :param expression:????????????????????????
    :param i: ?????????expression.find???'???'???
    :return: ?????? condition??????????????? ????????? ?????? ?????????
    '''
    left_flag = 0
    right_flag = 0
    left_mark = i - 1
    right_mark = i + 1
    colon_mark = i + 1
    catch_flag = 0
    for left_mark in range(i - 1, -1, -1):
        if expression[left_mark] == ']' or expression[left_mark] == ')':
            left_flag += 1
        elif expression[left_mark] == '[' or expression[left_mark] == '(':
            left_flag -= 1
        if left_flag == -1:
            break
        if left_flag == 0 and expression[left_mark] == ',':
            break
    for right_mark in range(i + 1, len(expression)):
        if expression[right_mark] == ']' or expression[right_mark] == ')':
            right_flag -= 1
        elif expression[right_mark] == '[' or expression[right_mark] == '(':
            right_flag += 1
        if right_flag == -1:
            break
        if right_flag == 0 and expression[right_mark] == ',':
            break
        if right_flag == 0 and expression[right_mark] == ':' and catch_flag == 0:
            colon_mark = right_mark
            catch_flag =1
    # ??????????????????
    if left_flag == 0 and left_mark == 0:
        left_mark = -1
    if right_flag == 0 and right_mark == len(expression) - 1:
        right_mark = len(expression)
    # print([left_mark, colon_mark, right_mark])
    return [left_mark, colon_mark, right_mark]


def chang_condition(expression):
    '''


    :param expression: ???expression??????????????????condition????????????
    :return:
    '''
    i = expression.find('?')
    mark_place = search(expression, i)
    field2 = expression[i + 1:mark_place[1]]
    field3 = expression[mark_place[1] + 1:mark_place[2]]
    if mark_place[0] == -1:
        field1 = expression[0:i]
        return 'condition(' + body(field1) + ',' + body(field2) + ',' + body(field3) + ')' \
               + expression[mark_place[2]:]
    else:
        field1 = expression[mark_place[0] + 1:i]
        return expression[0:mark_place[0] + 1] + 'condition(' + body(field1) + ',' + body(field2) + ',' \
               + body(field3) + ')' + expression[mark_place[2]:]


def chang_allcondition(expression):
    '''

    :param expression:????????????
    :return:
    '''
    while expression.find('?') != -1:
        expression = chang_condition(expression)
    return expression


def text_neg(string):
    if len(string) == 0:
        return string
    if string[0] == '-':
        return 'multiply' + '(' + '-1' + ',' + string[1:] + ')'
    else:
        return string


# ----------------------------------------

class Stack(object):
    def __init__(self):
        self.datas = []
        self.length = 0
        # print('???????????????')

    def push(self, data):
        self.datas.append(data)
        self.length += 1

    def peek(self):
        return None if self.empty() else self.datas[len(self.datas) - 1]

    def pop(self):
        try:
            return self.peek()
        finally:
            self.length -= 1
            del self.datas[len(self.datas) - 1]

    def empty(self):
        # return not bool(self.datas)
        return not bool(self.length)

    def __str__(self):
        print('-----------------------str called----------------------')
        return ','.join([str(data) for data in self.datas])

