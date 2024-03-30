def load_text(path, by_lines=False):
    with open(path, "r") as fp:
        if by_lines:
            return fp.readlines()
        else:
            return fp.read()
