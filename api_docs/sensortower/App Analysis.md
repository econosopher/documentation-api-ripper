# App Intelligence API v1.0

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

### OVERVIEW: App Overview
#### `GET /v1/{os}/apps`

Fetches app metadata.

<p>Retrieve app metadata, such as app name, publisher, categories,
description, screenshots, rating, etc.</p>
<p>Limit: <code>100</code> app_ids per call</p>


**Parameters**:
- `os` (path, string, **required**): Operating System
- `app_ids` (query, array, **required**): App IDs of apps, separated by commas (limited to 100)
- `country` (query, string): Country Code,
<a target='_blank' href='/api/docs/static/country_ids.json'>Country Codes</a>
(defaults to "US")
- `include_sdk_data` (query, boolean): Include SDK Insights data (requires subscription)

**Responses**:
- `200`: <strong>Success.</strong>
  - Content-Type: `application/json`
    - Schema: `object`
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
#### `GET /v1/ios/apps/top_in_app_purchases`

Fetches the top in-app purchases for particular apps.

<p>Retrieve top in-app purchases for the requested App IDs.</p>
<p>Limit: 100 <code>app_ids</code> per call</p>


**Parameters**:
- `app_ids` (query, array, **required**): App IDs of apps, separated by commas (limited to 100)
- `country` (query, string): Specify the country you want update history for,
              <a target='_blank' href='/api/docs/static/country_ids.json'>Country Codes</a> (defaults to "US")

**Responses**:
- `200`: <strong>Success.</strong>
- `401`
- `403`
- `422`
---

### PERFORMANCE: Downloads & Revenue
#### `GET /v1/{os}/sales_report_estimates`

Fetches download and revenue estimates of apps and publishers.

Retrieve download and revenue estimates of apps by country and date. <a target='blank' href='/api/docs/static/sales_report_estimates_key.json'>
  Download / Revenue Estimate Response Key
</a> <br><br> <strong>Note:</strong> The latest day's available Google Play estimates may change. More data becomes available to us a day later and we use this data to recalibrate the estimate for increased accuracy. <br><br> <b>At least one app ID, or one publisher ID is required.</b> Some Android publisher IDs contain commas. If you want to query by these publisher IDs, please use the <b>array parameter format</b> instead of the comma separated format. (I.e. <code>?publisher_ids[]=AndroidPubId1&publisher_ids[]=AndroidPubId2&publisher_ids[]=...</code>) <br><br> There are times when the API will timeout or return an <b>Internal Server Error</b> response.  When this occurs, it is recommended to segment the query by <b>start_date</b> and <b>end_date</b> depending on the <b>date_granularity</b> as follows: <br> <table>
  <tr>
    <td><b>date_granularity</b></td>
    <td><b>Recommendation</b></td>
  </tr>
  <tr>
    <td>daily</td>
    <td>limit start_date and end_date to 1 week segments</td>
  </tr>
  <tr>
    <td>weekly</td>
    <td>limit start_date and end_date to 3 month segments</td>
  </tr>
  <tr>
    <td>monthly</td>
    <td>limit start_date and end_date to 1 year segments</td>
  </tr>
  <tr>
    <td>quarterly</td>
    <td>limit start_date and end_date to 2 year segments</td>
  </tr>
</table> <br><br> <strong>Note:</strong> All revenues are returned in cents.

**Parameters**:
- `os` (path, string, **required**): Operating System
- `app_ids` (query, array): IDs of apps, separated by commas
- `publisher_ids` (query, array): Publisher IDs of apps, separated by commas <span style='color: #FF0000'>(See implementation notes for specific implementations regarding Android publisher IDs)</span>
- `countries` (query, array): Specify the countries you want download / revenue for, <a target='_blank' href='/api/docs/static/country_ids.json'>Country Codes</a>, separated by commas (use "WW" for worldwide)
- `date_granularity` (query, string, **required**): Aggregate estimates by granularity (use "daily", "weekly", "monthly", or "quarterly") defaults to "daily"
- `start_date` (query, string, **required**): Start Date, `YYYY-MM-DD` Format
- `end_date` (query, string, **required**): End Date, `YYYY-MM-DD` Format
- `data_model` (query, string): Specify the data model used to generate estimates. Use "DM_2025_Q1" to access Sensor Tower’s legacy estimates,  or "DM_2025_Q2" to access estimates produced by our new, improved models. Access to this parameter is limited to eligible accounts. If you believe you should have access, please contact your Account Director.

**Responses**:
- `200`: <strong>Success.</strong>
  - Content-Type: `application/json`
    - Schema: `Unknown`
- `401`
- `403`
- `422`
---
#### `GET /v1/{os}/compact_sales_report_estimates`

Fetches download and revenue estimates of apps and publishers in compact format.

