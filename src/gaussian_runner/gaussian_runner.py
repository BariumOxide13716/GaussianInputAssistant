"""
This file is an interface for running gaussian with python.
It assumes that the path to gaussian is added to the system path.
"""

import subprocess

def run_command(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result

def run_gaussian(input_file, output_file, gaussian_executable="g16"):
    """
    Runs Gaussian with the specified input file and writes the output to the output file.
    
    Args:
        input_file (str): The path to the Gaussian input file.
        output_file (str): The path where the output will be written.
            
    Returns:
        subprocess.CompletedProcess: The result of the command execution.
    """
    command = f"{gaussian_executable} < {input_file} > {output_file}"
    return run_command(command)

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 3:
        print("Usage: python gaussian_runner.py <input_file> <output_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    result = run_gaussian(input_file, output_file)
    
    if result.returncode == 0:
        print(f"Gaussian run completed successfully. Output written to {output_file}.")
    else:
        print(f"Error running Gaussian: {result.stderr}")
        sys.exit(result.returncode)