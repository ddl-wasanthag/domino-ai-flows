import os
import pandas as pd
from time import sleep
from argparse import ArgumentParser
from flows import read_flow_input, get_output_location

parser = ArgumentParser(description='Model training script. Default values assume the script is running in a flow.')
parser.add_argument('--local', action='store_true', help='Set this flag to indicate local testing (instead of triggering via flows)')
parser.add_argument('--processed_data', type=str, default=read_flow_input(name='processed_data', is_file=True), help='The path of the processed input dataset.')
args = parser.parse_args()

# Read input
df = pd.read_csv(args.processed_data) 

# Pretend like something is happening here to train the model
print("Training the model")
sleep(20)

# Write output
output_location = get_output_location(name='model', local=args.local)
os.mkdir(output_location) 