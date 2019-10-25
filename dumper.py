#!/usr/bin/env python3

import sys
import os
import re
from textwrap import wrap

hexline_pattern = re.compile(r"([0-9a-f]{4}):\s+((?:[0-9a-f]{4} )+)")
whitespace_pattern = re.compile(r"\s+")

def main():
    if not check_args():
        usage()
        return

    inf = sys.stdin

    with get_outfile(sys.argv[1]) as outf:
        lines = inf.read().splitlines()
        image = extract_image(lines)
        outf.write(image)

def extract_image(lines):
    mem_map = dict(filter(lambda x: x[0] != None, map(decode_line, lines)))

    last_addr = 0
    image = []
    for addr, line_bytes in mem_map.items():
        if is_gap(addr, last_addr):
            fill_gap(image, addr, last_addr)
        image.extend(line_bytes)
        last_addr = addr

    return bytearray(image)

def is_gap(addr, last_addr):
    return addr > last_addr + 16

def fill_gap(image_bytes, addr, last_addr):
    for i in range(0, (addr-last_addr)-16):
        image_bytes.append(0)

def decode_line(line):
    match = hexline_pattern.search(line)
    if match is None:
        return (None, None)
    addr = int(match.group(1), 16)
    line_bytes = extract_line_bytes(match.group(2))
    return (addr, line_bytes)

def extract_line_bytes(byte_str):
    clean_byte_str = re.sub(whitespace_pattern, "", byte_str)
    return list(map(lambda x: int(x, 16), wrap(clean_byte_str, 2)))

def check_args():
    if len(sys.argv) != 2:
        return False
    return True

def usage():
    print(f"Usage: {sys.argv[0]} <output path>")
    print()
    print("Input is read from stdin.")

def get_outfile(path):
    return os.fdopen(sys.stdout.fileno(), "wb", closefd=False)

main()
