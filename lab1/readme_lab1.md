# dependencies:
- graph_tool
- pycairo
- python3-gi-cairo
- matplotlib
- argparse

if on WSL2, add window displaying means like x11-apps

--------------------

# usage via linux console:
data always has to be prefixed with encoding type:
- 'ls' for lista sasiedztwa
- 'ms' for macierz sasiedztwa
- 'mi' for macierz incydencji

## task 1: encode.py 
available arguments:
- --input_file              like 'in.txt', file with input data
- -s / --save               whether to save (if -of not specified, saves with default name) (if -of specified, this flag is unnecessary)
- -of / --output_file       like 'out.txt', where to output data
- -ot / --output_type       encoding type to output (ls/ms/mi/all - all will output the other 2 the input wasn't encoded in)

those two work the same way:

python3 encode.py input.txt -of=output.txt -ot=ms

cat input.txt | python3 encode.py -of=output.txt -ot=ms

## task 2: graph.py
takes only macierze sasiedztwa

available arguments:
- --input_file              like 'in.txt', file with input data
- -s / --save               whether to save (if -of not specified, saves with default name) (if -of specified, this flag is unnecessary)
- -of / --output_file       like 'out.png', where to output graph
- -is / --image_size        output image will be square with a side of this length (in pixels)
- -ew / --edge_width        width of the drawn edges, float

python3 graph.py input_ms.txt

python3 graph.py input_BIG_ms.txt -of=output_READABLE_graph.png -is=3000 -ew=0.5

python3 encode.py input_ls.txt -ot=ms | python3 graph.py -s


## task 3: generate.py
outputs only macierz sasiedztwa

available arguments:
- -of / --output_file       like 'out.txt', where to output data
- -s / --save               whether to save (if -of not specified, saves with default name) (if -of specified, this flag is unnecessary)
- -n / --vertex_amount      number of vertices (n)
- -m / --mode               what mode to run program in (l/p - 'l' is number of edges; 'p' is probability of an edge existing)
- -mv / --mode_value        if mode is 'l': int - number of edges; if mode is 'p': float [0.0,1.0] - probability

python3 generate.py -s -n=7 -m=l -mv=10

python3 generate.py -n=30 -m=p -mv=0.2

python3 generate.py -n=100 -m=p -mv=0.9 | python3 graph.py -of=output_READABLE_graph.png -is=3000 -ew=0.5
