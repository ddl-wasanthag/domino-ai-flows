import os
import pandas as pd
from argparse import ArgumentParser
from flows import read_flow_input

# Argument parser for allowing user to toggle between local and flow execution
parser = ArgumentParser(description='Data preparation script.')
parser.add_argument('--local', action='store_true', help='Set this flag to indicate local testing (instead of triggering via flows)')
args = parser.parse_args()

# Set variables based on whether it is executed locally or triggered by a flow
data_path = '/mnt/code/data/data.csv'
output_location = '/mnt/code/outputs'
if args.local == False:
    data_path = read_flow_input(name='data_path')
    output_location = '/workflow/outputs'

# Read data input
df = pd.read_csv(data_path) 

# Process data
print(df)
print('Preparing the data')
df = df.drop('a', axis=1)
print(df)

# Write output. In flows, outputs must be written to /workflow/outputs/<NAME OF OUTPUT>.
output_name = 'processed_data'
df.to_csv(f'{output_location}/{output_name}')
