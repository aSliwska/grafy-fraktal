from graph_tool.all import *
import sys
import argparse
import math
import random
import time
from typing import List


# input: list of point coordinates x y, each in new line
# output: window displaying a graph with a shortest path through all points + output file if specified


def calc_distance(a: List[int], b: List[int]) -> float:
	return ((a[0] - b[0])*(a[0] - b[0]) + (a[1] - b[1])*(a[1] - b[1]))**0.5


def calc_route_length(route: List[int], coords: List[List[int]]) -> float:
	distance: float = 0
	for i in range(len(route) - 1):
		distance += calc_distance(coords[route[i]], coords[route[i+1]])

	return distance


def reverse_subroute(idx_a: int, idx_d: int, route: List[int]) -> List[int]:
	# reverse direction between a and d
	route[idx_a+1:idx_d] = route[idx_a+1:idx_d][::-1]
	return route


def montecarlo(coords: List[List[int]], iterations: int):
	noOfVertices: int = len(coords)

	# create a start route
	route: List[int] = [i for i in range(1, noOfVertices)]
	random.shuffle(route)
	route = [0] + route + [0]

	# monte carlo
	distance: float = calc_route_length(route, coords)
	print(distance)
	smallest_distance: float = distance

	for strength in range(100, 0, -1):
		temperature: float = 0.001*strength*strength 
		start_time: float = time.time()

		for it in range(0, iterations):
			# randomise a and d
			idx_a: int = random.randint(0, noOfVertices - 3)
			idx_d: int = random.randint(idx_a + 3, noOfVertices) if idx_a != 0 else random.randint(idx_a + 3, noOfVertices - 1)
			
			# check if the new route is better
			new_distance: float = distance - calc_distance(coords[route[idx_a]], coords[route[idx_a + 1]]) - calc_distance(coords[route[idx_d]], coords[route[idx_d - 1]]) + calc_distance(coords[route[idx_a]], coords[route[idx_d - 1]]) + calc_distance(coords[route[idx_d]], coords[route[idx_a + 1]])

			if new_distance < distance:
				distance = new_distance
				route = reverse_subroute(idx_a, idx_d, route)
			else:
				# if it's worse, there's still a chance it'll be accepted
				r: float = random.random()
				if r <= math.exp(-(new_distance - distance)/temperature):
					distance = new_distance
					route = reverse_subroute(idx_a, idx_d, route)
			
			if (smallest_distance > distance):
				smallest_distance = distance
				# print(strength, '-', it, ':', smallest_distance)
		
		end_time: float = time.time()
		print(strength, ':', smallest_distance, f'(time: {(end_time - start_time):.4f}s)')

	print('final :', distance)

	edges = []
	
	for i in range(1, noOfVertices + 1):
		edges.append([route[i-1], route[i]])

	return edges


# read args the program was run with
def read_args():
	argparser = argparse.ArgumentParser(
		prog='Komiwojazer',
		description='Szuka najkrotszej sciezki, ktora przechodzi przez wszystkie podane punkty.',
	)

	# input file name (if not piping input)
	if sys.stdin.isatty():
		argparser.add_argument('input_file')

	# change output file name and save
	argparser.add_argument('-of', '--output_file', default="komiwojazer.png")

	# save even if output file name is default
	argparser.add_argument('-s', '--save', action='store_true')

	# show vertices on output
	argparser.add_argument('-vv', '--visible_vertices', action='store_true')

	# number of iterations
	argparser.add_argument('-it', '--iterations', required=True)

	return argparser.parse_args()


def read_input(args):
	# pipe input stream from stdin if present, else read provided input file
	input_stream = sys.stdin if not sys.stdin.isatty() else open(args.input_file, 'r')
      
	input_data = []
	for line in input_stream:
		if len(line.strip()) != 0:
			input_data.append([int(el) for el in line.strip().split(' ')])
    
	return input_data


def main():
	args = read_args()
	print('----- reading input -----')
	input_data = read_input(args)

	vertices_amount = len(input_data)
	
	
	print('----- adding vertices -----')
	graph = Graph(directed=False)
	graph.add_vertex(vertices_amount)

	pos = graph.new_vertex_property("vector<double>")
	
	for i in range(vertices_amount):
		pos[graph.vertex(i)] = input_data[i]

	if not args.visible_vertices:
		shape = graph.new_vertex_property("int")

		for i in range(vertices_amount):
			shape[graph.vertex(i)] = 15 # 15 == 'none'


	print('----- finding shortest path -----')
	edge_list = montecarlo(input_data, int(args.iterations))

	print('----- adding edges -----')
	graph.add_edge_list(edge_list)


	print('----- drawing -----')
	if args.visible_vertices:
		if args.save or args.output_file != 'komiwojazer.png':
			graph_draw(graph, pos=pos, bg_color='white', output=args.output_file, ink_scale=0.125, edge_pen_width=6, output_size=(1500, 1500))
		graph_draw(graph, pos=pos, bg_color='white', ink_scale=0.75, edge_pen_width=1)

	else:
		if args.save or args.output_file != 'komiwojazer.png':
			graph_draw(graph, pos=pos, bg_color='white', output=args.output_file, ink_scale=0.5, output_size=(1500, 1500), vprops={'shape' : shape})
		graph_draw(graph, pos=pos, bg_color='white', ink_scale=0.5, vprops={'shape' : shape})
		

if __name__ == "__main__":
    main()