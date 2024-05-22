from utils.flyte import DominoTask, Input, Output
from flytekit import workflow
from flytekit.types.file import FlyteFile
from flytekit.types.directory import FlyteDirectory
from typing import TypeVar, NamedTuple

final_outputs = NamedTuple("final_outputs", model=FlyteFile)

@workflow
def training_workflow(data_path: str) -> final_outputs: 
    """
    Sample data preparation and training workflow

    This workflow accepts a path to a CSV for some initial input and simulates
    the processing of the data and usage of the processed data in a training job.

    To run this workflowp, execute the following line in the terminal

    pyflyte run --remote workflow.py training_workflow --data_path /mnt/code/data/data.csv

    :param data_path: Path of the CSV file data
    :return: The training results as a model
    """

    data_prep_results = DominoTask(
        name="Prepare data",
        command="python /mnt/code/scripts/prep-data.py",
        environment="Domino Standard Environment Py3.9 R4.3",
        hardware_tier="Small",
        inputs=[
            Input(name="data_path", type=str, value=data_path)
        ],
        outputs=[
            Output(name="processed_data", type=FlyteFile[TypeVar("csv")])
        ]
    )

    training_results = DominoTask(
        name="Train model",
        command="python /mnt/code/scripts/train-model.py",
        environment="Domino Standard Environment Py3.9 R4.3",
        hardware_tier="Small",
        inputs=[
            Input(name="processed_data", type=FlyteFile[TypeVar("csv")], value=data_prep_results['processed_data']),
            Input(name="epochs", type=int, value=10),
            Input(name="batch_size", type=int, value=32)
        ],
        outputs=[
            Output(name="model", type=FlyteFile)
        ]
    )

    return final_outputs(model=training_results['model'])
