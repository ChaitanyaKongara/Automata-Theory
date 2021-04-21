# Programming Assignment

Assignment consists of 4 questions:
1. Conversion of Regex to NFA
2. Conversion of NFA to DFA
3. Conversion of DFA to regex
4. Minimization of DFA

***

## Question 1:
### Conversion of Regex to NFA
***
## Question 2:
### Conversion of NFA to DFA

Run the python script using the following command

```bash

python3 q2.py input.json output.json

```
Where input.json consists of the formatted version of NFA and output.json will be created on execution of q2.py python script and consists of equivalent DFA of any number of states.

convert the given json object into a python dictionary (inp - name) using json.load() command

```python
input_name = sys.argv[1]
input_fd = open(input_name, 'r')
inp = json.load(input_fd)
```

Steps that are involved in the conversion
* Bulding 2<sup>k</sup> states of the DFA:

    We have 2<sup>k</sup> states, so each state can be represented by a number in the range of [0,2<sup>k</sup>). Each state in a DFA is nothing but a set of states corresponding to the NFA. Binary representation of the number present on the states of DFA, tells us what all states of NFA are used in bulding this state in DFA.  
    If i<sup>th</sup> bit (from right, starting from 0) of the binary representation is set on then it consists of the state Q<sub>i</sub>.

    Ex:     
        state that's represented by 0(00...00) is []<br/>
        state that's represented by 2(00...10) is [Q1]<br/>
        state that's represented by 3(0...11) is [Q0, Q1]<br/>
        state that's represented by 5(00...101) is [Q0,Q2]

* Finding start, final states and letters of the DFA:
    
    Letters and start states of the DFA start states remains the same as that of NFA. If Q<sub>0</sub> is the final state in NFA, then all states in DFA that consists of this state Q<sub>0</sub> are final states

    Ex:
        [Q0], [Q0, Q1], [Q0,Q2] etc....
* Bulding transition matrix:

    Here we build a transition matrix of size "2<sup>k</sup>L", this matrix tells us what state the system takes us to, when we are present on state [..., Qi,...] and if we get a particular input letter. This matrix is built using the transition matrix(Let it be nfa_t) of NFA which consist of transition if the current state(in DFA) consists of just one state(of NFA) and build the remaining matrix for states(Of DFA) that consistis of multiple states(of NFA) 

    Incase of states(Of DFA) with multiple states (of NFA) present in it. Use the nfa_t matrix for every single state present in the set of states and take the unique elements formed as the output and store the result in the transition matrix of dfa.

* output.json:

    make a python dictionary that consist of the 5-Tuple information of the DFA and use json.dump() to make it into a JSON object.

***
## Question 3:
### Conversion of DFA to regex

First of all we need to slightly modify the DFA, which reduce the complexity of problem when DFA consists the case of multiple final and start states.

* Add a new start state and ε edges connecting it with start states and remove the start state status.
* Add a new final state and ε edges connecting it with final states and remove the final state status.

The formed state diagram is known as Generalized NFA and from now start removing non-initial or non-final state one at a time and replace the paths that involve this removed state with corresponding regular expressions.

Final regular expression present between newly created start state and final state is our answer.

***
## Question 4:
### Minimization of DFA

Run the python script using the following command

```bash

python3 q4.py input.json output.json

```
Where input.json consistsof some DFA and output.json will be created on execution of q4.py python script and consists of equivalent DFA with as minimum number of states as possible.

Equivalent states:
    
Two states p,q  are said to be k-equivalent if they are present in the same set in partition P<sub>k-1</sub> and if for every input letter a, δ(p,a) and δ(q,a) belong to the same set in the partition P<sub>k-1</sub>.

partition 0 (P<sub>0</sub>):

Divide the total set of states into 2 sets, one coreesponding to non-final states and the other correspponding to final states.

partition k(P<sub>k</sub>):

consider the sets of P<sub>k-1</sub> individually and check the equivalence condition for all the pairs possible pairs of the same set in P<sub>k-1</sub> and if they are equivalent they are going to be in the same set even in the next partition P<sub>k</sub> orelse they just go into 2 different sets.

Follow the process untill P<sub>k-1</sub> becomes P<sub>k</sub>, each set in the final partition are nothing but states in the minimized DFA. 

Finally build the minimized DFA using the partition P<sub>k</sub>

***