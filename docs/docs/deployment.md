To deploy your NeRV app, you can utilize [Gunicorn](https://gunicorn.org/). Simply follow the instructions outlined in the Dash documentation [here](https://dash.plotly.comdeployment#heroku-for-sharing-public-dash-apps), making the necessary adjustment in the app.py module content:

**app.py**

```Python
from nerv import app

server = app.start("path-to-data-directory", False)
```

!!! note "Note"

```
When the `local` parameter of the `start` function is set to `False`, it will return the `app.server` object. This object represents the underlying Flask server that drives the Dash application. You can utilize the `app.server` object to customize and extend the NeRV application, going beyond the default functionality offered. For more details, refer to the [Flask documentation](https://flask.palletsprojects.com/).
```

For a demonstration, please refer to [nerv-demo](https://github.com/rmanaem/nerv-demo).
