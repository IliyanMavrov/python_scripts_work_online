#!/usr/bin/python3

import sys
import re

def find_and_delete(log_file, keyword):
    # Compile a regex pattern to match the keyword
    pattern = re.compile(keyword)

    # Open the log file and read its contents
    with open(log_file, 'r') as f:
        log_data = f.read()

    # Find all occurrences of the keyword in the log data
    matches = pattern.finditer(log_data)

    count = 0  # Count how many times the keyword was found
    for match in matches:
        count += 1

    print(f"The keyword '{keyword}' was found {count} times.")

    # Ask user if they want to delete all rows where word is found
    response = input("Do you want to delete all rows where the keyword is found? (y/n): ")

    if response.lower() == 'y':
        # Split the log data into lines
        log_lines = log_data.split('\n')

        # Initialize an empty list to store the modified log lines
        modified_log_lines = []

        for line in log_lines:
            if pattern.search(line):
                continue  # Skip this line, as it contains the keyword
            modified_log_lines.append(line)

        # Write the processed log data back to a new file (with the same name + "_processed")
        with open(log_file.replace('.log', '_processed.log'), 'w') as f:
            f.write('\n'.join(modified_log_lines))

    print("Script finished.")

def write_output_to_file(processed_log_file, original_log_file):
    # Read the processed log data
    with open(processed_log_file, 'r') as f:
        processed_data = f.read()

    # Write the output to a new file (with a default name)
    with open('output.log', 'w') as f:
        f.write(f"Processed {original_log_file}:\n{srt(processed_data)}")

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(f"Usage: python {sys.argv[0]} <log_file> <keyword>")
        sys.exit(1)

    log_file = sys.argv[1]
    keyword = sys.argv[2]

    find_and_delete(log_file, keyword)
    write_output_to_file(log_file.replace('.log', '_processed.log'), log_file)


# USAGE: 
#   It takes two command-line arguments: log_file (the name of the .log file to search) and keyword (the word to search for).
#   It compiles a regex pattern to match the keyword.
#   It opens the log file, reads its contents, and finds all occurrences of the keyword using the compiled pattern.
#   It counts how many times the keyword was found.
#   It asks the user if they want to delete all rows where the keyword is found.
#   If the user responds with "y", it splits the log data into lines, initializes an empty list to store the modified log lines, and iterates through each line. If a line contains the keyword, it skips that line; otherwise, it adds the line to the modified log list.
#   It writes the modified log data back to a new file (with the same name as the original file, but with ".processed" appended).
#
#       $ python log_search.py my_log_file.log my_keyword