# Domino AI Training Flow

This repo mocks a sample AI data prepartion and training script using Domino Flows. This flow:

1. Loads two datasets in from different sources
2. Merges the data together
3. Does some data preprocessing
4. Trains a model using the processed data

To run the flow, execute the following command in a workspace using the Domino Standard Environment: 

```
pyflyte run --remote flow.py model_training --data_path_a /mnt/code/data/datasetA.csv --data_path_b /mnt/code/data/datasetB.csv
```

Once you run the command, navigate to `Flows page > Runs pivot > Run name` to monitor the flow execution:

![Execution Link](https://github.com/ddl-jwu/domino-ai-flows/blob/00f667768b18e28985aeda8721ca8e1b8c92a9c4/screenshots/run.png?raw=true)

Clicking on the `View graph` button at the top-right of the runs view will take you to the the Flyte UI where you can see a graph view of the flow:

![Monitor](https://github.com/ddl-jwu/domino-ai-flows/blob/00f667768b18e28985aeda8721ca8e1b8c92a9c4/screenshots/graph.png?raw=true)

# Flow Definition

The flow is defined in the `flow.py` file. The sample flow contains 5 tasks - two for loading in data, one for merging the data together, one for preprocessing the data, and one for model training. Each task ultimately triggers a Domino Job and returns the outputs. We'll go through each of the tasks in detail.

**Data Loading**

The purpose of the data loading tasks is to load the data into flows and make a snapshot of it to capture the data at its current point in time. The code snippet below shows the definition for the two data loading tasks:

```
task1 = run_domino_job_task(
    flyte_task_name='Load Data A',
    command='python /mnt/code/scripts/load-data-A.py',
    hardware_tier_name='Small',
    inputs=[
        Input(name='data_path', type=str, value=data_path_A)
    ],
    output_specs=[
        Output(name='datasetA', type=FlyteFile[TypeVar('csv')])
    ],
    use_project_defaults_for_omitted=True
)

task2 = run_domino_job_task(
    flyte_task_name='Load Data B',
    command='python /mnt/code/scripts/load-data-B.py',
    hardware_tier_name='Small',
    inputs=[
        Input(name='data_path', type=str, value=data_path_B)
    ],
    output_specs=[
        Output(name='datasetB', type=FlyteFile[TypeVar('csv')])
    ],
    use_project_defaults_for_omitted=True
)
```

As you can see, we use the `run_domino_job_task` helper method to create the task with the appropriate parameters. Explaining each parameter in detail:

- `flyte_task_name`: The name for the task.
- `command`: The command that will be used in the Domino Job.
- `environment`: The name of the environment you want to use for the task. If not specified, the default environment for the project will be used. 
- `hardware_tier_name`: The name of the hardware tier you want to use for the task. If not specified, the default hardware tier for the project will be used.
- `inputs`: A list of inputs that the task depends on. Note how the `data_path` inputs are set to the arguments provided through the command line when starting the flow.
- `outputs`: A list of outputs that will be produced by that task. Supported input and output types are documented [here](https://docs.flyte.org/en/latest/user_guide/data_types_and_io/index.html)

Inputs can be accessed within Domino Jobs at `/workflow/inputs/<NAME OF INPUT>`. In a similar fashion, outputs must be written to `/workflow/outputs/<NAME OF OUTPUT>` inside the Domino Job for them to be tracked and returned in the task. See the scripts inside the `script` folder for more details.

**Data Merging**

With both datasets loaded in, the next task is to merge the datasets together into a single one. The code snippet below shows the definition for the data merging task:

```
task3 = run_domino_job_task(
    flyte_task_name='Merge Data',
    command='python /mnt/code/scripts/merge-data.py',
    hardware_tier_name='Small',
    inputs=[
        Input(name='datasetA', type=FlyteFile[TypeVar('csv')], value=task1['datasetA']),
        Input(name='datasetB', type=FlyteFile[TypeVar('csv')], value=task2['datasetB'])
    ],
    output_specs=[
        Output(name='merged_data', type=FlyteFile[TypeVar('csv')])
    ],
    use_project_defaults_for_omitted=True
)
```

As you can see, the same `run_domino_job_task` function is used again. One thing to note is how the output from the data data loading tasks are referenced via calling `task1['datasetA']` / `task2['datasetB']` and it specified as an input to the data merging task.

**Data Preparation**

The next task is to take the merged dataset and perform any necessary data cleaning. The code snippet below shows the definition for the data preprocessing task. 

```
task4 = run_domino_job_task(
    flyte_task_name='Process Data',
    command='python /mnt/code/scripts/process-data.py',
    hardware_tier_name='Small',
    inputs=[
        Input(name='data_path', type=FlyteFile[TypeVar('csv')], value=task3['merged_data'])
    ],
    output_specs=[
        Output(name='processed_data', type=FlyteFile[TypeVar('csv')])
    ],
    use_project_defaults_for_omitted=True
)
```

As you can see, very similar structure as previous tasks.

**Model training**

The final task trains a model using the processed data. The code snippet below shows the definition for the model training task:

```
task5 = run_domino_job_task(
    flyte_task_name='Train Model',
    command='python /mnt/code/scripts/train-model.py',
    hardware_tier_name='Small',
    inputs=[
        Input(name='processed_data', type=FlyteFile[TypeVar('csv')], value=task4['processed_data']),
        Input(name='epochs', type=int, value=10),
        Input(name='batch_size', type=int, value=32)
    ],
    output_specs=[
        Output(name='model', type=FlyteFile[TypeVar('pkl')])
    ],
    use_project_defaults_for_omitted=True
)
```

The output of the last task is then returned as the final output to the flow. 

# Environment Requirements

The project just requires the `Domino Standard Environment` which comes included with all Domino deployments.

# Hardware Requirements

This project works with a the default `small-k8s` tier that comes with all Domino deployments.

# License
This template is licensed under Apache 2.0 and contains the following open source components: 

* Flytekit [Apache 2.0](https://github.com/flyteorg/flytekit/blob/master/LICENSE)