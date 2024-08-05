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
    input_location = f"/workflow/inputs/{name}"
    if is_file:
        return input_location # Directly return the blob for file inputs
    else:
        with open(input_location, "r") as file: # Read the contents of the blob for other inputs
            contents = file.read()
            return contents
