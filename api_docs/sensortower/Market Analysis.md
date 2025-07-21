# Ad Intelligence API v1.0

## Authentication

### auth_token
**Type**: apiKey
**In**: query
**Name**: auth_token

API authentication token. You can generate yours on your <a target="_blank" href="/users/edit/api-settings">account profile (API Settings tab)</a>.


## Servers

### Server 1
**URL**: `https://api.sensortower.com`


## Endpoints

### APPS: Top Charts
#### `GET /v1/{os}/ranking`

Fetches top ranking apps of a particular category and chart type.

Retrieve a list of the top ranking apps on a specific category and chart type.

**Parameters**:
- `os` (path, string, **required**): Operating System
- `category` (query, string, **required**): ID of the Category, <a target='_blank' href='/api/docs/static/category_ids.json'>Category Ids</a>
- `chart_type` (query, string, **required**): The specific top chart type you are looking for, <a target='_blank' href='/api/docs/static/chart_type_ids.json'>
  Chart Type Ids
</a> (<b>This will override the "identifier" parameter</b>)
- `country` (query, string, **required**): The country you want download rankings for, <a target='_blank' href='/api/docs/static/country_ids.json'>Country Codes</a>
- `date` (query, string, **required**): Date. `YYYY-MM-DD` format (defaults to date of latest rankings)

**Responses**:
- `200`: <strong>Success.</strong>
- `401`: <strong>Invalid authentication token.</strong> <br> Generate an API authentication token on your <a target="_blank" href="https://app.sensortower.com/users/edit/api-settings">account profile (API Settings tab)</a> and ensure that your organization has access to this product. <br> Please contact the Sensor Tower team for more information.
  - Content-Type: `application/json`
    - Schema: `object`
- `403`: <strong>Forbidden.</strong> <br> Your API token is not valid. <br> If you lost your API token you can generate a new one on your <a target="_blank" href="https://app.sensortower.com/users/edit/api-settings">account profile (API Settings tab)</a> or contact the Sensor Tower team for more information.
  - Content-Type: `application/json`
    - Schema: `object`
- `422`: <strong>Invalid Query Parameter.</strong> <br> Please check that all required params are present and valid.
  - Content-Type: `application/json`
    - Schema: `object`
---

### APPS: Top Apps by Downloads and Revenue
#### `GET /v1/{os}/sales_report_estimates_comparison_attributes`

Fetches top apps by download and revenue estimates.

Retrieve top apps and their respective absolute, growth, and growth percentage download and revenue estimates. <br><br> <strong>Note:</strong> All revenues are returned in cents.

**Parameters**:
- `os` (path, string, **required**): Operating System
- `comparison_attribute` (query, string, **required**): Comparison Attribute (use "absolute", "delta", or "transformed_delta")
- `time_range` (query, string, **required**): Time Range (use "day", "week", "month", or "quarter")
- `measure` (query, string, **required**): Measure (use "units" or "revenue")
- `device_type` (query, string): Device Type <br> use "iphone", "ipad", or "total" for `ios`, <br> leave blank for `Android`, <br> use "total" for `unified`
- `category` (query, Unknown, **required**): ID of the Category, <a target='_blank' href='/api/docs/static/category_ids.json'>Category Ids</a>
- `date` (query, string, **required**): Date. <br> `YYYY-MM-DD` format. <br> Auto-changes to the beginning of time_range. <br> Ex: Mondays for weeks, 1st of the month, 1st day of the quarter, 1st day of the year.
- `end_date` (query, string): End date, inclusive. <br> `YYYY-MM-DD` format. <br> Allows aggregation of multiple weeks/months/quarters/years. <br> Auto-changes to the end of the specified time_range. <br> Ex: Sundays for weeks, last day of month, last day of quarter, last day of year.
- `regions` (query, array): Regions, separated by commas, <a target='_blank' href='/api/docs/static/country_ids.json'>Regions Codes</a>. <br> <b>`regions` parameter should be specified</b>
- `limit` (query, integer): Limit how many apps per call.<br> (Max: 2000)
- `offset` (query, integer): Number of apps to offset the results by
- `custom_fields_filter_id` (query, string): Filter by Custom fields filter. <br> <b>Requires 'custom_tags_mode' parameter if 'os' is 'unified'</b> <br>Use filter ID from <a target='_blank'
  href='/api/docs/custom_fields_metadata#/CUSTOM%20FIELDS%3A%20Custom%20Fields%20Filter%20ID/create_custom_fields_filter'>
  relevant endpoint
