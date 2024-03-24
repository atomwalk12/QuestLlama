import os
import subprocess

# Set environment variables
os.environ['CMAKE_ARGS'] = "-DLLAMA_CUBLAS=on"
os.environ['FORCE_CMAKE'] = "1"
os.environ['GGML_CUDA_NO_PINNED'] = "1" # Required for CUDA support

# Install requirements
# By default, we install the llama-cpp-python package with CUDA support.
subprocess.run(["pip", "install", "--upgrade", "--force-reinstall", "llama-cpp-python", "--no-cache-dir"], check=True)

# Construct the path to the requirements.txt file in the parent directory
script_dir = os.path.dirname(os.path.realpath(__file__))
requirements_voyager = os.path.join(script_dir, '..', 'requirements.txt')
requirements_questllama = os.path.join(script_dir, 'requirements.txt')

# You can also install other requirements from a requirements.txt file if needed
subprocess.run(["pip", "install", "-r", requirements_voyager], check=True)
subprocess.run(["pip", "install", "-r", requirements_questllama], check=True)
