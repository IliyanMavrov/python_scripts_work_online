#!/usr/bin/python3

def remove_empty_rows(input_file, output_file): 
	with open(input_file, 'r', encoding='utf-8') as infile: 
		lines = infile.readlines() 

	# Filter out empty lines (including those with only whitespace) 
	non_empty_lines = [line for line in lines if line.strip() != '']

	with open(output_file, 'w', encoding='utf-8') as outfile:
		outfile.writelines(non_empty_lines) 

	print(f"Empty rows removed. Output saved to '{output_file}'.") 

# Example usage: 
remove_empty_rows('search_AudioFlinger.txt', 'search_AudioFlinger_no_empty_lines.txt') 