Retrieve datasets of download and revenue estimates of apps by country and date. All revenues are returned in cents. <br><br> <strong>Note:</strong> The latest few days estimates could change since our models retroactively increase accuracy of recent data. <br> This endpoint lags behind regular <a href="/api/docs/app_analysis#/PERFORMANCE%3A%20Downloads%20%26%20Revenue/sales_report_estimates" target="_blank">Download / Revenue Estimates</a> endpoint a few hours and this can cause a temporary discrepancy of data between these two endpoints. <br><br> At least one of the App ID, Publisher ID, or Category parameters is required. <br><br> If a response is too large or if the endpoint takes too long to respond it will return an error. To prevent this, reduce the number of apps requested per call: <br> <table>
  <tr>
    <td><b>Parameter</b></td>
    <td><b>Recommendation</b></td>
  </tr>
  <tr>
    <td>app_ids, unified_app_ids</td>
    <td>No more than 100 IDs</td>
  </tr>
  <tr>
    <td>publisher_ids, unified_publisher_ids</td>
    <td>If a publisher has many apps it's recommended to fetch one publisher at a time</td>
  </tr>
</table>


**Parameters**:
- `os` (path, string, **required**): Operating System
- `start_date` (query, string, **required**): Start Date, `YYYY-MM-DD` Format
- `end_date` (query, string, **required**): End Date, `YYYY-MM-DD` Format
- `app_ids` (query, array): IDs of apps, separated by commas
- `publisher_ids[]` (query, array): Publisher IDs of apps. Please use the <b>array parameter format</b><br>
(i.e. publisher_ids[]=id1&publisher_ids[]=id2&...)

- `unified_app_ids` (query, array): IDs of unified apps, separated by commas
- `unified_publisher_ids` (query, array): IDs of unified publishers, separated by commas
- `categories` (query, array): Categories, separated by commas, see
              <a target='_blank' href='/api/docs/static/category_ids.json'>Category IDs</a>.
- `date_granularity` (query, string): Aggregate estimates by granularity
- `data_model` (query, string): Specify the data model used to generate estimates. Use "DM_2025_Q1" to access Sensor Tower’s legacy estimates,  or "DM_2025_Q2" to access estimates produced by our new, improved models. Access to this parameter is limited to eligible accounts. If you believe you should have access, please contact your Account Director.

**Responses**:
- `200`: <strong>Success.</strong>
  - Content-Type: `application/json`
    - Schema: `object`
- `401`
- `403`
- `422`
---

### PERFORMANCE: Active Users
#### `GET /v1/{os}/usage/active_users`

Fetches active user estimates of apps.

Retrieve active user estimates of apps per country by date and time period.

**Parameters**:
- `os` (path, string, **required**): Operating System
- `app_ids` (query, array, **required**): IDs of apps, separated by commas. Maximum 500 app ids. With "unified" os use Unified App IDs.<br>If apps that do not meet <a target='_blank' href='https://help.sensortower.com/hc/en-us/articles/6985667275675-What-is-a-Disabled-Small-App-in-Usage-Intelligence-'> minimum requirements for usage estimates</a> are requested, they will not be taken into consideration.
- `time_period` (query, string, **required**): Aggregate estimates by time period. Use "day" to get DAU, "week" for WAU, "month" for MAU.
- `start_date` (query, string, **required**): Start Date, `YYYY-MM-DD` Format. <br> Auto-changes to the beginning of time_period. Note that weeks begin on Monday.
- `end_date` (query, string, **required**): End Date, `YYYY-MM-DD` Format.<br> Auto-changes to the end of the specified time_period.
- `countries` (query, array): Countries to return results for, separated by commas, <a target='_blank' href='/api/v1/usage/countries.json'>Country Codes</a>. <br> Also supports 'WW' code (Worldwide).

- `data_model` (query, string): Specify the data model used to generate estimates. Use "DM_2025_Q1" to access Sensor Tower’s legacy estimates,  or "DM_2025_Q2" to access estimates produced by our new, improved models. Access to this parameter is limited to eligible accounts. If you believe you should have access, please contact your Account Director.

**Responses**:
- `200`: <strong>Success.</strong>
  - Content-Type: `application/json`
    - Schema: `Unknown`
- `401`
- `403`
- `422`
---

### PERFORMANCE: Category Rankings
#### `GET /v1/{os}/category/category_history`

Fetches detailed category ranking history of a particular app, category, and chart type.

Retrieve historical ranking information for a particular app, category, and chart type. You can request data for multiple apps, categories, chart types, and countries. Please refer to the parameter's description for more information.

**Parameters**:
- `os` (path, string, **required**): Operating System
- `app_ids` (query, array, **required**): IDs of Apps (separated by commas)
- `category` (query, string, **required**): Category ID to return results for (<a target='_blank' href='/api/docs/static/category_ids.json'>Category Ids</a>).
- `chart_type_ids` (query, array, **required**): IDs of the Chart Type, separated by commas <br> <a target='_blank' href='/api/docs/static/chart_type_ids.json'>
  Chart Type Ids Mapping
