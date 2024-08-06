import os
from argparse import Namespace
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
def read_input(name: str, args: Namespace, is_file: bool=False):
    if os.environ.get('DOMINO_IS_WORKFLOW_JOB') == 'false':
        return getattr(args, name) # Local execution, return the arguments in command line
    else:
        input_location = f'/workflow/inputs/{name}'
        if is_file:
            return input_location # Directly return the blob for file inputs
        else:
            with open(input_location, 'r') as file: # Read the contents of the blob for other inputs
                contents = file.read()
                return contents

def get_output_location(name: str, args: Namespace):
    if os.environ.get('DOMINO_IS_WORKFLOW_JOB') == 'false': # Local execution, return a default output folder
        output_folder = args.output_folder
        os.makedirs(output_folder, exist_ok=True)
        return f'{output_folder}/{name}'
    else:
        output_folder = '/workflow/outputs' # Flow execution, return the outputs folder
        return f'{output_folder}/{name}'
