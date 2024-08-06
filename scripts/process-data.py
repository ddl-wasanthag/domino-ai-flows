import os
import pandas as pd
from argparse import ArgumentParser
from flows import read_flow_input

# Argument parser for allowing user to toggle between local and flow execution
parser = ArgumentParser(description='Data processing script.')
parser.add_argument('--local', action='store_true', help='Set this flag to indicate local testing (instead of triggering via flows)')
parser.add_argument('--data_path', type=str, default='/mnt/code/outputs/merged_data', help='Path to the input data. Only used during local testing. Flow triggered jobs will use task inputs.')
parser.add_argument('--output_location', type=str, default='/mnt/code/outputs', help='Path to output results. Only used during local testing. Flow triggered jobs will use task output directory.')
args = parser.parse_args()

# Set variables based on whether it is executed locally or triggered by a flow
data_path = args.data_path
output_location = args.output_location
if args.local == False:
    data_path = read_flow_input(name='data_path', is_file=True)
    output_location = '/workflow/outputs'
os.makedirs(output_location, exist_ok=True)

# Read data input
df = pd.read_csv(data_path) 

# Process data
print(df)
print('Processing the data ...')
df = df.drop('RandomColumn', axis=1)
print(df)

# Write output. In flows, outputs must be written to /workflow/outputs/<NAME OF OUTPUT>.
output_name = 'processed_data'
df.to_csv(f'{output_location}/{output_name}', index=False)

