# Neuroimaging Results Visualization

Neuroimaging Results Visualization (NeRV) is an interface developed using [Plotly Dash](https://dash.plotly.com/) for visualization of neuroimaging results obtained from continuous testing of neuroimaging data across software pipelines.

## How to use

### Install the package using pip

```cmd
pip install nerv
```

In order for NeRV to generate and populate plots the underlying app requires access to the directory containing the datasets. The path to directory can be passed to the app module as input to the start function.

### Example of how to use

```python
from nerv import app

app.start("path-to-data-directory")
```

Once the file containing the above snipet is executed, a local server (at port 8050 by default) is launched. The server and the app can be accessed by browser through `localhost:8050` url.
