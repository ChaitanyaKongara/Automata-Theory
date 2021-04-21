import json
import sys

input_name = sys.argv[1]
output_name = sys.argv[2]

input_fd = open(input_name, 'r')
output_fd = open(output_name, 'w')

inp = json.load(input_fd)

out = {
    "regex": ""
}

start = "ss107"
final = "ff107"
epsilon = "$"


trans_mat = {}
for trans in inp["transition_function"]:
    if tuple([trans[0],trans[2]]) in trans_mat:
        trans_mat[tuple([trans[0],trans[2]])] += "+(" + trans[1] + ")"
    else:
        trans_mat[tuple([trans[0],trans[2]])] = trans[1]
for state in inp["start_states"]:
    if tuple([start,state]) in trans_mat:
        trans_mat[tuple([start,state])] += "+" + epsilon
    else:
        trans_mat[tuple([start,state])] = epsilon
for state in inp["final_states"]:
    if tuple([state,final]) in trans_mat:
        trans_mat[tuple([state,final])] += "+" + epsilon
    else:
        trans_mat[tuple([state,final])] = epsilon
dead_states = {}
for item in inp["states"]:
    dead_states[item]=False
dead_states[start] = False
dead_states[final] = False

states = inp["states"]
states.append(start)
states.append(final)

for dead in inp["states"]:
    if dead == start or dead == final:
        continue
    trans_mat1 = {}
    for state1 in states:
        if state1 == dead or dead_states[state1]:
            continue
        for state2 in states:
            if state2 == dead or dead_states[state2]:
                continue
            flag=0
            ans = "("
            if tuple([state1,state2]) in trans_mat:
                ans+= trans_mat[tuple([state1,state2])]
                flag=1
            if tuple([state1,dead]) in trans_mat and tuple([dead,state2]) in trans_mat:
                if tuple([dead,dead]) in trans_mat:
                    if flag:
                        ans+= "+("+trans_mat[tuple([state1,dead])] +"("+trans_mat[tuple([dead,dead])]+")*"+ trans_mat[tuple([dead,state2])]+")"
                    else:
                        ans+= trans_mat[tuple([state1,dead])] +"("+trans_mat[tuple([dead,dead])]+")*"+ trans_mat[tuple([dead,state2])]
                else:
                    if flag:
                        ans+= "+("+trans_mat[tuple([state1,dead])] + trans_mat[tuple([dead,state2])]+")"
                    else:
                        ans+= trans_mat[tuple([state1,dead])] + trans_mat[tuple([dead,state2])]
                flag=1
            ans+=")"
            if flag:
                trans_mat1[tuple([state1,state2])] = ans
    trans_mat = trans_mat1
    dead_states[dead]=True

out["regex"] = trans_mat[tuple([start,final])]

json.dump(out,output_fd, indent=4)