import os
import pandas as pd
from argparse import ArgumentParser
from flows import read_flow_input

# Argument parser for allowing user to toggle between local and flow execution
parser = ArgumentParser(description='Model training script.')
parser.add_argument('--local', action='store_true', help='Set this flag to indicate local testing (instead of triggering via flows)')
parser.add_argument('--datasetA', type=str, default='/mnt/code/outputs/datasetA', help='Path to the input data. Only used during local testing. Flow triggered jobs will use task inputs.')
parser.add_argument('--datasetB', type=str, default='/mnt/code/outputs/datasetB', help='Path to the input data. Only used during local testing. Flow triggered jobs will use task inputs.')
parser.add_argument('--output_location', type=str, default='/mnt/code/outputs', help='Path to output results. Only used during local testing. Flow triggered jobs will use task output directory.')
args = parser.parse_args()

# Set variables based on whether it is executed locally or triggered by a flow
datasetA = args.datasetA
datasetB = args.datasetB
output_location = args.output_location
if args.local == False:
    datasetA = read_flow_input(name='datasetA', is_file=True)
    datasetB = read_flow_input(name='datasetB', is_file=True)
    output_location = '/workflow/outputs'
os.makedirs(output_location, exist_ok=True)

# Read data input
a = pd.read_csv(datasetA, index_col='Id') 
b = pd.read_csv(datasetB, index_col='Id') 

# Merge the data together
print('Merging data...')
merged = pd.concat([a, a], axis=0).reset_index(drop=True)
print(merged)

# Write output. In flows, outputs must be written to /workflow/outputs/<NAME OF OUTPUT>.
output_name = 'merged_data'
merged.to_csv(f'{output_location}/{output_name}', index_label='Id')
