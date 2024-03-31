import subprocess

def run_bash_command(command):
    try:
        # Execute the command in the terminal
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        # Handle errors if the command fails
        print(f"Error executing command: {e}")
        return False
    return True

if __name__ == "__main__":
    # Replace the command string with the bash command you want to run
    command_to_run = "ollama cp deepseek-coder:33b-instruct-q5_K_M gpt-4"
    success1 = run_bash_command(command_to_run)

    # Run second command
    command_to_run = "ollama cp deepseek-coder:33b-instruct-q5_K_M gpt-3.5-turbo"
    success2 = run_bash_command(command_to_run)
    
    if success1 and success2:
        print("Command executed successfully.")
    else:
        print("Command execution failed.")
