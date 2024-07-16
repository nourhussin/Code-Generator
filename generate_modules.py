
def parse_parameters(params):
    parameters = {}
    for param in params:
        if '=' in param:
            key, value = param.strip().split('=')
            parameters[key.strip()] = value.strip()
    return parameters

def parse_io_section(io_section):
    io_lines = io_section.strip().split('\n')
    io_dict = {}
    for line in io_lines:
        parts = line.split()
        if len(parts) == 3:
            io_dict[parts[0]] = {'width': parts[1], 'type': parts[2]}
    return io_dict

def parse_design_info(design_info):
    design_type, clock_name, clock_edge, reset_name, reset_type, reset_edge = design_info.split()
    return {
        'design_type': design_type,
        'clock_name': clock_name,
        'clock_edge': clock_edge,
        'reset_name': reset_name,
        'reset_type': reset_type,
        'reset_edge': reset_edge
    }

def parse_module(module_data):
    module_info = {}
    lines = module_data.strip().split('\n')
    
    # Parse module name
    module_name_line = lines[0].split(':')
    if len(module_name_line) == 2:
        module_info['module_name'] = module_name_line[1].strip()
    
    # Parse parameters
    try:
        param_start = lines.index('parameters:')
        param_end = lines.index('inputs:')
        params = lines[param_start + 1:param_end]
        module_info['parameters'] = parse_parameters(params)
    except ValueError:
        module_info['parameters'] = {}
    
    # Parse inputs
    try:
        input_start = lines.index('inputs:')
        input_end = lines.index('outputs:')
        inputs = lines[input_start + 1:input_end]
        module_info['inputs'] = parse_io_section('\n'.join(inputs))
    except ValueError:
        module_info['inputs'] = {}
    
    # Parse outputs
    try:
        output_start = lines.index('outputs:')
        output_end = lines.index('design_info:')
        outputs = lines[output_start + 1:output_end]
        module_info['outputs'] = parse_io_section('\n'.join(outputs))
    except ValueError:
        module_info['outputs'] = {}
    
    # Parse design info
    try:
        design_info_start = lines.index('design_info:')
        design_info = lines[design_info_start + 1].strip()
        module_info['design_info'] = parse_design_info(design_info)
    except (ValueError, IndexError):
        module_info['design_info'] = {}
    
    return module_info

def read_modules_from_file(file_path):
    with open(file_path, 'r') as file:
        data = file.read().strip().split('----------------------------------------------')
    
    modules = []
    for module_data in data:
        modules.append(parse_module(module_data))
    
    return modules

# Example usage
file_path = 'module_info.txt' 
modules = read_modules_from_file(file_path)