</a>
- `countries` (query, array, **required**): Specify the countries you want download rankings for, separated by commas <br> <a target='_blank' href='/api/docs/static/country_ids.json'>Country Codes</a>
- `start_date` (query, string): Start Date, `YYYY-MM-DD` format (defaults to 90 days ago)
- `end_date` (query, string): End Date, `YYYY-MM-DD` format (defaults to today)
- `is_hourly` (query, boolean): Hourly rankings (only for iOS)

**Responses**:
- `200`: <strong>Success.</strong>
- `401`
- `403`
- `422`
---
#### `GET /v1/{os}/category/category_ranking_summary`

Fetches today's category ranking summary of a particular app.

Retrieve today's category ranking summary for a particular app with data on chart type, category, and rank.

**Parameters**:
- `os` (path, string, **required**): Operating System
- `app_id` (query, string, **required**): ID of App
- `country` (query, string, **required**): Specify the country you want download rankings for, <a target='_blank' href='/api/docs/static/country_ids.json'>Country Codes</a>

**Responses**:
- `200`: <strong>Success.</strong>
- `401`
- `403`
- `422`
---

### ADVERTISING: Creative Gallery
#### `GET /v1/{os}/ad_intel/creatives`

Fetches creatives for advertising apps.

Fetches creatives for an advertising app and includes Share of Voice and top publishers for each creative.

**Parameters**:
- `os` (path, string, **required**): Operating System
- `app_ids` (query, array, **required**): Apps to return creatives for, separated by commas.
- `start_date` (query, string, **required**): Start date for creatives, `YYYY-MM-DD` format.
- `end_date` (query, string): End date for creatives, `YYYY-MM-DD` format. (defaults to today)
- `countries` (query, array, **required**): Countries to return results for, separated by commas (<a target='_blank' href='/api/ios/ad_intel/countries.json'>Countries</a>).
- `networks` (query, array, **required**): Networks to return results for, separated by commas. List of networks: (<a target='_blank' href='/api/ios/ad_intel/creative_networks.json'>ios networks</a>), (<a target='_blank' href='/api/android/ad_intel/creative_networks.json'>android networks</a>), (<a target='_blank' href='/api/unified/ad_intel/creative_networks.json'>unified networks</a>).
- `ad_types` (query, array, **required**): Ad types to include, separated by commas.
- `limit` (query, integer): Limits the number of creatives returned, maximum of 100.
- `page` (query, integer): Page number. Total number of pages can be calculated by dividing "count" from response by limit size.
- `display_breakdown` (query, boolean): Display breakdown flags. Control if breakdown fields (breakdown and top_publishers) displays in ad unit.
- `placements` (query, array): Ad placement(s) to include, separated by commas.
- `video_durations` (query, array): The video durations to include, separated by commas. To filter video durations using ranges, one can specify the start and end points of each range in seconds, separated by a colon. For instance, `10:30` would filter videos longer than 10 seconds but 30 seconds or shorter. Multiple ranges can be applied simultaneously, with the logic that a video's duration only needs to meet the criteria of one range to be included. Open-ended ranges are also possible, where only one end of the range is specified, such as `:3` to include videos up to 3 seconds long, or `60:` for videos longer than 60 seconds.
- `aspect_ratios` (query, array): Specify the aspect ratios to include, separated by commas. This applies to all creative ad types except banners; for banners this parameter is ignored. The parameter can accept one or more values from a predefined set of common aspect ratios available. Aspect ratio sets are used as buckets, grouping creatives that might not fit the ratio fully, as we assume a small margin of error while computing the exact width and height
- `banner_dimensions` (query, array): Specify the banner dimensions to include, separated by commas. This applies to banner creatives only; this parameter will be ignored for the creatives of other ad types. The parameter can accept one or more values from a predefined set.
- `new_creative` (query, boolean): New creative flag. If the parameter's value is 'true', the endpoint will return new creatives only. The new creatives are creatives which are first seen in requested date range.

**Responses**:
- `200`: <strong>Success.</strong>
- `401`
- `403`
- `422`
---

### ADVERTISING: Network Analysis
#### `GET /v1/{os}/ad_intel/network_analysis`

Fetches the impressions share of voice (SOV) time series of the requested apps.

Fetches the SOV time series of the requested apps.

