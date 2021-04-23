import json
import sys

input_name = sys.argv[1]
output_name = sys.argv[2]

input_fd = open(input_name, 'r')
output_fd = open(output_name, 'w')

inp = json.load(input_fd)


# build dictionaries ---------------------------

p_k = {}
p_k1 = {}
trans_mat = {}
for item in inp["transition_function"]:
    trans_mat[tuple([item[0],item[1]])] = item[2]
for item in inp["states"]:
    p_k[item] = []
    p_k1[item] = []


# build P0-----------------------------------

final = []
non_final = []
for item in inp["final_states"]:
    final.append(item)
for item in inp["states"]:
    if item not in final:
        non_final.append(item)
for i in range(len(final)):
    p_k[final[0]].append(final[i])

for i in range(len(non_final)):
    p_k[non_final[0]].append(non_final[i])


def check_equivalence(state1, state2):
    for letter in inp["letters"]:
        end_1 = trans_mat[tuple([state1, letter])]
        end_2 = trans_mat[tuple([state2, letter])]
        for item in p_k:
            flag=0
            for i in p_k[item]:
                if i == end_1:
                    flag+=1
                if i == end_2:
                    flag+=1
            if flag == 1:
                flag=0
                return False
    return True
# build P1------------------------------------

for item in p_k:
    for i in p_k[item]:
        if check_equivalence(i, item):
            p_k1[item].append(i)
            continue
        flag=0
        for key in p_k1:
            if len(p_k1[key]) != 0 and check_equivalence(i, key):
                flag=1
                p_k1[key].append(i)
                break
        if flag==0:
            p_k1[i].append(i)

# build Pk using P(k-1) ----------------------------

while p_k != p_k1:
    p_k = p_k1
    p_k1 = {}
    for item in inp["states"]:
        p_k1[item] = []
    for item in p_k:
        for i in p_k[item]:
            if check_equivalence(i, item):
                p_k1[item].append(i)
                continue
            flag=0
            for key in p_k1:
                if len(p_k1[key]) != 0 and check_equivalence(i, key):
                    flag=1
                    p_k1[key].append(i)
                    break
            if flag==0:
                p_k1[i].append(i)


# print(p_k,'\n\n\n',p_k1)

DFA ={
    "states": [],
    "letters": [],
    "transition_function": [],
    "start_states": [],
    "final_states": []
}

for key in p_k1:
    if len(p_k1[key]) == 0:
        continue
    DFA["states"].append(p_k1[key])

for state in inp["start_states"]:
    for key in p_k1:
        if state in p_k1[key]: 
            if p_k1[key] not in DFA["start_states"]:
                DFA["start_states"].append(p_k1[key])
            break
for state in inp["final_states"]:
    for key in p_k1:
        if state in p_k1[key]: 
            if p_k1[key] not in DFA["final_states"]:
                DFA["final_states"].append(p_k1[key])
            break
DFA["letters"] = inp["letters"]

for state in DFA["states"]:
    for letter in DFA["letters"]:
        end = trans_mat[(state[0],letter)]
        for item in DFA["states"]:
            if end in item:
                DFA["transition_function"].append([state,letter, item])
                break
        


json.dump(DFA,output_fd, indent=4)