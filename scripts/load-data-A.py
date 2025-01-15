import os
import shutil
import pandas as pd

# The name of the Flow input, which Domino places into a file blob under /workflow/inputs
task_input_name = "data_path"
input_file = f"/workflow/inputs/{task_input_name}"

# Read input csv to dataframe
df = pd.read_csv(input_file) 


# Write output
df.to_csv(workflow/outputs/datasetA, index=False)