**Parameters**:
- `os` (path, string, **required**): Operating System.
- `app_ids` (query, array, **required**): Apps to return SOV for, separated by commas.
- `start_date` (query, string, **required**): Start date for the impressions share of voice data, `YYYY-MM-DD` format. Minimum date is 2018-01-01.
- `end_date` (query, string, **required**): End date for the impressions share of voice data, `YYYY-MM-DD` format.
- `period` (query, string, **required**): Time period to calculate Share of Voice for.
- `networks` (query, array): Networks to return results for, separated by commas (<a target='_blank' href='/api/unified/ad_intel/networks.json'>Networks</a>).
- `countries` (query, array): Countries to return results for, separated by commas (<a target='_blank' href='/api/ios/ad_intel/countries.json'>Countries</a>).

**Responses**:
- `200`: <strong>Success.</strong>
  - Content-Type: `application/json`
    - Schema: `array`
- `401`
- `403`
- `422`
---
#### `GET /v1/{os}/ad_intel/network_analysis/rank`

Fetches the ranks for the countries, networks and dates of the requested apps.

Fetches the ranks for the countries, networks and dates of the requested apps.

**Parameters**:
- `os` (path, string, **required**): Operating System.
- `app_ids` (query, array, **required**): Apps to return SOV for, separated by commas.
- `start_date` (query, string, **required**): Start date for the rank data, `YYYY-MM-DD` format. Minimum date is 2018-01-01.
- `end_date` (query, string, **required**): End date for the rank data, `YYYY-MM-DD` format.
- `period` (query, string, **required**): Time period to calculate ranks for.
- `networks` (query, array): Networks to return results for, separated by commas (<a target='_blank' href='/api/unified/ad_intel/networks.json'>Networks</a>).
- `countries` (query, array): Countries to return results for, separated by commas (<a target='_blank' href='/api/ios/ad_intel/countries.json'>Countries</a>).

**Responses**:
- `200`: <strong>Success.</strong>
  - Content-Type: `application/json`
    - Schema: `array`
- `401`
- `403`
- `422`
---

### ACQUISITION & CHURN: Retention
#### `GET /v1/{os}/usage/retention`

Fetches retention of apps.

Retrieve retention of apps (from day 1 to day 90), along with the baseline retention. <br><br> Mapping between confidence levels and their respective confidence color in the UI: <br> <table>
  <tr>
    <td>UI Color</td>
    <td>Confidence Level</td>
  </tr>
  <tr>
    <td>red</td><td> &lt= 3</td>
  </tr>
  <tr>
    <td>yellow</td><td>4 - 6</td>
  </tr>
  <tr>
    <td>green</td><td> &gt= 7</td>
  </tr>
</table>


**Parameters**:
- `os` (path, string, **required**): Operating System
- `app_ids` (query, array, **required**): IDs of apps, separated by commas. Maximum 500 app ids.<br>If apps that do not meet  <a target='_blank' href='https://help.sensortower.com/hc/en-us/articles/6985667275675-What-is-a-Disabled-Small-App-in-Usage-Intelligence-'> minimum requirements for usage estimates</a> are requested, they will not be taken into consideration; their IDs can be found in the disabled_app_ids field.
- `date_granularity` (query, string, **required**):  Aggregate estimates by granularity (use "all_time", or "quarterly") 
- `start_date` (query, string, **required**): Start Date, `YYYY-MM-DD` Format
- `end_date` (query, string): End Date, `YYYY-MM-DD` Format. If specified, all date periods between start_date and end_date are to be returned. E.g. if 'date_granularity' is set to 'quarterly', 'start_date' is '2021-01-01' and 'end_date' is '2021-08-01', response will contain data for Q1, Q2 and Q3 of 2021. If 'date_granularity' is set to 'all_time', 'end_date' parameter is ignored.
- `country` (query, string): Country (<a target='_blank' href='/api/v1/usage/countries.json'>country codes</a>) or region (<a target='_blank' href='/api/v1/usage/regions.json'>region codes</a>) to return results for. (Leave blank for Worldwide.) <br> Quarterly regional and country data begins in Q1 2021. Worldwide and All Time data goes back to Q4 2015.


**Responses**:
- `200`: <strong>Success.</strong>
  - Content-Type: `application/json`
    - Schema: `Unknown`
- `401`
- `403`
- `422`
---

### ACQUISITION & CHURN: Downloads by Source
#### `GET /v1/{os}/downloads_by_sources`

Fetches app downloads by sources

Fetch percentages and absolute values for all three download sources: organic, paid, and browser. <br> Regardless of the OS parameter, this endpoint only accepts Unified app IDs and returns data grouped by Unified app IDs.

**Parameters**:
- `os` (path, string, **required**): Operating System. This parameter doesn't affect app_ids. It always expects Unified apps IDs. <br> If "Android" or "iOS" is selected, only apps from this platform will be taken into account.
- `app_ids` (query, array, **required**): Unified app IDs, separated by commas
- `countries` (query, array, **required**): Country codes, separated by commas. For worldwide data, use 'WW'. <br> Note that this product leverages the set of worldwide countries available in Google Play, which notably excludes China. <br> <a target='_blank' href='/api/docs/static/country_ids.json'>Country Codes</a>.
- `date_granularity` (query, string): Aggregate estimates by granularity (use "daily" or "monthly"). Defaults to "monthly".
- `start_date` (query, string, **required**): Start Date, `YYYY-MM-DD` Format
- `end_date` (query, string, **required**): End Date, `YYYY-MM-DD` Format

