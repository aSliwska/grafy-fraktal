import sys
import argparse
from enum import Enum
import random


# input: number of vertices and either the number of edges or a probability of an edge existing
# output: an adjacency matrix


# the mode in which the program was run in
class Mode(Enum):
	EDGE_AMOUNT = 'l'
	EDGE_PROBABILITY = 'p'


# read args the program was run with
def read_args():
    argparser = argparse.ArgumentParser(
	    prog='Generator',
        description='Generuje prosty graf o liczbie wierzcholkow n oraz albo liczbie krawedzi l, albo prawdopodobienstwie wystapienia krawedzi p.',
    )

	# change output file name and save
    argparser.add_argument('-of', '--output_file', default="generate.txt")

	# save even if output file name is default
    argparser.add_argument('-s', '--save', action='store_true')

    argparser.add_argument('-n', '--vertex_amount', required=True)

	# -m=l -mv=14		sets the number of edges to 14
	# -m=p -mv=0.4		sets the probability of an edge existing to 0.4
    argparser.add_argument('-m', '--mode', choices=[m.value for m in Mode])
    argparser.add_argument('-mv', '--mode_value', required=True)

    return argparser.parse_args()


def main():
	args = read_args()
	shouldSave = args.save or args.output_file != 'generate.txt'
	edges = [] # list of edges that will be drawn
	vertex_amount = int(args.vertex_amount)

	match Mode(args.mode):
		case Mode.EDGE_AMOUNT:
			# lists all edges and chooses a user defined amount of them at random
			edge_amount = int(args.mode_value)
			available_edges = [[a, b] for a in range(vertex_amount) for b in range(a + 1, vertex_amount)]

			for _ in range(edge_amount):
				index = random.randrange(len(available_edges))
				edge = available_edges.pop(index)
				edges.append(edge)

		case Mode.EDGE_PROBABILITY:
			# rolls the dice for the appearance of every edge in the graph, one by one
			probability = float(args.mode_value)

			for row in range(vertex_amount):
				for col in range(row + 1, vertex_amount):
					if random.random() < probability:
						edges.append([row, col])

	output = generate_output(vertex_amount, edges)
	print_output(shouldSave, args.output_file, output)


# saves to file (if user specified to save) and prints to console
def print_output(shouldSave, output_file, output):
	if shouldSave:
		format_and_print(output_file, output)
	format_and_print(sys.stdout, output)
	print('')


# example:
# 	output from [['ms'], ['0', '1', '1'], ['1', '0', '0'], ['1', '0', '0']]:
#	ms
#	0 1 1
#	1 0 0
#	1 0 0
def format_and_print(stream, data):
	if stream != sys.stdout:
		stream = open(stream, 'w')
	print('\n'.join([' '.join(row) for row in data]), end='', file=stream)


# generates an adjacency matrix
# example output: [['ms'], ['0', '1', '1'], ['1', '0', '0'], ['1', '0', '0']]
def generate_output(vertex_amount, edges):
	output = [['0' for _ in range(vertex_amount)] for _ in range(vertex_amount)]

	for edge in edges:
		output[edge[0]][edge[1]] = '1'
		output[edge[1]][edge[0]] = '1'

	return [['ms']] + output


if __name__ == "__main__":
    main()