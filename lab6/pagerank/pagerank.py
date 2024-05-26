#!/usr/bin/env python
import sys
import argparse
import random
from enum import Enum

# input: adjacency list
# output: pagerank ranking with scores


class Mode(Enum):
	RANDOM_WALK = 'r'
	POWER_ITERATION = 'p'


def read_args():
	# read args the program was run with
	
	argparser = argparse.ArgumentParser(
		prog='PageRank',
		description='Ocenia ważność wierzchołków w grafie skierowanym na podstawie algorytmu pagerank.',
	)

	# input file name (if not piping input)
	if sys.stdin.isatty():
		argparser.add_argument('input_file')

	# change output file name and save
	argparser.add_argument('-of', '--output_file', default="pagerank.txt")

	# save even if output file name is default (output is always printed to console)
	argparser.add_argument('-s', '--save', action='store_true')

	# number of iterations for random walk
	argparser.add_argument('-n', '--iterations', default=1000000)
	
	argparser.add_argument('-d', '--teleportation_probability', required=True)

	# "r" for random walk or "p" for power iteration
	argparser.add_argument('-m', '--mode', required=True)

	return argparser.parse_args()


def read_input(args):
	# pipe input stream from stdin if present, else read file provided via input_file argument
	input_stream = sys.stdin if not sys.stdin.isatty() else open(args.input_file, 'r')
      
	input_data = dict()
	for line in input_stream:
		if len(line.strip()) != 0:
			line = line.split(':')
			input_data[line[0].strip()] = [s.strip() for s in line[1].split(',')]
	
	if args.mode not in [m.value for m in Mode]:
		raise ValueError('mode must be either "r" (random walk) or "p" (power iteration)')
	mode = Mode(args.mode)
    
	return input_data, mode


def random_walk(adjacency_list: dict, iterations: int, teleportation_probability: float) -> list:
	
	times_visited = dict()
	for node in adjacency_list.keys():
		times_visited[node] = 0

	# choose random start node
	cur_node = random.choice(list(adjacency_list.keys()))
	times_visited[cur_node] += 1

	for it in range(iterations):
		if (random.random() < teleportation_probability) or (len(adjacency_list[cur_node]) == 0):
			# teleport to random node (including current node)
			cur_node = random.choice(list(adjacency_list.keys()))
		else:
			# move to random neighbour
			cur_node = random.choice(adjacency_list[cur_node])
		
		times_visited[cur_node] += 1

	# get [node, score] list and reverse sort it
	return sorted([(node, visits/iterations) for node, visits in times_visited.items()], key=lambda node: node[1], reverse=True)


def power_iteration(adjacency_list: dict, teleportation_probability: float) -> list:
	node_names = list(adjacency_list.keys())
	node_indices = {node: i for i, node in enumerate(node_names)}

	vertex_count = len(adjacency_list)

	stochastic_matrix = [[0 for _ in range(vertex_count)] for _ in range(vertex_count)]

	# first, fill as adjacency matrix
	for node, neighbours in adjacency_list.items():
		for neighbour in neighbours:
			stochastic_matrix[node_indices[node]][node_indices[neighbour]] = 1

	# then change it into a stochastic matrix
	for i in range(vertex_count):
		for j in range(vertex_count):
			out_degree = len(adjacency_list[node_names[i]])
			if out_degree == 0:
				raise ValueError(f"Node {node_names[i]} has out degree == 0")
			
			stochastic_matrix[i][j] *= (1 - teleportation_probability) / out_degree
			stochastic_matrix[i][j] += teleportation_probability / vertex_count

	# multiply vector until convergence
	old_vector = [10] * vertex_count
	new_vector = [1/vertex_count] * vertex_count
	it = 0

	while (vector_difference_length(new_vector, old_vector) > 1e-9):
		it += 1
		old_vector = new_vector.copy()

		for col in range(vertex_count):
			new_vector[col] = 0
			for row in range(vertex_count):
				new_vector[col] += stochastic_matrix[row][col] * old_vector[row]

	print(f"converged in {it} iterations\n")

	return sorted([(node_names[i], new_vector[i]) for i in range(vertex_count)], key=lambda node: node[1], reverse=True)


def vector_difference_length(vector1, vector2):
	return sum([(vector2[i] - vector1[i])**2 for i in range(len(vector1))]) ** 0.5


def main():
	args = read_args()
	input_data, mode = read_input(args)
	
	match mode:
		case Mode.POWER_ITERATION:
			scores: list = power_iteration(input_data, float(args.teleportation_probability))
		case Mode.RANDOM_WALK:
			scores: list = random_walk(input_data, int(args.iterations), float(args.teleportation_probability))

	print_result(scores)

	if args.save or args.output_file != "pagerank.txt":
		with open(args.output_file, 'w') as output_file:
			print_result(scores, output_file)


def print_result(scores, stream = sys.stdout):
	print("rank\tnode\tscore", file=stream)
	for i, (node, score) in enumerate(scores):
		print(f"{i+1}\t{node}\t{score}", file=stream)


if __name__ == "__main__":
    main()