**Responses**:
- `200`: <strong>Success.</strong>
  - Content-Type: `application/json`
    - Schema: `object`
- `401`
- `403`
- `422`
---

### ACQUISITION & CHURN: Acquisition & Churn
#### `GET /v1/{os}/consumer_intel/churn_analysis`

Fetches churn analysis.

Fetches app churn rate as well as active user breakdown metrics (percentage of new, resurrected, and retained users). <br> <br> <strong>Note:</strong> There may be gaps in the data in which case null values will be given.


**Parameters**:
- `os` (path, string, **required**): Operating System
- `selection_cohort_ids` (query, array, **required**): IDs of selection cohorts, separated by commas. (Max: 5) <br> Can be queried with <a href="/api/docs/app_analysis#/ACQUISITION%20%26%20CHURN%3A%20Acquisition%20%26%20Churn/churn_analysis_cohorts" target="_blank">
  Churn Analysis Cohorts
</a>

- `country` (query, string): Country to return results for (leave blank for Worldwide)
- `granularity` (query, string, **required**): Churn Analysis by granularity
- `start_date` (query, string, **required**): Start Date, `YYYY-MM-DD` Format (minimum date: 2020-05-01)
- `end_date` (query, string, **required**): End Date, `YYYY-MM-DD` Format

**Responses**:
- `200`: <strong>Success.</strong>
  - Content-Type: `application/json`
    - Schema: `object`
- `401`
- `403`
- `422`
---
#### `GET /v1/{os}/consumer_intel/churn_analysis/cohorts`

Fetches cohorts.

Fetches the available cohorts.

**Parameters**:
- `os` (path, string, **required**): Operating System

**Responses**:
- `200`: <strong>Success.</strong>
  - Content-Type: `application/json`
    - Schema: `Unknown`
- `401`
- `403`
- `422`
---
#### `GET /v1/{os}/consumer_intel/cohort_retention`

Fetches cohort retention.

Fetches the cohort retention from a specific subset of panel users.

**Parameters**:
- `os` (path, string, **required**): Operating System
- `selection_cohort_ids` (query, array, **required**): IDs of selection cohorts, separated by commas. (Max: 5) <br> Can be queried with <a href="/api/docs/app_analysis#/ACQUISITION%20%26%20CHURN%3A%20Acquisition%20%26%20Churn/cohort_retention_cohorts" target="_blank">
  Cohort Retention Cohorts
</a>

- `granularity` (query, string, **required**): Retention by granularity
- `start_date` (query, string, **required**): Start Date, `YYYY-MM-DD` Format (minimum date: 2020-03-30)
- `end_date` (query, string, **required**): End Date, `YYYY-MM-DD` Format

**Responses**:
- `200`: <strong>Success.</strong>
  - Content-Type: `application/json`
    - Schema: `object`
- `401`
- `403`
- `422`
---
#### `GET /v1/{os}/consumer_intel/cohort_retention/cohorts`

Fetches cohorts.

Fetches the available cohorts.

**Parameters**:
- `os` (path, string, **required**): Operating System

**Responses**:
- `200`: <strong>Success.</strong>
  - Content-Type: `application/json`
    - Schema: `Unknown`
- `401`
- `403`
- `422`
---

### USAGE: Demographics
#### `GET /v1/{os}/usage/demographics`

Fetches demographic of apps.

Retrieve demographic breakdown of apps (by gender and age range), along with the baseline demographic. <br><br> Mapping between confidence levels and their respective confidence color in the UI: <br> <table>
  <tr>
    <td>UI Color</td>
    <td>Confidence Level</td>
  </tr>
  <tr>
    <td>red</td><td> &lt= 3</td>
  </tr>
  <tr>
    <td>yellow</td><td>4 - 6</td>
  </tr>
  <tr>
    <td>green</td><td> &gt= 7</td>
  </tr>
</table>


