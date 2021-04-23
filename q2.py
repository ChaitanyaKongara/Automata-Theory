import json
import sys

input_name = sys.argv[1]
output_name = sys.argv[2]

input_fd = open(input_name, 'r')
output_fd = open(output_name, 'w')

inp = json.load(input_fd)

DFA = {
    "states": [],
    "letters": [],
    "transition_function": [],
    "start_states": [],
    "final_states": [],
}


# 2 ** k states creation ---------------------------------------

dfa_noofstates = pow(2,len(inp["states"]))

num_to_state = {}
state_to_num = {}
def mapper(num):  
    arr = []
    for i in range(len(inp["states"])):
        if num & 1<<i:
            state = inp["states"][i]
            arr.append(state)
    num_to_state[num] = arr
    state_to_num[tuple(arr)] = num
    return arr

for i in range(dfa_noofstates):
    DFA["states"].append(mapper(i))

#  letters and start states will be the same for NFA and DFA
DFA["letters"] = inp["letters"]
DFA["start_states"] = [inp["start_states"]]


# finding final states of DFA

for item in  inp["final_states"]:
    for i in range(dfa_noofstates):
        # print(i,item)
        if i & state_to_num[tuple([item])] and  num_to_state[i] not in DFA["final_states"]:
            DFA["final_states"].append(num_to_state[i])



# bulding transition matrix

states_found = []
for item in inp["states"]:
    states_found.append([item])
trans_mat = {}
for i in range(dfa_noofstates):
    item = mapper(i)
    for action in inp["letters"]:
        trans_mat[tuple([tuple(item),action])] = []
for item in inp["transition_function"]:
    trans_mat[tuple([tuple([item[0]]), item[1]])].append(item[2])
for item in inp["transition_function"]:
    trans_mat[tuple([tuple([item[0]]), item[1]])].sort()


for var in  range(dfa_noofstates):
    state = num_to_state[var]
    for action in DFA["letters"]:
        end_state = []
        for i in range(len(state)):
            for item in trans_mat[tuple([tuple([state[i]]), action])]:
                if item not in end_state:
                    end_state.append(item)
        end_state.sort()
        trans_mat[tuple([tuple(state),action])]=end_state

for item in trans_mat:
    DFA["transition_function"].append([list(item[0]),item[1],trans_mat[item]])

json.dump(DFA,output_fd, indent=4)