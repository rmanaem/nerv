## Directory structure

In order to generate and populate plots, the `start` function requires access to the directory housing subdirectories, which in turn contain JSON files to be visualized.

Here is an example of the directory structure:

```
.
├── app.py
├── internal
│      ├── experiment1
|      |    └── compass-nd.json
|      |
|      ├── experiment2
|      |    ├── prevent-AD.json
|      |    └── compass-nd.json
|      |
│      └── experiment3
|           └── prevent-AD.json
```

## Data file structure

NeRV processes JSON files that adhere to a specific format.

!!! info "info"
For a more comprehensive example, please refer to this [link](https://raw.githubusercontent.com/rmanaem/nerv/master/tests/data/prevent-AD.json).

Below is a portion of the file that follows this specific format as an example of its structure:

```json
{
  "sub-1004359_ses-PREBL00_run-001_T1w.nii.gz": {
    "FSL": {
      "FSL_First": {
        "inputID": 3541682,
        "toolConfigID": 721,
        "taskID": 1874664,
        "status": "Completed",
        "outputID": 3663588,
        "isUsed": true
      },
      "Subfolder_File_Extractor_FSL": {
        "inputID": 3663588,
        "toolConfigID": 2094,
        "taskID": 1874748,
        "status": "Completed",
        "outputID": 3663636,
        "isUsed": true
      },
      "FSL_Stats": {
        "inputID": 3663636,
        "toolConfigID": 1698,
        "taskID": 1874769,
        "status": "Completed",
        "outputID": 3663651,
        "isUsed": true
      },
      "Result": {
        "result": "1715",
        "isUsed": true
      }
    },
    "FreeSurfer": {
      "FreeSurfer_Recon_all": {
        "inputID": 3541682,
        "toolConfigID": 583,
        "taskID": 1874685,
        "status": "Completed",
        "outputID": 3663675,
        "isUsed": true
      },
      "Subfolder_File_Extractor_FreeSurfer_1": {
        "inputID": 3663675,
        "toolConfigID": 2094,
        "taskID": 1874793,
        "status": "Completed",
        "outputID": 3663702,
        "isUsed": true
      },
      "Subfolder_File_Extractor_FreeSurfer_2": {
        "inputID": 3663702,
        "toolConfigID": 2094,
        "taskID": 1881855,
        "status": "Completed",
        "outputID": 3673260,
        "isUsed": true
      },
      "Result": {
        "result": "3900.6",
        "isUsed": true
      }
    }
  },
}
```
