#!/usr/bin/python3

import os
from argparse import ArgumentParser

def search_folder(folder_path, keyword):
    if not folder_path or not keyword:
        print("Please provide a valid folder path and keyword")
        return

    output_file = f"{keyword}_found.txt"
    
    found_lines = set()

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        
        if os.path.isfile(file_path):  # Check if the path represents a file
            try:
                with open(file_path, 'r') as file:
                    text = file.read()
                    lines = text.split('\n')
                    
                    for i, line in enumerate(lines):
                        if keyword.lower() in line.lower():
                            found_lines.add(f"{filename}:{i+1} - {line.strip()}")
            except Exception as e:
                print(f"{file_path} could not be read due to error: {str(e)}")

    with open(output_file, 'w') as out_file:
        for line in sorted(found_lines):
            out_file.write(line + '\n')
    
    print(f"The results were written to: {output_file}")

def get_user_confirmation():
    confirmation = None

    while confirmation is None:
        user_input = input("File existed for keyword. Overwrite? [Y/N] ")

        if user_input.lower() in ['y', 'yes']:
            return True
        elif user_input.lower() in ['n', 'no']:
            return False
        else:
            print("Invalid input. Please Enter Y/Yes or N/No")

if __name__ == "__main__":
    parser = ArgumentParser(description='Searches for the given keyword in a given folder')
    parser.add_argument('keyword', help='Keyword to search for, case-insensitive')
    parser.add_argument('-f', '--folder-path', required=True, help='Path of the folder to be searched')

    args = parser.parse_args()

    if os.path.exists(args.keyword + '_found.txt'):
        overwrite = get_user_confirmation()
        if not overwrite:
            print("User chose not to overwrite. No results were written.")
            exit(0)

    search_folder(args.folder_path, args.keyword)