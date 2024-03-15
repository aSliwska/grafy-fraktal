# dependencies:
- matplotlib
- networkx

--------------------

## task 1: graphic_sequence.py
input: 
sequence of graph node degrees

output:
visualization of graph (if the sequence is a valid graphic sequence)

available arguments:
- -if       input file containing list of degrees ex. python3 graphic_sequence.py -if example_sequence.txt
- -sq       list of degrees separated by spaces ex. python3 graphic_sequence.py -sq 4 4 3 2 2 1 1 1

## task 2: randomize.py
first line of input file has to be 'ms'
input:
adjacency matrix

argument:
input file containing adjacency matrix
ex. python3 randomize.py example_ms.txt

## task 3: component.py
first line of input file has to be 'ms'
input:
adjacency matrix

argument:
input file containing adjacency matrix
ex. python3 component.py example_ms.txt

