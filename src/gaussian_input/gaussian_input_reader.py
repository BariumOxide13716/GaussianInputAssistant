from gaussian_input import GaussianInput
import sys

if __name__ == "__main__":
    # Example usage
    input_file = sys.argv[1]  # Replace with your Gaussian input file
    gaussian_input = GaussianInput()
    gaussian_input.read_gaussian_input_file(input_file)
    
    # Print the parameters
    #gaussian_input.print_parameters()
    gaussian_input.set_calculation_parameter('method', 'umn15l')
    gaussian_input.set_calculation_parameter('density_fitting', None)
    gaussian_input.save_input_dict_to_json("input_parameters.json")
    gaussian_input.save_gaussian_input_file("output.gjf")
    gaussian_input.load_input_dict_from_json("input_parameters.json")
    gaussian_input.print_parameters()