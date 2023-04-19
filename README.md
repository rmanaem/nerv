<div align="center">

# Neuroimaging Results Visualization

<div>
    <a href="https://github.com/rmanaem/nerv/actions/workflows/test.yaml">
        <img src="https://img.shields.io/github/actions/workflow/status/neurobagel/api/test.yaml?color=BDB76B&label=test&style=flat-square">
    </a>
    <a href="https://www.python.org/">
        <img src="https://img.shields.io/badge/python-3.10-4682B4?style=flat-square" alt="Python">
    </a>
    <a href="LICENSE">
        <img src="https://img.shields.io/github/license/neurobagel/api?color=CD5C5C&style=flat-square" alt="GitHub license">
    </a>
</div>
<br>
</div>

Neuroimaging Results Visualization (NeRV) is a web interface developed in Python using [Plotly Dash](https://dash.plotly.com/),  [Dash Bootstrap Components](https://dash-bootstrap-components.opensource.faculty.ai/), and [pandas](https://pandas.pydata.org/) for visualization of neuroimaging results obtained from continuous testing of neuroimaging data across software pipelines.

______________________________________________________________________

## Getting Started

### Installation

```bash
pip install nerv
```

In order for NeRV to generate and populate plots the underlying app requires access to the directory containing the datasets. The path to directory can be passed to the app module as input to the start function.

### Example usage

```python
from nerv import app

app.start("path-to-data-directory")
```

After executing the file containing the above code snippet, a local server is started at port 8050 (by default). You can access the running NeRV application using a browser through the URL `localhost:8050`.

<p alt="ui" align="center"><a href="https://github.com/rmanaem/nerv/blob/master/img/ui.png"><img src="https://github.com/rmanaem/nerv/blob/master/img/ui.png?raw=true"/></a></p>

______________________________________________________________________

## Deployment

_Work in progress_

______________________________________________________________________

## License

This project is licensed under the terms of [MIT License](LICENSE).
