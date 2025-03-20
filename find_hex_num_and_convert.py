#!/usr/bin/python3

import re
import os

def extract_hex_values(log_file):
    """
    Extract hexadecimal numbers starting with "0x" from the log file
    """
    hex_pattern = r'0[xX][0-9a-fA-F]+'
    hex_strings = []
    with open(log_file, 'r') as f:
        for line in f:
            matches = re.findall(hex_pattern, line)
            hex_strings.extend(matches)
    return hex_strings

def convert_to_binary_and_decimal(hex_values):
    """
    Convert hexadecimal values to binary and decimal
    """
    conversion_results = []
    for hex_value in hex_values:
        decimal_value = int(hex_value, 16)  # Convert hex to decimal
        binary_value = bin(int(hex_value, 16))[2:]  # Convert hex to binary
        conversion_results.append((hex_value, decimal_value, binary_value))
    return conversion_results

log_file = './find_hex_num_and_convert_test.log'  # Replace with your log file path
output_file = 'result_hex_convert.txt'  # Output file name

hex_values = extract_hex_values(log_file)
conversion_results = convert_to_binary_and_decimal(hex_values)

with open(output_file, 'w') as f:
    print("Hex\tDecimal\tBinary", file=f)
    for hex_value, decimal_value, binary_value in conversion_results:
        print(f"{hex_value}\t{decimal_value}\t{binary_value}", file=f)