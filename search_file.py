#!/usr/bin/python3

import argparse
import re
import os

def search_file(input_filename, search_keyword):
    try:
        with open(input_filename, 'r', newline='') as input_file:
            text = input_file.readlines()
    except FileNotFoundError:
        print(f"Error: File '{input_filename}' not found.")
        return

    output_lines = []
    pattern = re.compile(search_keyword, re.IGNORECASE | re.MULTILINE)
    for line_number, line in enumerate(text, start=1):
        if pattern.search(line):
            print(f"Found match at line {line_number}: {line.strip()}")
            output_lines.append(line)

    if not args.output_file:
        output_filename = 'search_' + search_keyword.replace(' ', '_') + '.txt'
    else:
        output_filename = args.output_file

    # Check if the file already exists
    if os.path.exists(output_filename):
        while True:
            response = input(f'File {output_filename} already exists. Overwrite? Y/N: ')
            if response.lower() in ['y', 'yes']:
                with open(output_filename, 'w') as output_file:
                    output_file.write('\n'.join(map(str, output_lines)))
                print(f'File {output_filename} overwritten.')
                break
            elif response.lower() in ['n', 'no']:
                print('Output was not written.')
                return
    else:
        with open(output_filename, 'w') as output_file:
            output_file.write('\n'.join(map(str, output_lines)))
        print(f'File {output_filename} written.')
    
    print(f'Output file: {output_filename}')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Search file and store lines containing the keyword')
    parser.add_argument('input_filename', help='Input filename to search')
    parser.add_argument('search_keyword', help='Keyword to search for')
    parser.add_argument('-o', '--output-file', default=None, help='Output filename (default: search_text.txt)')
    args = parser.parse_args()
    search_file(args.input_filename, args.search_keyword)
