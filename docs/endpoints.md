# Endpoints

All endpoints accept two parameters specifying start and end time of the query:

- `start_time`
- `end_time`

Dates need to be supplied in UTC as an ISO 8601 string, i.e. `2020-06-07T17:47:29.181948`

An example query for the Facebook endpoint:

````
/facebook?start_time=2020-06-07T17:47:29.181948&end_time=2020-06-08T17:47:29.181948
````

The three top-level endpoints `/twitter` `/facebook` `/media` return the data for all their respective lower-level endpoints.

## `/twitter`

### `/hashtags`

#### Parameters

- `party`

  Accepted values: `CSU` `SPD` `CDU` `AfD` `FDP` `Gruenen` `Linke`

## `/facebook`

### `/posts`

### `/shares`

### `/likes`

### `/reactions`

### `/sentiment`

### `/ads`

## `/media`

### `/attention`

### `/topics_by_media_source`
