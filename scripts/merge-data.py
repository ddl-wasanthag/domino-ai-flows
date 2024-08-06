import os
import pickle
import shutil
import pandas as pd
from time import sleep
from argparse import ArgumentParser
from flows import read_flow_input
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# Argument parser for allowing user to toggle between local and flow execution
parser = ArgumentParser(description='Model training script.')
parser.add_argument('--local', action='store_true', help='Set this flag to indicate local testing (instead of triggering via flows)')
parser.add_argument('--source_data_A', type=str, default='/mnt/code/outputs/data_A', help='Path to the input data. Only used during local testing. Flow triggered jobs will use task inputs.')
parser.add_argument('--source_data_B', type=str, default='/mnt/code/outputs/data_B', help='Path to the input data. Only used during local testing. Flow triggered jobs will use task inputs.')
parser.add_argument('--output_location', type=str, default='/mnt/code/outputs', help='Path to output results. Only used during local testing. Flow triggered jobs will use task output directory.')
args = parser.parse_args()

# Set variables based on whether it is executed locally or triggered by a flow
source_data_A = args.source_data_A
source_data_B = args.source_data_B
output_location = args.output_location
if args.local == False:
    source_data_A = read_flow_input(name='source_data_A', is_file=True)
    source_data_B = read_flow_input(name='source_data_B', is_file=True)
    output_location = '/workflow/outputs'
os.makedirs(output_location, exist_ok=True)

# Read data input
a = pd.read_csv(source_data_A, index_col='Id') 
b = pd.read_csv(source_data_B, index_col='Id') 

# Merge the data together
print('Merging data...')
merged = pd.concat([a, a], axis=0).reset_index(drop=True)
print(merged)

# Write output. In flows, outputs must be written to /workflow/outputs/<NAME OF OUTPUT>.
output_name = 'processed_data'
merged.to_csv(f'{output_location}/{output_name}', index_label='Id')
