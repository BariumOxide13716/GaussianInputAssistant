from gaussian_input import GaussianInput
import sys

if __name__ == "__main__":
    # Example usage
    input_file = sys.argv[1]  # Replace with your Gaussian input file
    gaussian_input = GaussianInput()
    gaussian_input.read_gaussian_input_file(input_file)
    
    # Print the parameters
    gaussian_input.print_parameters()
    
    