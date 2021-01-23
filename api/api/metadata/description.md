REST-API to access current and historical data from [political-dashboard.com](https://political-dashboard.com) \
The data collection and analysis process is described in this [paper](https://ojs.aaai.org/index.php/ICWSM/article/view/7371) \
An overview of the methodology is available [here](https://political-dashboard.com/methodology.pdf)

The data collection effort was started in 2017 and is limited to German language content and
specifically focuses on German politics.

Because of the strict copyright protection of virtually all collected data, none of the raw
data can be republished. Thus only aggregated data and analysis results are offered.

All endpoints accept the query parameters `start_date` and `end_date`. You can query
for maximum 10 days in a single request. By default only data for the current day is
returned.

Please report issues on [Github](https://github.com/nikstur/political-dashboard-api/issues)
