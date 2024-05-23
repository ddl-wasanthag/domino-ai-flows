# Domino AI Training Flow

This repo mocks a sample AI training script using Domino Flows. 

The input to this flow is the path to a sample dataset that is provided in this repository.

To run the flow, execute the following command in a workspace using the Domino Standard Environment: 

```
pyflyte run --remote workflow.py training_workflow --data_path /mnt/code/data/data.csv
```

Once you run the command, a direct link to the Flyte console should be returned:

![Execution Link](https://github.com/dominodatalab/domino-ai-flows/blob/8256e3ce6aaffe4e37d962b996dd167a37020f57/screenshots/execution-link.png?raw=true)

Upon clicking on the link, you should be navigated to a page where you can monitor the execution:

![Monitor](https://github.com/dominodatalab/domino-ai-flows/blob/8256e3ce6aaffe4e37d962b996dd167a37020f57/screenshots/monitor.png?raw=true)

# Flow Definition

The flow is defined in the `workflow.py` file and it leverages some helper methods that are located in `utils/flyte.py`. It is reccommended that you do not modify the contents within the helper methods, but they are there for you if you want the full flexibility.

The sample flow contains two tasks - one for data preparation and one for model training. Each task ultimately triggers a Domino Job and returns the outputs. We'll go through each of the steps in detail.

**Data preparation**

The code snippet below shows the definition for the data preparation task:

```
data_prep_results = DominoTask(
    name="Prepare data",
    command="python /mnt/code/scripts/prep-data.py",
    environment="Domino Standard Environment Py3.9 R4.3",
    hardware_tier="Small",
    inputs=[
        Input(name="data_path", type=str, value=data_path)
    ],
    outputs=[
        Output(name="processed_data", type=FlyteFile)
    ]
)
```

As you can see, we use the `DominoTask` function to create the task with the appropriate parameters. Explaining each parameter in detail:

- `name`: The name for the task.
- `command`: The command that will be used in the Domino Job.
- `environment`: The name of the environment you want to use for the task. If not specified, the default environment for the project will be used.
- `hardware_tier`: The name of the hardware tier you want to use for the task. If not specified, the default hardware tier for the project will be used.
- `inputs`: A list of inputs that the task depends on. Note how the `data_path` input is set to the argument provided through the command line when starting the flow.
- `outputs`: A list of outputs that will be produced by that task. Supported input and output types are documented [here](https://docs.flyte.org/en/latest/user_guide/data_types_and_io/index.html)

Inputs can be accessed within Domino Jobs at `/workflow/inputs/<NAME OF INPUT>`. In a similar fashion, outputs must be written to `/workflow/outputs/<NAME OF OUTPUT>` inside the Domino Job for them to be tracked and returned in the task. See the scripts inside the `script` folder for more details.

**Model training**

The code snippet below shows the definition for the model training task:

```
training_results = DominoTask(
    name="Train model",
    command="python /mnt/code/scripts/train-model.py",
    environment="Domino Standard Environment Py3.9 R4.3",
    hardware_tier="Small",
    inputs=[
        Input(name="processed_data", type=FlyteFile, value=data_prep_results['processed_data']),
        Input(name="epochs", type=int, value=10),
        Input(name="batch_size", type=int, value=32)
    ],
    outputs=[
        Output(name="model", type=FlyteFile)
    ]
)
```

As you can see, the same `DominoTask` function is used. A few things to note about the snippet above:
- Different command, environments, and hardware tiers can be used in each task. Even though we are using the same ones in this example, it is not a requirement.
- The output from the data prep tasks is referenced via `data_prep_results['processed_data']` and it specified as an input to the training task.

# Environment Requirements

The project just requires the `Domino Standard Environment` which comes included with all Domino deployments.

# Hardware Requirements

This project works with a the default `small-k8s` tier that comes with all Domino deployments.
