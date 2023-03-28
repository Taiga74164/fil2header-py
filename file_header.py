import sys
import os
import datetime

BYTES_PER_LINE = 16

def read_file_binary(file_path: str) -> bytes:
    try:
        with open(file_path, "rb") as file_stream:
            return file_stream.read()
    except:
        return b''

def write_file_text(file_path: str, in_buffer: str) -> bool:
    try:
        with open(file_path, "w") as file_stream:
            file_stream.write(in_buffer)
            return True
    except:
        return False

def generate_header(binary_name: str, binary_data: bytes) -> str:
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    header = f"// {binary_name} ({now})\n"
    header += f"// StartOffset: 0x00000000, EndOffset: 0x{len(binary_data):08X}, Length: {len(binary_data)} bytes\n"
    header += "#pragma once\n"
    header += "#include <cstdint>\n\n"
    header += "const uint8_t raw_data[] = \n"
    header += "{\n"

    for i, current_byte in enumerate(binary_data):
        if i % BYTES_PER_LINE == 0:
            header += "    "

        hex_string = f"0x{current_byte:02X}"
        header += hex_string

        if i != len(binary_data) - 1:
            header += ", "

        if (i + 1) % BYTES_PER_LINE == 0:
            header += "\n"

    header += "\n};\n"
    return header

def main():
    # Ensure parameters are correctly entered
    if len(sys.argv) != 3:
        # Print an example
        print("Incorrect usage!")
        print("Syntax: " + os.path.basename(sys.argv[0]) + " <input_binary.exe> <output_header.h>")
        print("<input_binary.exe>    Path to any binary file")
        print("<output_header.h>     Path to output file")
        print("Example: " + os.path.basename(sys.argv[0]) + " image.exe image.h")
        sys.exit(1)

    # Read input and output paths
    input_path = sys.argv[1]
    output_path = sys.argv[2]

    # Print paths
    print(f"Input file: {input_path}")
    print(f"Output file: {output_path}")

    # Read input binary data
    binary_data = read_file_binary(input_path)

    if not binary_data:
        print("Couldn't read input file")
        sys.exit(1)

    # Print some info
    print(f"Input file size: 0x{len(binary_data):X}")
    print("Generating file, please wait...")

    # Generate header file
    header = generate_header(os.path.basename(input_path), binary_data)

    # Write file
    if not write_file_text(output_path, header):
        print("Couldn't write output file")
        sys.exit(1)

    # Success!
    print("Success!")

if __name__ == '__main__':
    main()