<a>.
- `custom_tags_mode` (query, string): Custom fields filtering mode. <br> <b>Required for unified 'os' if 'custom_fields_filter_id' selected</b>. <br> 'include_unified_apps' allows you to include all versions of a unified app if at least one of them is included by the filters you've set.
- `data_model` (query, string): Specify the data model used to generate estimates. Use "DM_2025_Q1" to access Sensor Tower’s legacy estimates,  or "DM_2025_Q2" to access estimates produced by our new, improved models. Access to this parameter is limited to eligible accounts. If you believe you should have access, please contact your Account Director.

**Responses**:
- `200`: <strong>Success.</strong>
  - Content-Type: `application/json`
    - Schema: `Unknown`
- `401`
- `403`
- `422`
---

### APPS: Top Apps by Active Users
#### `GET /v1/{os}/top_and_trending/active_users`

Fetches top apps by active users.

Retrieve top apps and their respective absolute, growth, and growth percentage active user estimates.

**Parameters**:
- `os` (path, string, **required**): Operating System
- `comparison_attribute` (query, string, **required**): Comparison Attribute (use "absolute", "delta", or "transformed_delta")
- `time_range` (query, string, **required**): Time Range (use "week", "month", or "quarter") <br> "week" is not available when measuing by MAU
- `measure` (query, string, **required**): Measure (use "DAU", "WAU" or "MAU")
- `category` (query, string): ID of the Category, <a target='_blank' href='/api/docs/static/category_ids.json'>Category Ids</a>
- `date` (query, string, **required**): Date, `YYYY-MM-DD` format. Should match beginning of range
- `regions` (query, array): Regions, separated by commas, <a target='_blank' href='/api/ios/usage/countries.json'>Region Codes</a>. <br> <b>`regions` parameter should be specified</b>
- `limit` (query, integer): Limit how many apps per call (defaults to 25)
- `offset` (query, integer): Number of apps to offset the results by
- `device_type` (query, string): Device type parameter is iOS only. On `iOS`, use "iphone", "ipad" or "total". <br> <strong>Note:</strong> For `Android`, leave this blank.
- `custom_fields_filter_id` (query, string): Filter by Custom fields filter. <br> <br>Use filter ID from <a target='_blank'
  href='/api/docs/custom_fields_metadata#/CUSTOM%20FIELDS%3A%20Custom%20Fields%20Filter%20ID/create_custom_fields_filter'>
          relevant endpoint
<a>.
- `data_model` (query, string): Specify the data model used to generate estimates. Use "DM_2025_Q1" to access Sensor Tower’s legacy estimates,  or "DM_2025_Q2" to access estimates produced by our new, improved models. Access to this parameter is limited to eligible accounts. If you believe you should have access, please contact your Account Director.

**Responses**:
- `200`: <strong>Success.</strong>
  - Content-Type: `application/json`
    - Schema: `Unknown`
- `401`
- `403`
- `422`
---

### APPS: Top App Publishers
#### `GET /v1/{os}/top_and_trending/publishers`

Fetches top publishers by download and revenue estimates.

Retrieve top app publishers and their respective absolute, growth, and growth percentage download and revenue estimates. <br><br> <strong>Note:</strong> All revenues are returned in cents.

**Parameters**:
- `os` (path, string, **required**): Operating System
- `comparison_attribute` (query, string, **required**): Comparison Attribute (use "absolute", "delta", or "transformed_delta")
- `time_range` (query, string, **required**): Time Range (use "day", "week", "month", or "quarter")
- `measure` (query, string, **required**): Comparison Attribute (use "units" or "revenue")
- `device_type` (query, string): Device Type <br> use "iphone", "ipad", or "total" for `ios`, <br> leave blank for `Android`, <br> use "total" for `unified`
- `category` (query, Unknown, **required**): ID of the Category, <a target='_blank' href='/api/docs/static/category_ids.json'>Category Ids</a>
- `date` (query, string, **required**): Date. <br> `YYYY-MM-DD` format. <br> Auto-changes to the beginning of time_range. <br> Ex: Mondays for weeks, 1st of the month, 1st day of the quarter, 1st day of the year.
- `end_date` (query, string): End date, inclusive. <br> `YYYY-MM-DD` format. <br> Allows aggregation of multiple weeks/months/quarters/years. <br> Auto-changes to the end of the specified time_range. <br> Ex: Sundays for weeks, last day of month, last day of quarter, last day of year.
- `country` (query, string): Country or Region Code, <a target='_blank' href='/api/docs/static/country_ids.json'>Country Codes</a>, <a target='_blank' href='/api/docs/static/region_ids.json'>Region Codes</a>.
- `limit` (query, integer): Limit how many publishers per call
- `offset` (query, integer): Number of publishers to offset the results by

