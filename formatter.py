# Author: Erica Ferrua
# 2022-12-05 22:24
# Filename: formatter.py 

def handle(chunk, i):
    # Strip chunk
    chunk = [l.strip() for l in chunk]

    # Max len
    max_len = max(map(len, chunk))

    out = ""

    line = 0
    while line < len(chunk):

        spaces = max_len - len(chunk[line])

        out += f"{chunk[line]}{' '*spaces} = {i}\n"

        i += 1
        line += 1

    return out

with open("./a", "r") as f:
    lines = f.readlines()

out = ""

i = 0
start_line = 0

while start_line < len(lines):
    # Find end of chunk
    end_line = start_line

    try:
        while lines[end_line].strip():
            end_line += 1
    except IndexError:
        end_line = len(lines)

    chunk = lines[start_line:end_line]

    out += handle(chunk, i)
    out += "\n"

    start_line = end_line + 1
    i += len(chunk)

print(out)
