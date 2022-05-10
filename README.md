# Neuroimaging Results Visualization

Neuroimaging Results Visualization (NeRV) is an interface developed in Python using Plotly Dash and pandas for visualization of neuroimaging results obtained from continuous testing of neuroimaging data across software pipelines.

## Getting Started

### Install the package using pip

```cmd
pip install nerv
```

In order for NeRV to generate and populate plots the underlying app requires access to the directory containing the datasets. The path to directory can be passed to the app module as input to the start function.

### Example usage

```python
from nerv import app

app.start("path-to-data-directory")
```

Once the file containing the above snipet is executed, a local server (at port 8050 by default) is launched. The server and the app can be accessed by browser through `localhost:8050` url.

## Deployment

*Work in progress*

## Developed with

* [Python](https://www.python.org/)
* [Plotly](https://plotly.com/python/)
* [pandas](https://pandas.pydata.org/)

## Author

* **Arman Jahanpour** - [rmanaem](https://www.python.org/rmanaem)

## License

This package is licensed under the [MIT License](LICENSE).
