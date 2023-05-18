<div align="center">

# Neuroimaging Results Visualization

<div>
    <a href="https://pypi.org/project/nerv/">
        <img src="https://img.shields.io/pypi/v/nerv?color=8FBC8F&style=flat-square" alt="demo">
    </a>
    <a href="https://github.com/rmanaem/nerv/actions/workflows/test.yaml">
        <img src="https://img.shields.io/github/actions/workflow/status/neurobagel/api/test.yaml?color=BDB76B&label=test&style=flat-square" alt="test">
    </a>
    <a href="https://www.python.org/">
        <img src="https://img.shields.io/badge/python-3.10-4682B4?style=flat-square" alt="python">
    </a>
    <a href="LICENSE">
        <img src="https://img.shields.io/github/license/neurobagel/api?color=CD5C5C&style=flat-square" alt="license">
    </a>
</div>
<br>
</div>

Neuroimaging Results Visualization (NeRV) is a Python-based web interface designed for visualizing neuroimaging results obtained from continuous testing of neuroimaging data across software pipelines. It utilizes [Plotly Dash](https://dash.plotly.com/), [Dash Bootstrap Components](https://dash-bootstrap-components.opensource.faculty.ai/), and [pandas](https://pandas.pydata.org/) to provide an interactive and informative visualization experience.\
NeRV is released as a PyPI package, available [here](https://pypi.org/project/nerv/). Explore the [demo](https://nerv-demo.onrender.com/) and experience NeRV in action firsthand. For more information, refer to the [documentation](https://rmanaem.github.io/nerv/).

- [Getting Started](#getting-started)
  - [Installation](#installation)
  - [Example usage](#example-usage)
- [Deployment](#deployment)
- [License](#license)

______________________________________________________________________

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

![ui](https://github.com/rmanaem/nerv/blob/master/img/ui.png?raw=true)

______________________________________________________________________

## Deployment

To deploy your NeRV app, you can utilize [Gunicorn](https://gunicorn.org/). Simply follow the instructions outlined in the Dash documentation [here](https://dash.plotly.comdeployment#heroku-for-sharing-public-dash-apps), making the necessary adjustment in the app.py module content:

**app.py**

```Python
from nerv import app

server = app.start("path-to-data-directory", False)
```

Note that when the `local` parameter of the `start` function is set to `False`, it will return the `app.server` object. This object represents the underlying Flask server that drives the Dash application. You can utilize the `app.server` object to customize and extend the NeRV application, going beyond the default functionality offered. For more details, refer to the [Flask documentation](https://flask.palletsprojects.com/).

______________________________________________________________________

## License

This project is licensed under the terms of [MIT License](LICENSE).