**Responses**:
- `200`: <strong>Success.</strong>
  - Content-Type: `application/json`
    - Schema: `Unknown`
- `401`
- `403`
- `422`
---

### APPS: Store Summary
#### `GET /v1/{os}/store_summary`

Fetches aggregated download and revenue estimates of store categories.

Retrieve aggregated download and revenue estimates of store categories by country and date. <br><br> <strong>Note:</strong> The latest day's available Google Play estimates may change. More data becomes available to us a day later and we use this data to recalibrate the estimate for increased accuracy. <br><br> <strong>Note:</strong> All revenues are returned in cents.

**Parameters**:
- `os` (path, string, **required**): Operating System
- `categories` (query, array, **required**): IDs of the Categories, <a target='_blank' href='/api/docs/static/category_ids.json'>Category Ids</a> (use "categories" for multiples, separated by commas). Game categories are also supported, but the game_breakdown endpoint is recommended.
- `countries` (query, array): Specify the countries you want download / revenue for, <a target='_blank' href='/api/docs/static/country_ids.json'>Country Codes</a>, separated by commas (use "WW" for worldwide)
- `date_granularity` (query, string, **required**): Aggregate estimates by granularity (use "daily", "weekly", "monthly", or "quarterly") defaults to "daily"
- `start_date` (query, string, **required**): Start Date, `YYYY-MM-DD` Format
- `end_date` (query, string, **required**): End Date, `YYYY-MM-DD` Format

**Responses**:
- `200`: <strong>Success.</strong>
  - Content-Type: `application/json`
    - Schema: `Unknown`
- `401`
- `403`
- `422`
---

### ADVERTISING: Top Advertisers and Ad Publishers
#### `GET /v1/{os}/ad_intel/top_apps`

Fetches the top advertisers or publishers over a given time period.

Fetches the current and prior Share of Voice for the top advertisers or publishers over a given time period.

**Parameters**:
- `os` (path, string, **required**): Operating System.
- `role` (query, string, **required**): Advertisers or publishers.
- `date` (query, string, **required**): Start date for impression data, `YYYY-MM-DD` format.
- `period` (query, string, **required**): Time period to calculate Share of Voice.
- `category` (query, string, **required**): Category ID to return results for (<a target='_blank' href='/api/docs/static/category_ids.json'>Category Ids</a>). Use iOS categories for unified.
- `country` (query, string, **required**): Country to return results for (<a target='_blank' href='/api/ios/ad_intel/countries.json'>Countries</a>).
- `network` (query, string, **required**): Network to return results for (<a target='_blank' href='/api/ios/ad_intel/networks.json'>Networks</a>).
- `custom_fields_filter_id` (query, string): Filter by Custom fields filter. <br> <br>Use filter ID from <a target='_blank'
  href='/api/docs/custom_fields_metadata#/CUSTOM%20FIELDS%3A%20Custom%20Fields%20Filter%20ID/create_custom_fields_filter'>
  relevant endpoint
<a>.
- `limit` (query, integer): Limits the number of apps returned, maximum of 250.
- `page` (query, integer): Page number. Total number of pages is returned in response field "pages".

**Responses**:
- `200`: <strong>Success.</strong>
- `401`
- `403`
- `422`
---
#### `GET /v1/{os}/ad_intel/top_apps/search`

Fetches the rank of an advertiser or publisher.

Fetches the rank of a top advertiser or top publisher in apps matching the provided filters.

**Parameters**:
- `os` (path, string, **required**): Operating System.
- `app_id` (query, string, **required**): App to search for.
- `role` (query, string, **required**): Search advertisers or publishers.
- `date` (query, string, **required**): Date to search, `YYYY-MM-DD` format.
- `period` (query, string, **required**): Time period to search.
- `category` (query, string, **required**): Category to search (<a target='_blank' href='/api/docs/static/category_ids.json'>Category Ids</a>). Use iOS categories for unified.
- `country` (query, string, **required**): Country to search (<a target='_blank' href='/api/ios/ad_intel/countries.json'>Countries</a>).
- `network` (query, string, **required**): Network to search (<a target='_blank' href='/api/ios/ad_intel/networks.json'>Networks</a>).

**Responses**:
- `200`: <strong>Success.</strong>
- `401`
- `403`
- `422`
---