**Parameters**:
- `os` (path, string, **required**): Operating System
- `app_ids` (query, array, **required**): IDs of apps, separated by commas. Maximum 500 app ids.<br>If apps that do not meet  <a target='_blank' href='https://help.sensortower.com/hc/en-us/articles/6985667275675-What-is-a-Disabled-Small-App-in-Usage-Intelligence-'> minimum requirements for usage estimates</a> are requested, they will not be taken into consideration; their IDs can be found in the disabled_app_ids field.
- `date_granularity` (query, string, **required**): Aggregate estimates by granularity (use "all_time", or "quarterly")
- `start_date` (query, string, **required**): Start Date, `YYYY-MM-DD` Format
- `end_date` (query, string): End Date, `YYYY-MM-DD` Format. If specified, all date periods between start_date and end_date are to be returned. E.g. if 'date_granularity' is set to 'quarterly', 'start_date' is '2021-01-01' and 'end_date' is '2021-08-01', response will contain data for Q1, Q2 and Q3 of 2021. If 'date_granularity' is set to 'all_time', 'end_date' parameter is ignored.
- `country` (query, string): Country (<a target='_blank' href='/api/v1/usage/demographics/countries.json'>country codes</a>) or region (<a target='_blank' href='/api/v1/usage/regions.json'>region codes</a>) to return results for. (Leave blank for Worldwide.) <br> Quarterly regional and country data begins in Q1 2021. Worldwide and All Time data goes back to Q4 2015.


**Responses**:
- `200`: <strong>Success.</strong>
  - Content-Type: `application/json`
    - Schema: `object`
- `401`
- `403`
- `422`
---

### USAGE: Session Metrics (Time Spent, Session Count)
#### `GET /v1/apps/timeseries`

Fetch time series data for non-unified apps.

Retrieve session metrics data across a time series for Android or iOS apps. <br><br> Supported metrics include:
  - time_spent (seconds)
  - total_time_spent (seconds)
  - session_duration (seconds)
  - session_count
  - total_session_count

**Parameters**:
- `start_date` (query, string, **required**): Start Date in `YYYY-MM-DD` format. Data is available from 2021-01-01 onward.
- `end_date` (query, string, **required**): End Date in `YYYY-MM-DD` format.
- `app_ids` (query, array, **required**): App IDs, separated by commas (maximum 100).
- `timeseries` (query, array, **required**): Time series metrics, separated by commas.
- `regions` (query, array): Regions, separated by commas. All regions are included unless specified. <a target='_blank' href='/api/ios/usage/countries.json'>Region Codes</a>.

- `time_period` (query, string, **required**): Specifies the session metrics time period.<br> Returns averaged session metrics for each period within a month.<br> Example: "week" = average session metrics per week, averaged over all weeks in a month.

- `breakdown` (query, string, **required**): Fields used for data aggregation, separated by commas.<br> The specified fields will be preserved in the response, while others will be aggregated.


**Responses**:
- `200`: <strong>Success.</strong>
  - Content-Type: `application/json`
- `401`
- `403`
- `422`
---
#### `GET /v1/apps/timeseries/unified_apps`

Fetch time series data for unified apps.

Retrieve session metrics data across a time series for Unified Apps. <br> <i>Note: An optional OS filter is available, but responses are aggregated by unified app.</i> <br><br> Supported metrics include:
  - time_spent (seconds)
  - total_time_spent (seconds)
  - session_duration (seconds)
  - session_count
  - total_session_count

**Parameters**:
- `start_date` (query, string, **required**): Start date in `YYYY-MM-DD` format. Data is available from 2021-01-01 onward.
- `end_date` (query, string, **required**): End date in `YYYY-MM-DD` format.
- `app_ids` (query, array, **required**): Unified app IDs, separated by commas (maximum 100).
- `timeseries` (query, array, **required**): Time series metrics, separated by commas.
- `regions` (query, array): Regions, separated by commas. All regions are included unless specified. <a target='_blank' href='/api/ios/usage/countries.json'>Region Codes</a>.

- `time_period` (query, string): Specifies the session metrics time period.<br> Returns averaged session metrics for each period within a month.<br> Example: "week" = average session metrics per week, averaged over all weeks in a month.

- `os` (query, string): Filter apps by platform.
- `breakdown` (query, string, **required**): Fields used for data aggregation, separated by commas.<br> The specified fields will be preserved in the response, while others will be aggregated.


**Responses**:
- `200`: <strong>Success.</strong>
  - Content-Type: `application/json`
- `401`
- `403`
- `422`
---

### USAGE: Engagement
#### `GET /v1/{os}/consumer_intel/engagement_insights`

Fetches app engagement trends.

Fetches the app engagement trends from a specific subset of panel users.

**Parameters**:
- `os` (path, string, **required**): Operating System
- `selection_cohort_ids` (query, array, **required**): IDs of selection cohorts, separated by commas. (Max: 5) <br> Can be queried with <a href="/api/docs/app_analysis#/USAGE%3A%20Engagement/engagement_insights_cohorts" target="_blank">
  Engagement Insights Cohorts
</a>

- `country` (query, string): Region to return results for (leave blank for Worldwide)
- `granularity` (query, string, **required**): Aggregate metrics by granularity
- `start_date` (query, string, **required**): Start Date, `YYYY-MM-DD` Format (minimum date: 2020-03-30)
- `end_date` (query, string, **required**): End Date, `YYYY-MM-DD` Format

