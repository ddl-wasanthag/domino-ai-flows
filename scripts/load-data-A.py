import os
import shutil
import pandas as pd

# The name of the Flow input, which Domino places into a file blob under /workflow/inputs
input_name = "data_path"
input_location = f"/workflow/inputs/{input_name}"
with open(input_location, "r") as file:
    input_csv = file.read()
# Read input csv to dataframe
df = pd.read_csv(input_csv) 


# Write output
df.to_csv('/workflow/outputs/datasetA.csv', index=False)