### ADVERTISING: Top Creatives
#### `GET /v1/{os}/ad_intel/creatives/top`

Fetches the top creatives over a given time period.

Fetches the top creatives over a given time period.

**Parameters**:
- `os` (path, string, **required**): Operating System.
- `date` (query, string, **required**): Start date for creatives data, `YYYY-MM-DD` format.
- `period` (query, string, **required**): Time period for creatives data.
- `category` (query, string, **required**): Category ID to return results for (<a target='_blank' href='/api/docs/static/category_ids.json'>Category Ids</a>). Use iOS categories for unified.
- `country` (query, string, **required**): Country to return results for (<a target='_blank' href='/api/ios/ad_intel/countries.json'>Countries</a>).
- `network` (query, string, **required**): Network to return results for. List of networks: (<a target='_blank' href='/api/ios/ad_intel/creative_networks.json'>ios networks</a>), (<a target='_blank' href='/api/android/ad_intel/creative_networks.json'>android networks</a>), (<a target='_blank' href='/api/unified/ad_intel/creative_networks.json'>unified networks</a>).
- `ad_types` (query, array, **required**): Ad types to include, separated by commas.
- `limit` (query, integer): Limits the number of apps returned, maximum of 250.
- `page` (query, integer): Page number. Total number of pages can be calculated by dividing "count" from response by limit size.
- `placements` (query, array): Ad placement(s) to include, separated by commas.
- `video_durations` (query, array): The video durations to include, separated by commas. To filter video durations using ranges, one can specify the start and end points of each range in seconds, separated by a colon. For instance, `10:30` would filter videos longer than 10 seconds but 30 seconds or shorter. Multiple ranges can be applied simultaneously, with the logic that a video's duration only needs to meet the criteria of one range to be included. Open-ended ranges are also possible, where only one end of the range is specified, such as `:3` to include videos up to 3 seconds long, or `60:` for videos longer than 60 seconds.
- `aspect_ratios` (query, array): Specify the aspect ratios to include, separated by commas. This applies to all creative ad types except banners; for banners this parameter is ignored. The parameter can accept one or more values from a predefined set of common aspect ratios available. Aspect ratio sets are used as buckets, grouping creatives that might not fit the ratio fully, as we assume a small margin of error while computing the exact width and height
- `banner_dimensions` (query, array): Specify the banner dimensions to include, separated by commas. This applies to banner creatives only; this parameter will be ignored for the creatives of other ad types. The parameter can accept one or more values from a predefined set.
- `new_creative` (query, boolean): New creative flag. If the parameter's value is 'true', the endpoint will return new creatives only. The new creatives are creatives which are first seen in requested date range.

**Responses**:
- `200`: <strong>Success.</strong>
- `401`
- `403`
- `422`: <strong>Invalid Query Parameter.</strong> <br> Please check that all required params are present and valid.
  - Content-Type: `application/json`
    - Schema: `object`
---

### GAMES: Game Summary
#### `GET /v1/{os}/games_breakdown`

Fetches aggregated download and revenue estimates of game categories.

Retrieve aggregated download and revenue estimates of game categories by country and date. <a target='blank' href='/api/docs/static/games_breakdown_key.json'>Game Summary Response Key</a> <br><br> <strong>Note:</strong> The latest day's available Google Play estimates may change. More data becomes available to us a day later and we use this data to recalibrate the estimate for increased accuracy. <br><br> <strong>Note:</strong> All revenues are returned in cents.

**Parameters**:
- `os` (path, string, **required**): Operating System
- `categories` (query, array, **required**): IDs of Game Categories, <a target='_blank' href='/api/docs/static/category_ids.json'>Category Ids</a> (use "categories" for multiples, separated by commas). Play and the App Store use completely different game category IDs.
- `countries` (query, array): Specify the countries you want download / revenue for, <a target='_blank' href='/api/docs/static/country_ids.json'>Country Codes</a>, separated by commas (use "WW" for worldwide)
- `date_granularity` (query, string, **required**): Aggregate estimates by granularity (use "daily", "weekly", "monthly", or "quarterly") defaults to "daily"
- `start_date` (query, string, **required**): Start Date, `YYYY-MM-DD` Format. Data before 2016-01-01 is not supported.
- `end_date` (query, string, **required**): End Date, `YYYY-MM-DD` Format

**Responses**:
- `200`: <strong>Success.</strong>
  - Content-Type: `application/json`
    - Schema: `Unknown`
- `401`
- `403`
- `422`
---



---

*Generated on 2025-07-21 21:03:46*