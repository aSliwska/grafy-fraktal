#!/usr/bin/env python
import sys
import argparse
from enum import Enum


# input: graph encoded as an adjacency list, adjacency matrix or incidence matrix
# output: graph(s) encoded as the user specified type


class InputType(Enum):
	ADJACENCY_LIST = 'ls'
	ADJACENCY_MATRIX = 'ms'
	INCIDENCE_MATRIX = 'mi'

class OutputType(Enum):
	ADJACENCY_LIST = 'ls'
	ADJACENCY_MATRIX = 'ms'
	INCIDENCE_MATRIX = 'mi'
	ALL = 'all'


# read args the program was run with
def read_args():
	argparser = argparse.ArgumentParser(
		prog='Encoder',
		description='Przekodowuje reprezentacje grafowe na inne. Pracuje na macierzach sąsiedztwa, macierzach incydencji i listach sąsiedztwa.',
	)

	# input file name (if not piping input)
	if sys.stdin.isatty():
		argparser.add_argument('input_file')

	# change output file name and save
	argparser.add_argument('-of', '--output_file', default="encode.txt")

	# save even if output file name is default (output is always printed to console)
	argparser.add_argument('-s', '--save', action='store_true')

	# output type: adjacency list, adjacency matrix, incidence matrix, all that don't match input file
	argparser.add_argument('-ot', '--output_type', choices=[ot.value for ot in OutputType], required=True)

	return argparser.parse_args()


def read_input(args):
	# pipe input stream from stdin if present, else read file provided via input_file argument
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
	output_type = OutputType(args.output_type)
	shouldSave = args.save or args.output_file != 'encode.txt'
	
	match output_type:
		case OutputType.ADJACENCY_LIST:
			output = encode_adjacency_list(input_type, input_data)

		case OutputType.ADJACENCY_MATRIX:
			output = encode_adjacency_matrix(input_type, input_data)

		case OutputType.INCIDENCE_MATRIX:
			output = encode_incidence_matrix(input_type, input_data)

		case OutputType.ALL:
			if input_type != InputType.ADJACENCY_LIST:
				output = encode_adjacency_list(input_type, input_data)
				print_output(shouldSave, args.output_file, OutputType.ADJACENCY_LIST.value, output)

			if input_type != InputType.ADJACENCY_MATRIX:
				output = encode_adjacency_matrix(input_type, input_data)
				print_output(shouldSave, args.output_file, OutputType.ADJACENCY_MATRIX.value, output)

			if input_type != InputType.INCIDENCE_MATRIX:
				output = encode_incidence_matrix(input_type, input_data)
				print_output(shouldSave, args.output_file, OutputType.INCIDENCE_MATRIX.value, output)

			return
	
	print_output(shouldSave, args.output_file, output_type.value, output)


# saves to file (if user specified to save) and prints to console
def print_output(shouldSave, output_file, output_type, output):
	if shouldSave:
		output_file = output_file.split('.')[0] + '_' + output_type + '.' + output_file.split('.')[-1]
		format_and_print(output_file, output)

	format_and_print(sys.stdout, output)
	print('')


# example:
# 	output from [['ms'], ['0', '1', '1'], ['1', '0', '0'], ['1', '0', '0']]:
#	ms
#	0 1 1
#	1 0 0
#	1 0 0
def format_and_print(stream, output):
	if stream != sys.stdout:
		stream = open(stream, 'w')
	print('\n'.join([' '.join(row) for row in output]), end='', file=stream)


def encode_adjacency_list(input_type, input_data) -> list[list[str]]:
	if input_type == InputType.ADJACENCY_LIST:
		return [[input_type.value]] + input_data
	
	output = [[] for _ in input_data]

	for i in range(len(input_data)):
		output[i].append(str(i) + ".")

	match input_type:
		case InputType.ADJACENCY_MATRIX:
			output = decode_adjacency_matrix(input_data, output, update_adjacency_list)
		
		case InputType.INCIDENCE_MATRIX:
			output = decode_incidence_matrix(input_data, output, update_adjacency_list)
	
	return [[OutputType.ADJACENCY_LIST.value]] + output


def encode_adjacency_matrix(input_type, input_data) -> list[list[str]]:
	if input_type == InputType.ADJACENCY_MATRIX:
		return [[input_type.value]] + input_data
	
	output = [['0' for _ in input_data] for _ in input_data]

	match input_type:
		case InputType.ADJACENCY_LIST:
			output = decode_adjacency_list(input_data, output, update_adjacency_matrix)

		case InputType.INCIDENCE_MATRIX:
			output = decode_incidence_matrix(input_data, output, update_adjacency_matrix)

	return [[OutputType.ADJACENCY_MATRIX.value]] + output


def encode_incidence_matrix(input_type, input_data) -> list[list[str]]:
	if input_type == InputType.INCIDENCE_MATRIX:
		return [[input_type.value]] + input_data
	
	output = [[] for _ in input_data]

	match input_type:
		case InputType.ADJACENCY_LIST:
			output = decode_adjacency_list(input_data, output, update_incidence_matrix)
		
		case InputType.ADJACENCY_MATRIX:
			output = decode_adjacency_matrix(input_data, output, update_incidence_matrix)
			
	return [[OutputType.INCIDENCE_MATRIX.value]] + output


def decode_adjacency_list(input_data, output, update_function):
	# for each vertex, pay attention only to connections to vertices with higher indexes
	for row in range(len(input_data)):
		first_index = int(input_data[row][0][:-1])

		for col in range(1, len(input_data[row])):
			if int(input_data[row][col]) > first_index:
				output = update_function(output, first_index, int(input_data[row][col]))

	return output


def decode_adjacency_matrix(input_data, output, update_function):
	# search top triangle of the matrix for 1s
	for row in range(len(input_data)):
		for col in range(row + 1, len(input_data)):
			if input_data[row][col] == '1':
				output = update_function(output, row, col)
	return output


def decode_incidence_matrix(input_data, output, update_function):
	# search column after column for pairs of 1s
	for col in range(len(input_data[0])):
		first_found_index = -1

		for row in range(len(input_data)):

			if input_data[row][col] == '1':
				# save the index at which you found the first 1
				if first_found_index == -1:
					first_found_index = row

				# when you find the second, add the edge to the output
				else:
					output = update_function(output, row, first_found_index)
					break

	return output


def update_adjacency_list(output, row, col):
	output[row].append(str(col))
	output[col].append(str(row))
	return output


def update_adjacency_matrix(output, row, col):
	output[row][col] = '1'
	output[col][row] = '1'
	return output


def update_incidence_matrix(output, row, col):
	# append 1 if vertex index is equal row or col, otherwise append 0
	# this is a no-if-checks-version (i can't bring myself to write a loop with that many 
	# unnecessary if-checks even if it would be more readable)
	for vertex_index in range(row):
		output[vertex_index].append('0')

	output[row].append('1')

	for vertex_index in range(row + 1, col):
		output[vertex_index].append('0')

	output[col].append('1')

	for vertex_index in range(col + 1, len(output)):
		output[vertex_index].append('0')

	return output


if __name__ == "__main__":
    main()