**Responses**:
- `200`: <strong>Success.</strong>
  - Content-Type: `application/json`
    - Schema: `Unknown`
- `401`
- `403`
- `422`
---
#### `GET /v1/{os}/consumer_intel/engagement_insights/cohorts`

Fetches cohorts.

Fetches the available cohorts.

**Parameters**:
- `os` (path, string, **required**): Operating System

**Responses**:
- `200`: <strong>Success.</strong>
  - Content-Type: `application/json`
    - Schema: `object`
- `401`
- `403`
- `422`
---
#### `GET /v1/{os}/consumer_intel/time_of_day`

Fetches time of day data.

Fetches the time of day data from a specific subset of panel users. <br><br> The index of each number in <code>time_spent_hourly</code> maps to the hour of the day. For example, the 0th index is midnight and the 23rd index is 11pm.


**Parameters**:
- `os` (path, string, **required**): Operating System
- `selection_cohort_ids` (query, array, **required**): IDs of selection cohorts, separated by commas. (Max: 5) <br> Can be queried with <a href="/api/docs/app_analysis#/USAGE%3A%20Engagement/time_of_day_cohorts" target="_blank">
  Time Of Day Cohorts
</a>

- `country` (query, string): Country to return results for (leave blank for Worldwide)
- `granularity` (query, string, **required**): Retention by granularity

**Responses**:
- `200`: <strong>Success.</strong>
  - Content-Type: `application/json`
    - Schema: `object`
- `401`
- `403`
- `422`
---
#### `GET /v1/{os}/consumer_intel/time_of_day/cohorts`

Fetches cohorts.

Fetches the available cohorts.

**Parameters**:
- `os` (path, string, **required**): Operating System

**Responses**:
- `200`: <strong>Success.</strong>
  - Content-Type: `application/json`
    - Schema: `object`
- `401`
- `403`
- `422`
---
#### `GET /v1/{os}/consumer_intel/power_user_curve`

Fetches power user curve.

Fetches the power user curve from a specific subset of panel users.

**Parameters**:
- `os` (path, string, **required**): Operating System
- `selection_cohort_ids` (query, array, **required**): IDs of selection cohorts, separated by commas. (Max: 5) <br> Can be queried with <a href="/api/docs/app_analysis#/USAGE%3A%20Engagement/power_user_curve_cohorts" target="_blank">
  Power User Curve Cohorts
</a>

- `country` (query, string): Country to return results for (leave blank for Worldwide)
- `granularity` (query, string, **required**): Power User Curve by granularity
- `start_date` (query, string, **required**): Start Date, `YYYY-MM-DD` Format (minimum date: 2020-03-30)
- `end_date` (query, string, **required**): End Date, `YYYY-MM-DD` Format

**Responses**:
- `200`: <strong>Success.</strong>
  - Content-Type: `application/json`
    - Schema: `object`
- `401`
- `403`
- `422`
---
#### `GET /v1/{os}/consumer_intel/power_user_curve/cohorts`

Fetches cohorts.

Fetches the available cohorts.

**Parameters**:
- `os` (path, string, **required**): Operating System

**Responses**:
- `200`: <strong>Success.</strong>
  - Content-Type: `application/json`
    - Schema: `Unknown`
- `401`
- `403`
- `422`
---

### APP UPDATES: App Update Timeline
#### `GET /v1/{os}/app_update/get_app_update_history`

Fetches app update history.

Retrieve detailed app update history for a particular app, with information such as update version, summary, price, description, and screenshots. The app's information will also be returned in the response. <br><br> <strong>Note:</strong> Not all update information are available historically. See <a target='blank' href='/api/docs/static/app_update_type_start_dates.json'>
  App Update Type Start Dates
</a> for information on when the earliest update history is available for each update type.

**Parameters**:
- `os` (path, string, **required**): Operating System
- `app_id` (query, string, **required**): ID of App
- `country` (query, string): Specify the country you want update history for, <a target='_blank' href='/api/docs/static/country_ids.json'>
  Country Codes
</a> (defaults to "US")
- `date_limit` (query, string): Number of days from today to start the update timeline

**Responses**:
- `200`: <strong>Success.</strong>
- `401`
- `403`
- `422`
---
#### `GET /v1/{os}/apps/version_history`

Fetches the version history of a particular app.

Retrieve version history for a particular app, with update versions and release notes. The app's information will also be returned in the response.

**Parameters**:
- `os` (path, string, **required**): Operating System
- `app_id` (query, string, **required**): ID of of App
- `country` (query, string): Specify the country you want update history for,
<a target='_blank' href='/api/docs/static/country_ids.json'>Country Codes</a>
(defaults to "US")

**Responses**:
- `200`: <strong>Success.</strong>
- `401`
- `403`
- `422`
---

