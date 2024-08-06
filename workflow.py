from flytekitplugins.domino.helpers import Input, Output, run_domino_job_task
from flytekitplugins.domino.task import DominoJobConfig, DominoJobTask
from flytekit import workflow
from flytekit.types.file import FlyteFile
from flytekit.types.directory import FlyteDirectory
from typing import TypeVar, NamedTuple

final_outputs = NamedTuple("final_outputs", model=FlyteFile[TypeVar("pkl")])

@workflow
def training_workflow(data_path_A: str='/mnt/code/data/datasetA.csv', data_path_B: str='/mnt/code/data/datasetB.csv') -> final_outputs: 
    """
    Sample data preparation and training workflow

    This workflow accepts a path to a CSV for some initial input and simulates
    the processing of the data and usage of the processed data in a training job.

    To run this workflowp, execute the following line in the terminal

    pyflyte run --remote workflow.py training_workflow --data_path /mnt/code/data/data.csv

    :param data_path: Path of the CSV file data
    :return: The training results as a model
    """

    task1 = run_domino_job_task(
        flyte_task_name="Load Dataset A",
        command="python /mnt/code/scripts/load-dataset-A.py",
        hardware_tier_name="Small",
        inputs=[
            Input(name="data_path", type=str, value=data_path_A)
        ],
        output_specs=[
            Output(name="datasetA", type=FlyteFile[TypeVar("csv")])
        ],
        use_project_defaults_for_omitted=True
    )

    task2 = run_domino_job_task(
        flyte_task_name="Load Dataset B",
        command="python /mnt/code/scripts/load-dataset-B.py",
        hardware_tier_name="Small",
        inputs=[
            Input(name="data_path", type=str, value=data_path_B)
        ],
        output_specs=[
            Output(name="datasetB", type=FlyteFile[TypeVar("csv")])
        ],
        use_project_defaults_for_omitted=True
    )

    task3 = run_domino_job_task(
        flyte_task_name="Merge Datasets",
        command="python /mnt/code/scripts/merge-data.py",
        hardware_tier_name="Small",
        inputs=[
            Input(name="datasetA", type=FlyteFile[TypeVar("csv")], value=task1['datasetA']),
            Input(name="datasetB", type=FlyteFile[TypeVar("csv")], value=task2['datasetB'])
        ],
        output_specs=[
            Output(name="processed_data", type=FlyteFile[TypeVar("csv")])
        ],
        use_project_defaults_for_omitted=True
    )

    task4 = run_domino_job_task(
        flyte_task_name="Train Model",
        command="python /mnt/code/scripts/train-model.py",
        hardware_tier_name="Small",
        inputs=[
            Input(name="processed_data", type=FlyteFile[TypeVar("csv")], value=task3['processed_data']),
            Input(name="epochs", type=int, value=10),
            Input(name="batch_size", type=int, value=32)
        ],
        output_specs=[
            Output(name="model", type=FlyteFile[TypeVar("pkl")])
        ],
        use_project_defaults_for_omitted=True
    )

    return final_outputs(model=task4['model'])
