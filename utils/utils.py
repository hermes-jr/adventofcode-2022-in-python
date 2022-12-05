def read_file(filepath):
    data = []
    with open(filepath, 'r') as f:
        for line in f:
            data.append(line.strip())
    return data
