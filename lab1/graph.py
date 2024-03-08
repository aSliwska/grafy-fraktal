from graph_tool.all import *
import sys
import argparse
from enum import Enum
import math


# input: adjacency matrix
# output: image of a graph with a circular layout


# input file encoding (specified at the beginning of the file)
class InputType(Enum):
	ADJACENCY_LIST = 'ls'
	ADJACENCY_MATRIX = 'ms'
	INCIDENCE_MATRIX = 'mi'


# read args the program was run with
def read_args():
	argparser = argparse.ArgumentParser(
		prog='Grapher',
		description='Rysuje prosty graf na obwodzie koła.',
	)

	# input file name (if not piping input)
	if sys.stdin.isatty():
		argparser.add_argument('input_file')

	# change output file name and save
	argparser.add_argument('-of', '--output_file', default="graph.png")

	# save even if output file name is default
	argparser.add_argument('-s', '--save', action='store_true')

	# height and width of output image in pixels 
	argparser.add_argument('-is', '--image_size', default=600)

	argparser.add_argument('-ew', '--edge_width', default=10.0)

	return argparser.parse_args()


def read_input(args):
	# pipe input stream from stdin if present, else read provided input file
	input_stream = sys.stdin if not sys.stdin.isatty() else open(args.input_file, 'r')
    
	# first line in input should contain the encoding type
	input_type_string = input_stream.readline().strip()
	if (input_type_string not in [it.value for it in InputType]):
		raise ValueError('first line in file must indicate encoding type')
	input_type = InputType(input_type_string)
      
	input_data = []
	for line in input_stream:
		if len(line.strip()) != 0:
			input_data.append(line.strip().split(' '))
    
	return input_type, input_data


def main():
	args = read_args()
	input_type, input_data = read_input(args)

	if input_type != InputType.ADJACENCY_MATRIX:
		print('graph needs to be encoded as an adjacency matrix')
		return

	# the entire edge list needs to be added at once to the graph for graph_tool to work quickly
	edge_list = []
	vertices_amount = len(input_data)
	for row in range(vertices_amount):
		for col in range(row + 1, vertices_amount):
			if (input_data[row][col] == '1'):
				edge_list.append((row, col))

	graph = Graph(directed=False)
	graph.add_vertex(vertices_amount)
	graph.add_edge_list(edge_list)

	# calculate coordinates of vertices 
	# default circular graphs either have edge bundling or don't keep the order of vertices (and so big graphs optimize forever)
	positions = []
	alpha = 2 * math.pi / vertices_amount
	r = 1000.0
	pos = graph.new_vertex_property("vector<double>")
	for i in range(vertices_amount):
		pos[graph.vertex(i)] = (1000.0 + r * math.cos(i * alpha), 1000.0 + r * math.sin(i * alpha))

	if args.save or args.output_file != 'graph.png':
		graph_draw(graph, pos=pos, vertex_text=graph.vertex_index, output=args.output_file, output_size=(int(args.image_size), int(args.image_size)), edge_pen_width=float(args.edge_width))

	graph_draw(graph, pos=pos, vertex_text=graph.vertex_index)
		

if __name__ == "__main__":
    main()