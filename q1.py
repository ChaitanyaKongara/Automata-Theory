import json
import sys

input_name = sys.argv[1]
output_name = sys.argv[2]

input_fd = open(input_name, 'r')
output_fd = open(output_name, 'w')

inp = json.load(input_fd)

# NFA = {
#     "states": [],
#     "letters": [],
#     "transition_function": [],
#     "start_states": [],
#     "final_states": [],
# }
state_cnt = 0
operators = {
    "+": 0,
    ".": 1,
    "*": 2,
    "(": -1,
    ")": -2
}
letters = []
class NFA():
    def __init__(self,start,char):
        self.nfa = {}
        self.nfa["states"] = [start, start+1]
        self.nfa["transition_function"] = [[start,char, start+1]]
        self.nfa["start_states"] = [start]
        self.nfa["final_states"] = [start+1]

def postfix_conversion(regex):
    upd = ""
    for i in range(len(regex)):
        if regex[i] not in operators:
            if i!=0 and (regex[i-1] not in operators or regex[i-1] == ')' or regex[i-1] == '*'):
                upd += '.'
        else:
            if i!=0 and regex[i] == '(' and (regex[i-1] not in operators or regex[i-1] == ')' or regex[i-1] == '*'):
                upd+='.'
        upd +=regex[i]
    ans = ""
    stack = []
    for item in upd:
        if item not in operators:
            ans+=item
        else:
            if item == '(':
                stack.append('(')
            elif item == ')':
                while(stack[len(stack)-1]!='('):
                    ans+=stack[len(stack)-1]
                    stack.pop()
                stack.pop()
            else:
                if len(stack) == 0:
                    stack.append(item)
                elif stack[len(stack)-1] == '(':
                    stack.append(item)
                elif operators[stack[len(stack)-1]] < operators[item]:
                    stack.append(item)
                else:
                    while True:
                        if len(stack) == 0:
                            break
                        elif operators[stack[len(stack)-1]] < operators[item]:
                            stack.append(item)
                            break
                        else:
                            ans+=stack[len(stack)-1]
                            stack.pop()
                    stack.append(item)
    while len(stack):
        ans+=stack.pop()
    return ans

def evaluate_postfix(regex):
    global state_cnt
    stack = []
    stack.append(NFA(state_cnt,'$'))
    for i in range(len(regex)):
        if regex[i] not in operators:
            stack.append(NFA(state_cnt,regex[i]))
            state_cnt+=2
        elif regex[i] == '*':
            obj = stack.pop()
            for end in obj.nfa["final_states"]:
                for start in obj.nfa["start_states"]:
                    obj.nfa["transition_function"].append([end,'$',start])
            for start in obj.nfa["start_states"]:
                obj.nfa["transition_function"].append([state_cnt,'$',start])
            obj.nfa["final_states"].append(state_cnt)
            obj.nfa["start_states"] = [state_cnt]
            obj.nfa["states"].append(state_cnt)
            state_cnt+=1
            stack.append(obj)
        elif regex[i] == '.':
            obj2 = stack.pop()
            obj1 = stack.pop()
            for end in obj1.nfa["final_states"]:
                for start in obj2.nfa["start_states"]:
                    obj2.nfa["transition_function"].append([end,'$',start])
            obj2.nfa["start_states"] = obj1.nfa["start_states"]
            for item in obj1.nfa["states"]:
                obj2.nfa["states"].append(item)
            for item in obj1.nfa["transition_function"]:
                obj2.nfa["transition_function"].append(item)
            stack.append(obj2)
        elif regex[i] == '+':
            obj2 = stack.pop()
            obj1 = stack.pop()
            transition_function = []
            start_states = [state_cnt]
            final_states = obj1.nfa["final_states"] + obj2.nfa["final_states"]
            transition_function = obj2.nfa["transition_function"] + obj1.nfa["transition_function"]
            states = obj2.nfa["states"] + obj1.nfa["states"] + [state_cnt]
            for start in obj1.nfa["start_states"]:
                transition_function.append([state_cnt,'$',start])
            for start in obj2.nfa["start_states"]:
                transition_function.append([state_cnt,'$',start])
            obj2.nfa["states"] = states
            obj2.nfa["transition_function"] = transition_function
            obj2.nfa["start_states"] = start_states
            obj2.nfa["final_states"] = final_states
            stack.append(obj2)
            state_cnt+=1
    return stack.pop()
            


postfix = postfix_conversion(inp["regex"])
for i in postfix:
    if i not in operators and i not in letters:
        letters.append(i)

ans = evaluate_postfix(postfix)

# print(ans.nfa)

letters.append('$')
out = {
    "states": list(map(str,ans.nfa["states"])),
    "letters": letters,
    "transition_function": [],
    "start_states": list(map(str,ans.nfa["start_states"])),
    "final_states": list(map(str,ans.nfa["final_states"]))
}
for item in ans.nfa["transition_function"]:
    out["transition_function"].append([str(item[0]),item[1],str(item[2])])
json.dump(out,output_fd, indent=4)