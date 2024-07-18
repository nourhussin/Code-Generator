# Verilog Module and Testbench Generator

This Python script generates templates for Verilog modules and their corresponding testbenches. It reads data from a text file with a specific format and produces the necessary Verilog files.

## Features

- Generates Verilog module templates
- Generates corresponding testbench templates
- Parses input parameters, inputs, outputs, and design information from a text file

## Input File Format

- Module Name: Defined with module name : <name>
- Parameters: Listed under the parameters: section with <name> = <value>
- Inputs: Listed under the inputs: section with <name> <width> <type>
- Outputs: Listed under the outputs: section with <name> <width> <type>
- Design Info: Listed under the design_info: section with <type> <clock> <clock_edge> <reset> <reset_type> <reset_edge>

## Important Notes

- *Files will not be generated if there is an error in the input data*
  
### In the design info section:
- The first option is seq or comb (sequential or combinational logic).
- The third and last options are pos or neg (positive or negative edge).
- The fifth option is async or sync (asynchronous or synchronous reset).
