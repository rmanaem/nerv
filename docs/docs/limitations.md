NeRV leverages Dash's [built-in sequential color scales](https://plotly.com/python/builtin-colorscales/#builtin-sequential-color-scales) to differentiate pipelines within the same JSON file. This enforces is a limitation on the number of pipelines per file and the number of JSON files per experiment that NeRV can visualize.

!!! info "info"
The maximum number of pipelines allowed varies between 7 and 12, depending on the file system configuration and the assigned color scale for each pipeline, see the table below. Additionally, there is a maximum limit of 8 files per experiment directory.

| color scale | pipeline limit |
| ----------- | -------------- |
| Teal        | 7              |
| OrRd        | 9              |
| Purp        | 7              |
| Green       | 9              |
| Pinkyl      | 7              |
| Brwnyl      | 7              |
| solar       | 12             |
| turbid      | 12             |
