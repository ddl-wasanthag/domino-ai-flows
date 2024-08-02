'''
Helper function to read inputs when inside a job triggered by Domino Flows.

All inputs are stored in a blob at /workflow/inputs/<NAME OF INPUT>.
For file input types, the blob is the file input itself.
For all other supported input types (str, int, bool, etc), they are stored as conents inside the blob.

Args:
    name (str): The name of the input
    is_file (bool): Whether the input type is a file or not.

Returns:
    Any: Either the input file or value
'''
def read_flow_input(name: str, is_file: bool=False):
    # input_location = f"/workflow/inputs/{name}"
    # if is_file:
    #     return input_location # Direction return the blob for file inputs
    # else:
    #     with open(input_location, "r") as file: # Read the contents of the blob for other inputs
    #         contents = file.read()
    #         return contents
    return '/mnt/code/data/data.csv'


'''
Helper function to retrieve the path where outputs should be written too.

For jobs triggered by flows, outputs must be written to /workflow/outputs/<NAME OF INPUT>.
For local testing, we will write the outputs to a temporary /mnt/code/outputs folder

Args:
    name (str): The name of the input
    is_file (bool): Whether the input type is a file or not.

Returns:
    str: The root path of the output folder
'''
def get_output_location(local: bool=False):
    output_location = ''
    if local:
        output_location = '/mnt/code/outputs'
        if not os.path.exists(output_location):
            os.makedirs(output_location)
    else:
        output_location = '/workflow/outputs'
    return output_location