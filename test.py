import os
import pandas as pd
from argparse import ArgumentParser

# Argument parser for allowing user to toggle between local and flow execution
parser = ArgumentParser(description='Data preparation script.')
parser.add_argument('--local', action='store_true', help='Set this flag to indicate local testing (instead of triggering via flows)')
parser.add_argument('--data_path', type=str, default='/mnt/code/data/datasetA.csv', help='Path to the input data. Only used during local testing. Flow triggered jobs will use task inputs.')
parser.add_argument('--output_location', type=str, default='/mnt/code/outputs', help='Path to output results. Only used during local testing. Flow triggered jobs will use task output directory.')
args = parser.parse_args()

# Set variables based on whether it is executed locally or triggered by a flow
variable = 'data_path'
data_path = getattr(args, variable)
print(data_path)