### CROSS APP USAGE: App Overlap
#### `GET /v1/unified/app_overlap`

Fetches app overlap for a specific app.

Retrieve apps which users of this app are more likely to use. <br><br> Description of Results <br> <table>
  <tr>
    <td>app_id</td>
    <td>App being compared (result app)</td>
  </tr>
  <tr>
    <td>app_a_users_likelihood_multiplier</td>
    <td>
      Requested app's users increased chance of use of result app.
    </td>
  </tr>
  <tr>
    <td>app_a_users_using_app_b_share</td>
    <td>Percentage of requested app users which also use result app</td>
  </tr>
  <tr>
    <td>app_a_users_using_app_b_share_previous_period</td>
    <td>Percentage of requested app users which also use result app in the previous period</td>
  </tr>
  <tr>
    <td>app_a_users_using_app_b_share_previous_period_diff</td>
    <td>Percentage of requested app users which also use result app – difference between the current period and the previous</td>
  </tr>
  <tr>
    <td>app_b_users_likelihood_multiplier</td>
    <td>
      Result app's users increased chance of use of requested app.
      <br>This field is only present if the `include_inverse_multiplier` parameter is set to `true`.  
    </td>
  </tr>
</table>

**Parameters**:
- `app_id` (query, string, **required**): The ID of the reference Unified App. If it belongs to an app that does not meet <a target='_blank' href='https://help.sensortower.com/hc/en-us/articles/6985667275675-What-is-a-Disabled-Small-App-in-Usage-Intelligence-'> minimum requirements for usage estimates</a>, an error will be returned.
- `countries[]` (query, array, **required**): Country to return results for. The allowed countries are the following: US, AU, CA, FR, DE, GB, IT, JP, KR, BR, IN,  ID, MY, SG, ES, TH, VN, CN, TW, HK, RU, TR, MX, PL, NL, PH, SA, AE. <br> Only single countries are supported at this time. Passing multiple countries in one request will cause an error.

- `start_date` (query, string, **required**): Start of the date range to query, `YYYY-MM-DD` Format. Must be the first day of the month.
- `end_date` (query, string, **required**): End of the date range to query, `YYYY-MM-DD` Format. Must be the last day of the month.
- `category` (query, string): Unified Category ID for the result apps.
<b>Omit this parameter to select all categories.</b>
- `include_inverse_multiplier` (query, boolean): Whether to include the inverse likelihood multiplier metric (result app's users increased chance of use of the requested app).
The metric is returned in the `app_a_users_likelihood_multiplier` field.
If this parameter is omitted, the field is not included in the response.

**Responses**:
- `200`: <strong>Success.</strong>
  - Content-Type: `application/json`
- `401`
- `403`
- `422`: <strong>Invalid Start Date.</strong> <br> The ID you requested belongs to an app which does not meet minimum requirements for usage estimates.
  - Content-Type: `application/json`
    - Schema: `object`
---

### CROSS APP USAGE: Cross App Usage
#### `GET /v1/{os}/consumer_intel/cohort_engagement`

Fetches app engagement trends.

Fetches the app engagement trends from a specific subset of panel users.

**Parameters**:
- `os` (path, string, **required**): Operating System
- `filter_cohort_id` (query, string, **required**): ID of the filter cohort. <br> Can be queried with <a href="/api/docs/app_analysis#/CROSS%20APP%20USAGE%3A%20Cross%20App%20Usage/cohort_engagement_cohorts" target="_blank"> Cohort Engagement Cohorts </a>
- `selection_cohort_ids` (query, array, **required**): IDs of selection cohorts, separated by commas. (Max: 5) <br> Can be queried with <a href="/api/docs/app_analysis#/CROSS%20APP%20USAGE%3A%20Cross%20App%20Usage/cohort_engagement_cohorts" target="_blank">
  Cohort Engagement Cohorts
</a>

- `country` (query, string): Region to return results for (leave blank for Worldwide)
- `granularity` (query, string, **required**): Aggregate metrics by granularity
- `start_date` (query, string, **required**): Start Date, `YYYY-MM-DD` Format (minimum date: 2020-03-30)
- `end_date` (query, string, **required**): End Date, `YYYY-MM-DD` Format

**Responses**:
- `200`: <strong>Success.</strong>
  - Content-Type: `application/json`
    - Schema: `object`
- `401`
- `403`
- `422`
---
#### `GET /v1/{os}/consumer_intel/cohort_engagement/cohorts`

Fetches cohorts.

Fetches the available cohorts.

**Parameters**:
- `os` (path, string, **required**): Operating System

**Responses**:
- `200`: <strong>Success.</strong>
  - Content-Type: `application/json`
    - Schema: `object`
- `401`
- `403`
- `422`
---



---

*Generated on 2025-07-21 21:03:47*