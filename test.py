from flytekitplugins.domino.helpers import BlobDataLocation, download_blobs

"""
This code downloads the data associated with the requested Flows Artifact.
Notes about the keyword args to each BlobDataLocation:
local_dir with None or "" defaults to the configured Flows inputs directory (typically, /workflow/inputs).
local_filename is set to the corresponding ArtifactFile's output variable name from the task execution that produced it.
local_file_extension is set to the ArtifactFile's file format.
These values support the use case of inspecting the Artifact data in an IDE.
You can customize these values as needed by changing the strings in the code below.
For example, to use the data as input to locally-run Flows task code, change the local_filename keyword arg
to the input name the task code expects and remove the local_file_extension keyword arg.
"""
blobs = [
    BlobDataLocation(
        "s3://ddl-sce57693-flyte-data//8dc249a9-a6ce-4d5a-a69e-4f2274b7dc1a/model",
        local_dir="/mnt/code",
        local_filename="model",
        local_file_extension="pkl",
    )
]
download_blobs(blobs)