for module in modules:
    module_file = open(module['module_name']+".v","w")
    module_tb   = open(module['module_name']+"_tb.v","w")
    module_file.write("module %s " %module['module_name'])

    if(len(module['parameters']) > 0):
        module_file.write("#(parameter ")
        for index, parameter in enumerate(module['parameters']):
            if(index == len(module['parameters']) - 1):
                module_file.write("%s = %s" %(parameter,module['parameters'][parameter]))
            else:
                module_file.write("%s = %s, " %(parameter,module['parameters'][parameter]))


        module_file.write(")( \n//--------------------Input Ports---------------------\n")
    for input in module['inputs']:
        if(module['inputs'][input]['width']=="1"):
            module_file.write("input wire %s,\n" %input)
        else:
            module_file.write("input wire [%s-1 : 0] %s,\n" %(module['inputs'][input]['width'],input))


    module_file.write("//--------------------Output Ports---------------------\n")
    for index, output in enumerate(module['outputs']):
        if(module['outputs'][output]['width']=="1"):
            if(index == len(module['outputs']) - 1):
                module_file.write("output %s %s\n" %(module['outputs'][output]['type'],output))
            else:
                module_file.write("output %s %s,\n" %(module['outputs'][output]['type'],output))
        else:
            if(index == len(module['outputs']) - 1):
                module_file.write("output %s [%s-1 : 0] %s\n" %(module['outputs'][output]['type'],module['outputs'][output]['width'],output))
            else:
                module_file.write("output %s [%s-1 : 0] %s,\n" %(module['outputs'][output]['type'],module['outputs'][output]['width'],output))


    module_file.write(");\n//--------------------Internal Variables---------------------\n\n//--------------------Design Implementation---------------------\n")
    if(module['design_info']['design_type'] == "seq"):
        if(module['design_info']['clock_edge'] == "pos"):
            module_file.write("always @(posedge %s" %module['design_info']['clock_name'])
        elif(module['design_info']['clock_edge'] == "neg"):
            module_file.write("always @(negedge %s" %module['design_info']['clock_name'])

        if(module['design_info']['reset_type'] == "async"):
            if(module['design_info']['reset_edge'] == "pos"):
                module_file.write(", posedge %s)\nbegin\n" %module['design_info']['reset_name'])
            elif(module['design_info']['reset_edge'] == "neg"):
                module_file.write(", negedge %s)\nbegin\n" %module['design_info']['reset_name'])
        else:
            module_file.write(")\nbegin\n")

        if(module['design_info']['reset_edge'] == "pos"):
            module_file.write("\tif (%s == 1)\n\tbegin\n\t//--------------------Reset Conditions---------------------\n\n\tend\n\n" %module['design_info']['reset_name'])
            module_file.write("\telse\n\tbegin\n\t//--------------------Your Design---------------------\n\n\tend\nend\n")
        elif(module['design_info']['reset_edge'] == "neg"):
            module_file.write("\tif (%s == 0)\n\tbegin\n\t//--------------------Reset Conditions---------------------\n\n\tend\n\n" %module['design_info']['reset_name'])
            module_file.write("\telse\n\tbegin\n\t//--------------------Your Design---------------------\n\n\tend\nend\n")
    module_file.write("\nendmodule")


    module_tb.write("`include \"%s.v\" \nmodule %s_tb;\n"%(module['module_name'],module['module_name']))
    if(len(module['parameters']) > 0):
        module_tb.write("//--------------------Parameters---------------------\n")
        for parameter in module['parameters']:
            module_tb.write("localparam %s = %s;\n" %(parameter,module['parameters'][parameter]))
    
    module_tb.write("//--------------------Inputs---------------------\n")
    for input in module['inputs']:
        if(module['inputs'][input]['width']=="1"):
            module_tb.write("reg %s_tb;\n" %input)
        else:
            module_tb.write("reg [%s-1 : 0] %s_tb;\n" %(module['inputs'][input]['width'],input))

    module_tb.write("//--------------------Outputs---------------------\n")
    for output in module['outputs']:
        if(module['outputs'][output]['width']=="1"):
            module_tb.write("wire %s_tb;\n" %output)
        else:
            module_tb.write("wire [%s-1 : 0] %s_tb;\n" %(module['outputs'][output]['width'],output))

    module_tb.write("//--------------------Instantiation---------------------\n%s #(" %module['module_name'])
    for index, parameter in enumerate(module['parameters']):
        if(index == len(module['parameters']) - 1):
            module_tb.write(".%s(%s)" %(parameter, parameter))
        else:
            module_tb.write(".%s(%s)," %(parameter, parameter))
    module_tb.write(") DUT(\n")
    for input in module['inputs']:
        module_tb.write("\t.%s(%s_tb),\n" %(input, input))
    for index, output in enumerate(module['outputs']):
        if(index == len(module['outputs']) - 1):
            module_tb.write("\t.%s(%s_tb)\n" %(output, output))
        else:
            module_tb.write("\t.%s(%s_tb),\n" %(output, output))
    module_tb.write("\t);\n")

    module_tb.write("//--------------------Clock Generation---------------------\n")
    module_tb.write("localparam T = 10;\nalways#(T/2) %s_tb <= ~%s_tb;\n" %(module['design_info']['clock_name'],module['design_info']['clock_name']))

    module_tb.write("//--------------------Start Testing---------------------\ninitial begin\n\t//Reset Inputs:\n")
    module_tb.write("\t%s_tb = 0;\n" %module['design_info']['clock_name'])
    if(module['design_info']['reset_edge'] == "pos"):
        module_tb.write("\t%s_tb = 1;\n" %module['design_info']['reset_name'])
    elif(module['design_info']['reset_edge'] == "neg"):
        module_tb.write("\t%s_tb = 0;\n" %module['design_info']['reset_name'])
    module_tb.write("\n\t//Apply Stimulus:\n\n\tend\nendmodule")
    
    module_file.close()
    module_tb.close()