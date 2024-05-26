# dependencies:
- graph_tool
- pycairo
- python3-gi-cairo
- matplotlib
- argparse
- typing

if on WSL2, add window displaying means like x11-apps

--------------------

# usage via linux console:

## task 1: pagerank.py 

available arguments:
- --input_file                  file with input data
- -s / --save                   whether to save output (with default name)
- -of / --output_file           name of file to save output to (-s flag is unnecessary)
- -n / --iterations             number of random walk iterations (ignored in power iteration mode)
- -d / --teleportation_probability       probability of teleportation to a random node
- -m / --mode                   "r" for random walk or "p" for power iteration

python3 pagerank.py input.txt -m=r -n=1000000 -d=0.15 

python3 pagerank.py input.txt -m=p -d=0.15 -of=output_power_iteration.txt


## task 2: komiwojazer.py

available arguments:
- --input_file                  file with input data
- -s / --save                   whether to save output (with default name)
- -of / --output_file           name of file to save output to (-s flag is unnecessary)
- -vv / --visible_vertices      make vertices visible on output
- -it / --iterations            number of monte carlo iterations for each temperature change


python3 komiwojazer.py input.dat -s -vv -it=50000

python3 komiwojazer.py input.dat -of=output.dat -it=1000
