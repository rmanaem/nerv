# Welcome to NeRV

**Ne**uroimaging **R**results **V**isualization is a Python-based web interface designed for visualizing neuroimaging results obtained from continuous testing of neuroimaging data across software pipelines. It utilizes [Plotly Dash](https://dash.plotly.com/), [Dash Bootstrap Components](https://dash-bootstrap-components.opensource.faculty.ai/), and [pandas](https://pandas.pydata.org/) to provide an interactive and informative visualization experience.\
NeRV is released as a PyPI package, available [here](https://pypi.org/project/nerv/). Explore the [demo](https://nerv-demo.onrender.com/) and experience NeRV in action firsthand. For more information, refer to the [documentation](https://rmanaem.github.io/nerv/).

## Getting Started

### Installation

Install NeRV using pip:

```bash
pip install nerv
```

### Example usage

In order for NeRV to generate and populate plots the underlying app requires access to the directory that houses subdirectories, which in turn contain the JSON files to be visualized. The path to directory can be passed to the app as input to the `start` function.

```python
from nerv import app

app.start("path-to-data-directory")
```

After executing the file containing the above code snippet, a local server is started at port 8050 (by default). You can access the running NeRV application using a browser through the URL `localhost:8050`.

Once there you you will find your experiment directories presented as cards. By selecting each card, you can visualize the plots corresponding to the data in the respective experiment directory.

![ui](https://github.com/rmanaem/nerv/blob/master/img/ui.png?raw=true)
