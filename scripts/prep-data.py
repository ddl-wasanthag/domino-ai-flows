import os
import pandas as pd
from argparse import ArgumentParser
from flows import read_flow_input, get_output_location

parser = ArgumentParser(description='Data preparation script')
parser.add_argument('--local', action='store_true', help='Set this flag to indicate local testing (instead of triggering via flows)')
parser.add_argument('--data_path', type=str, default=read_flow_input(name='data_path'), help='The path of the input dataset.')
args = parser.parse_args()

# Read input
df = pd.read_csv(data_path) 

# Process data
print(df)
print("Preparing the data")
df = df.drop('a', axis=1)
print(df)

# Write output
output_name = "processed_data"
output_location = get_output_location(name=processed_data, local=args.local)
df.to_csv(f'{output_location}/{output_name}')
