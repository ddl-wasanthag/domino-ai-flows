from flytekit import workflow
from flytekit.types.file import FlyteFile
from typing import TypeVar, NamedTuple
from flytekitplugins.domino.helpers import Input, Output, run_domino_job_task
from flytekitplugins.domino.task import DominoJobConfig, DominoJobTask, GitRef, EnvironmentRevisionSpecification, EnvironmentRevisionType, DatasetSnapshot
from flytekitplugins.domino.artifact import Artifact, DATA, MODEL, REPORT


# As this is considered a PROD Flow definition, we do not the use_project_defaults_for_omitted parameter
# and explictly set every required parameter in the task defintion to ensure reproducability.
# These are the additional parameters that need to be explicitly set of each task. 

environment_name="Domino Standard Environment Py3.10 R4.5"  # Change to the name of your deployments Domino Standard Environment
environment_revision_id="68a771f590d3cf5ff19c5a17"              # Change to the latest revision ID of your deployments Domino Standard Environment
hardware_tier_name="Small"                                 # Change to the name of one of your Domino's hardware tiers
GitRef_type="commitId"                                     
GitRef_value="c4f273e63e3267d079ebb7c5e5dbcef600521829"   # Change to the commitId of main Git repository 
volume_size_gib=10
dfs_repo_commit_id="52ee5113a38de2dddbd051b42623c23065f28803"   # Change to the latest commit ID of the Artifacts file system in your project


# Set if you want caching on or off for all your tasks.
cache=True

# This calls the Artifact library, to create two named Flow Artifacts that we can label our merged data and model files as. 
DataArtifact = Artifact("Merged Data", DATA)
ModelArtifact = Artifact("Random Forest Model", MODEL)

@workflow
def model_training(data_path_a: str, data_path_b: str): 
    '''
    Sample data preparation and training flow. This flow:
    
        1. Loads two datasets in from different sources
        2. Merges the data together
        3. Does some data preprocessing
        4. Trains a model using the processed data
        5. Output the merged data and model as Flow Artifacts

    To run this flow, execute the following line in the terminal

    pyflyte run --remote  mlops_flow_prod.py model_training --data_path_a /mnt/code/data/datasetA.csv --data_path_b /mnt/code/data/datasetB.csv
    '''

    task1 = run_domino_job_task(
        flyte_task_name='Load Data A',
        command='python /mnt/code/scripts/load-data-A.py',
        inputs=[Input(name='data_path', type=str, value=data_path_a)],
        output_specs=[Output(name='datasetA', type=FlyteFile[TypeVar('csv')])],
        environment_name=environment_name,
        environment_revision_id=environment_revision_id,
        hardware_tier_name="Small",
        dataset_snapshots=[],
        main_git_repo_ref=GitRef(Type=GitRef_type, Value=GitRef_value),
        volume_size_gib=volume_size_gib,
        dfs_repo_commit_id=dfs_repo_commit_id,
        external_data_volumes=[],
        cache=cache,
        cache_version="1.0"
    )

    task2 = run_domino_job_task(
        flyte_task_name='Load Data B',
        command='python /mnt/code/scripts/load-data-B.py',
        inputs=[Input(name='data_path', type=str, value=data_path_b)],
        output_specs=[Output(name='datasetB', type=FlyteFile[TypeVar('csv')])],
        environment_name=environment_name,
        environment_revision_id=environment_revision_id,
        hardware_tier_name="Small",
        dataset_snapshots=[],
        main_git_repo_ref=GitRef(Type=GitRef_type, Value=GitRef_value),
        volume_size_gib=volume_size_gib,
        dfs_repo_commit_id=dfs_repo_commit_id,
        external_data_volumes=[],
        cache=cache,
        cache_version="1.0"
    )

    task3 = run_domino_job_task(
        flyte_task_name='Merge Data',
        command='python /mnt/code/scripts/merge-data.py',
        inputs=[
            Input(name='datasetA', type=FlyteFile[TypeVar('csv')], value=task1['datasetA']),
            Input(name='datasetB', type=FlyteFile[TypeVar('csv')], value=task2['datasetB'])],
        output_specs=[Output(name='merged_data', type=DataArtifact.File(name="merged_data.csv"))],
        environment_name=environment_name,
        environment_revision_id=environment_revision_id,
        hardware_tier_name="Medium",
        dataset_snapshots=[],
        main_git_repo_ref=GitRef(Type=GitRef_type, Value=GitRef_value),
        volume_size_gib=volume_size_gib,
        dfs_repo_commit_id=dfs_repo_commit_id,
        external_data_volumes=[],
        cache=cache,
        cache_version="1.0"
    )

    task4 = run_domino_job_task(
        flyte_task_name='Process Data',
        command='python /mnt/code/scripts/process-data.py',
        inputs=[Input(name='merged_data', type=FlyteFile[TypeVar('csv')], value=task3['merged_data'])],
        output_specs=[Output(name='processed_data', type=FlyteFile[TypeVar('csv')])],
        environment_name=environment_name,
        environment_revision_id=environment_revision_id,
        hardware_tier_name="Medium",
        dataset_snapshots=[],
        main_git_repo_ref=GitRef(Type=GitRef_type, Value=GitRef_value),
        volume_size_gib=volume_size_gib,
        dfs_repo_commit_id=dfs_repo_commit_id,
        external_data_volumes=[],
        cache=cache,
        cache_version="1.0"
    )

    task5 = run_domino_job_task(
        flyte_task_name='Train Model',
        command='python /mnt/code/scripts/train-model.py',
        inputs=[
            Input(name='processed_data', type=FlyteFile[TypeVar('csv')], value=task4['processed_data']),
            Input(name='num_estimators', type=int, value=100)],
        output_specs=[Output(name='model', type=ModelArtifact.File(name="model.pkl"))],
        environment_name=environment_name,
        environment_revision_id=environment_revision_id,
        hardware_tier_name="Large",
        dataset_snapshots=[],
        main_git_repo_ref=GitRef(Type=GitRef_type, Value=GitRef_value),
        volume_size_gib=volume_size_gib,
        dfs_repo_commit_id=dfs_repo_commit_id,
        external_data_volumes=[],
        cache=cache,
        cache_version="1.0"
    )

    return 
