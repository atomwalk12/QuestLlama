def writeToFile(lines, filename='prompts.txt'):
    """
    Write lines to a file. Used to debug LM Studio prompts.
    """
    with open(filename, 'w') as f:
        for line in lines:
            f.write(f"type: {line.type}\n")
            f.write(f"content: {line.content}\n")
