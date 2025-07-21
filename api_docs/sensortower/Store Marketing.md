# Store Intelligence. v1.0

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

### FEATURED: Featured Today
#### `GET /v1/ios/featured/today/stories`

Fetches featured today stories.

<p>Retrieve featured today story metadata, such as story title, label, style, and position, as well as the story's featured apps and relevant app metadata.</p> <p> <strong>Note:</strong> Non-App Intelligence users are limited the the last 3 days of featured today stories. App Intelligence users will be able to retrieve all-time featured today stories, including <strong>tomorrow's</strong> stories.</p>


**Parameters**:
- `country` (query, string): Country code for the featured today stories,
<a target='_blank' href='/api/docs/static/country_ids.json'>Country Codes</a>
- `start_date` (query, string): Start Date, `YYYY-MM-DD` (defaults to 3 days ago)
- `end_date` (query, string): End Date, `YYYY-MM-DD` (defaults to today)

**Responses**:
- `200`: <strong>Success.</strong>
- `401`
- `403`
- `422`
---

### FEATURED: Featured Apps and Games
#### `GET /v1/ios/featured/apps`

Fetches featured apps and games.

<p>Retrieve apps featured on the App Store&#39;s Apps &amp; Games pages.</p> <p><strong>Note:</strong> Non-App Intelligence users are limited the the last 3 days of data. App Intelligence users will be able to retrive all-time data.</p>


**Parameters**:
- `category` (query, string, **required**): Category ID,
<a target='_blank' href='/api/docs/static/featured_apps_category_ids.json'>Category IDs</a>
- `country` (query, string): Country code,
<a target='_blank' href='/api/docs/static/country_ids.json'>Country Codes</a>
- `start_date` (query, string): Start Date, `YYYY-MM-DD` (defaults to 3 days ago)
- `end_date` (query, string): End Date, `YYYY-MM-DD` (defaults to today)

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

### FEATURED: Featured App Rankings
#### `GET /v1/{os}/featured/creatives`

Fetches featured creatives details of a particular app.

Retrieve the featured creatives and their positions within the App and Google Play store over time. <br> <strong>Note:</strong> Some Feature Types are specific to the iOS App Store.


**Parameters**:
- `os` (path, string, **required**): Operating System
- `app_id` (query, string, **required**): ID of App
- `countries` (query, array): Countries to return results for, separated by commas
<br>
<a target='_blank' href='/api/docs/static/country_ids.json'>Country Codes</a>
- `types` (query, array): Types to return results for, separated by commas,
<a target='_blank' href='/api/docs/static/featured_rankings_types.json'>Types</a>
- `start_date` (query, string): Start Date, `YYYY-MM-DD` (defaults to 30 days ago)
- `end_date` (query, string): End Date, `YYYY-MM-DD` (defaults to today)

**Responses**:
- `200`: <strong>Success.</strong>
  - Content-Type: `application/json`
    - Schema: `object`
- `401`
- `403`
- `422`
---
#### `GET /v1/{os}/featured/impacts`

Fetches occurrence and download-impact data for an app.

Retrieve the occurrence and download-impact data for an apps featured in the App or Google Play Store. <br> <strong>Note:</strong> Some Feature Types are specific to the iOS App Store.


**Parameters**:
- `os` (path, string, **required**): Operating System
- `app_id` (query, string, **required**): ID of App
- `countries` (query, array): Countries to return results for, separated by commas
<br>
<a target='_blank' href='/api/docs/static/country_ids.json'>Country Codes</a>
- `types` (query, array): Types to return results for, separated by commas,
<a target='_blank' href='/api/docs/static/featured_rankings_types.json'>Types</a>
- `breakdown` (query, string): Breakdown type for the featured today stories
- `start_date` (query, string): Start Date, `YYYY-MM-DD` (defaults to 30 days ago)
- `end_date` (query, string): End Date, `YYYY-MM-DD` (defaults to today)

**Responses**:
- `200`: <strong>Success.</strong>
- `401`
- `403`
- `422`
---

### APP STORE OPTIMIZATION: User Apps
#### `GET /v1/ios/ajax/user_apps`

Fetches apps that you manage.

Retrieve detailed information on the iOS <b>and</b> Android apps that you own or currently have access to.

**Responses**:
- `200`: <strong>Success.</strong>
- `401`
- `403`
---

### APP STORE OPTIMIZATION: Keyword Rankings
#### `GET /v1/{os}/keywords/keywords`

Fetches currently tracked keywords of a particular app that you manage.

Retrieve a summary of the keywords that you are currently tracking for a particular app that you follow in your Sensor Tower account. Information includes keyword traffic, ranking difficulty, trend, current rank, and density.<br><br> Density is a tuple consisting of: term density (%), term frequency (integer), and total number of non-filler words (integer) <br><br> Rank is 1-indexed.

**Parameters**:
- `os` (path, string, **required**): Operating System
- `user_app_id` (query, string, **required**): ID of your User App (this is not the `app_id`). Use the <a target='_blank' href='#/APP%20STORE%20OPTIMIZATION%3A%20User%20Apps/user_apps'>User App API</a> to get a list of your User App IDs
- `country` (query, string, **required**): Country code for the keywords, <a target='_blank' href='/api/docs/static/country_ids.json'>Country Codes</a>
- `device` (query, string, **required**): On iOS, use "phone", or "tablet". For Android, use "phone".

**Responses**:
- `200`: <strong>Success.</strong>
- `401`
- `403`
- `422`
---
#### `GET /v1/{os}/keywords/get_current_keywords`

Fetches keyword list of a particular app.

Retrieve a list of filtered and unfiltered keywords for any app on the
Google Play / App Store.
<br><br>
<strong>Note:</strong> While we don't set a hard limit, a subscription
must be purchased for the continued use of this API.

**Parameters**:
- `os` (path, string, **required**): Operating System
- `app_id` (query, string, **required**): ID of App
- `country` (query, string): Country code for the keywords,
<a target='_blank' href='/api/docs/static/country_ids.json'>Country Codes</a>

**Responses**:
- `200`: <strong>Success.</strong>
- `401`
- `403`
- `422`
---

### APP STORE OPTIMIZATION: Keyword Overview
#### `GET /v1/{os}/keywords/overview/history`

Fetches overall ranking of an app against a list of keywords.

Retrieve a historical summary of the keywords that you are currently tracking for a particular app that you follow in your Sensor Tower account. Information includes keyword traffic, ranking difficulty, trend, and current rank. Rank is 1-indexed.

**Parameters**:
- `os` (path, string, **required**): Operating System
- `user_app_id` (query, string, **required**): ID of your User App (this is not the `app_id`). Use the <a target='_blank' href='#/APP%20STORE%20OPTIMIZATION%3A%20User%20Apps/user_apps'>User App API</a> to get a list of your User App IDs
- `country` (query, string, **required**): Country code for the keywords,
<a target='_blank' href='/api/docs/static/country_ids.json'>Country Codes</a>
- `start_date` (query, string): Start Date, `YYYY-MM-DD` (defaults to 30 days ago)
- `end_date` (query, string): End Date, `YYYY-MM-DD` (defaults to today)
- `device` (query, string, **required**): On iOS, use "phone", or "tablet". For Android, use "phone".
- `date_granularity` (query, string): Aggregate counts of Keyword Rankings (use "daily", or "weekly")
- `traffic_score` (query, integer): Optional floor of traffic scores to query. "0" or empty, means "all".

**Responses**:
- `200`: <strong>Success.</strong>
- `401`
- `403`
- `422`
---

### APP STORE OPTIMIZATION: Keyword Downloads
#### `GET /v1/{os}/keywords/downloads/history`

Fetches download estimates for various search terms.

Retrieve estimates of the downloads that an app earned from user searches for specific keywords. You must follow the app in your Sensor Tower account, and provide the country and device. Estimates are at a weekly or monthly granularity and go back to January 1, 2020. You may optionally include estimates for keywords that you do not currently track.

**Parameters**:
- `os` (path, string, **required**): Operating System
- `user_app_id` (query, string, **required**): ID of your User App (this is not the `app_id`). Use the <a target='_blank' href='#/APP%20STORE%20OPTIMIZATION%3A%20User%20Apps/user_apps'>User App API</a> to get a list of your User App IDs
- `country` (query, string, **required**): Country code for the keywords,
<a target='_blank' href='/api/docs/static/country_ids.json'>Country Codes</a>
- `start_date` (query, string): Start Date, `YYYY-MM-DD` (defaults to 30 days ago)
- `end_date` (query, string): End Date, `YYYY-MM-DD` (defaults to today)
- `device` (query, string, **required**): On iOS, use "phone", or "tablet". For Android, use "phone".
- `date_granularity` (query, string, **required**): Aggregate counts of Keyword Download estimates (use "weekly", or "monthly")
- `display_untracked_keywords` (query, boolean): Optionally include top untracked Keywords.

**Responses**:
- `200`: <strong>Success.</strong>
- `401`
- `403`
- `422`
---

### APP STORE OPTIMIZATION: Keyword Research
#### `GET /v1/{os}/keywords/research_keyword`

Fetches detailed summary of a particular keyword.

Retrieve detailed information for any keyword, such as related search terms, traffic data, and ranking difficulty, along with a list of apps that are currently ranking for that keyword.

**Parameters**:
- `os` (path, string, **required**): Operating System
- `app_id` (query, integer): App ID for Keyword Ranking Prediction <span style='color: #ff0000'>(iOS only)</span>
- `term` (query, string, **required**): Term to research
- `country` (query, string, **required**): Country code for the keywords,
<a target='_blank' href='/api/docs/static/country_ids.json'>Country Codes</a>
- `page` (query, integer): Offset the top ranking apps by 25 for each Page Index

**Responses**:
- `200`: <strong>Success.</strong>
- `401`
- `403`
- `422`
---
#### `GET /v1/ios/keywords/search_suggestions`

Fetches iOS search suggestions of a particular keyword.

Retrieve a list of search suggestion for any iOS keyword.

**Parameters**:
- `term` (query, string, **required**): Term to research
- `country` (query, string, **required**): Country code for the keywords,
<a target='_blank' href='/api/docs/static/country_ids.json'>Country Codes</a>

**Responses**:
- `200`: <strong>Success.</strong>
- `401`
- `403`
- `422`
---
#### `GET /v1/ios/keywords/trending_searches`

Fetches current trending search terms.

Retrieve a list currently trending search terms on the iOS App Store.

**Parameters**:
- `country` (query, string): Country code for trending searches, <a target='_blank' href='/api/docs/static/country_ids.json'>Country Codes</a>
- `device` (query, string): Use "iphone" or "ipad", defaults to "iphone"
- `date` (query, string): Date, `YYYY-MM-DD` Format, defaults to today

**Responses**:
- `200`: <strong>Success.</strong>
- `401`
- `403`
- `422`
---

### APP STORE OPTIMIZATION: Traffic Score
#### `GET /v1/{os}/keywords/traffic`

Fetches current keyword traffic scores.

Retrieve a list of traffic scores for up to 500 keywords for up to 25 countries. <br> <strong>Note:</strong> Some keywords may not have a traffic score for each requested country. In such cases, the country key will be omitted in the response.


**Parameters**:
- `os` (path, string, **required**): Operating System
- `countries` (query, array, **required**): Requested countries, separated by commas. <br> <b>Max: 25</b> <a target='_blank' href='/api/docs/static/country_ids.json'>Country Codes</a><br>

- `terms` (query, array, **required**): List of keywords to scan per country, separated by commas. <br> <b>Max: 500</b>


**Responses**:
- `200`: <strong>Success.</strong>
- `401`
- `403`
- `422`
---
#### `GET /v1/{os}/keywords/traffic_history`

Fetches historical keyword traffic scores.

Retrieve a list of historical traffic scores for up to 25 keyword/terms for up to 10 countries. <br> <strong>Note:</strong> Traffic scores go back to Jan 1st 2018.

**Parameters**:
- `os` (path, string, **required**): Operating System
- `start_date` (query, string, **required**): Start Date, `YYYY-MM-DD` Format
- `end_date` (query, string, **required**): End Date, `YYYY-MM-DD` Format
- `countries` (query, array, **required**): Countries to return results for, separated by commas
<br>
<a target='_blank' href='/api/docs/static/country_ids.json'>Country Codes</a><br>
<b>Max: 10</b>
- `date_granularity` (query, string, **required**): Aggregate traffic scores (use "weekly", "monthly")
- `terms` (query, array, **required**): List of keywords to scan per country, separated by commas. <br><b>Max: 25</b>

**Responses**:
- `200`: <strong>Success.</strong>
- `401`
- `403`
- `422`
---

### RATINGS & REVIEWS: Review Analysis and History
#### `GET /v1/{os}/review/get_reviews`

Fetches detailed reviews information for a particular app.

Retrieve user reviews with information such as the review's content, rating, username, app id, version, date, tags, and more.

**Parameters**:
- `os` (path, string, **required**): Operating System
- `app_id` (query, string, **required**): Filter reviews by the App ID i.e. 529479190 (iOS) or com.facebook.katana (Android)
- `start_date` (query, string): Start Date, `YYYY-MM-DD` format
- `end_date` (query, string): End Date, `YYYY-MM-DD` format
- `country` (query, string, **required**): Country code for the reviews, <a target='_blank' href='/api/docs/static/country_ids.json'>Country Codes</a>
- `rating_filter` (query, String / Integer): Filter reviews by the ratings given by the user, "positive" "negative", or 1-5  (e.g. 4)
- `search_term` (query, string): Filter reviews by content (e.g. "love the app!")
- `username` (query, string): Filter reviews by the username of the reviewer
- `limit` (query, integer): Limit how many reviews per call (maximum: 200)
- `page` (query, integer): Offset reviews by the limit for each page, valid values are >= 1

**Responses**:
- `200`: <strong>Success.</strong>
- `401`
- `403`
- `422`
---

### RATINGS & REVIEWS: Review Breakdown
#### `GET /v1/{os}/review/app_history_summary`

Fetches summary of positive and negative review counts by day.

Retrieve a summary of positive and or negative reviews of a particular app by each day, along with the app's version update information.

**Parameters**:
- `os` (path, string, **required**): Operating System
- `app_id` (query, string, **required**): Filter reviews by the App ID
- `start_date` (query, string): Start Date, `YYYY-MM-DD` format
- `end_date` (query, string): End Date, `YYYY-MM-DD` format
- `country` (query, string): Country code for the reviews, <a target='_blank' href='/api/docs/static/country_ids.json'>Country Codes</a> (defaults to US)
- `rating_filter` (query, String / Integer): Filter reviews by the ratings given by the user, "positive" "negative", or 1-5  (e.g. 4)

**Responses**:
- `200`: <strong>Success.</strong>
- `401`
- `403`
- `422`
---

### RATINGS & REVIEWS: Rating Analysis
#### `GET /v1/{os}/review/get_ratings`

Fetches rating count breakdown of a particular app.

Retrieve historical rating count summary for a particular app, ordered by descending date. If the start date and end date parameters are both left blank, this will return a 0 or 1 length array containing the most recent Rating Count Breakdown for the specified app. <br><br> The returned <code>breakdown</code> is the total cumulative ratings for the lifetime and current version (if applicable) of the app sorted from 1 star to 5 stars. The returned <code>average</code> and <code>total</code> values are of the lifetime breakdowns. <br><br> <strong>Note:</strong> Rating count breakdowns may not be available every day for every app. <br><br> <strong>Deprecation:</strong> <code>current_version_breakdown</code> parameter is deprecated and currently returns the same data as in <code>breakdown</code>.

**Parameters**:
- `os` (path, string, **required**): Operating System
- `app_id` (query, string, **required**): Filter ratings by the App ID i.e. 284882215 (iOS) or com.facebook.katana (Android)
- `start_date` (query, string): Start Date, `YYYY-MM-DD` format
- `end_date` (query, string): End Date, `YYYY-MM-DD` format
- `country` (query, string): Country code for the ratings, <a target='_blank' href='/api/docs/static/country_ids.json'>Country Codes</a>

**Responses**:
- `200`: <strong>Success.</strong>
- `401`
- `403`
- `422`
---

### SEARCH ADS: Apple Search Ads
#### `GET /v1/ios/search_ads/apps`

Fetches search ad apps of a particular keyword.

Retrieve a list of apps that have Search Ads for the given keyword,
along with its current share of voice for that keyword.

**Parameters**:
- `term` (query, string, **required**): Keyword to lookup
- `country` (query, string, **required**): Country code for the keywords,
<a target='_blank' href='/api/docs/static/country_ids.json'>Country Codes</a>

**Responses**:
- `200`: <strong>Success.</strong>
- `401`
- `403`
- `422`
---
#### `GET /v1/ios/search_ads/terms`

Fetches search ad keywords of a particular app.

Retrieve a list of keywords that the given app has Search Ads for,
along with its share of voice for the selected date range, number of competitors
for the same keyword, and information on the keyword's top competitors

**Parameters**:
- `app_id` (query, string, **required**): ID of App
- `country` (query, string, **required**): Country code for the keywords,
<a target='_blank' href='/api/docs/static/country_ids.json'>Country Codes</a>
- `start_date` (query, string, **required**): Start Date, `YYYY-MM-DD` Format
- `end_date` (query, string, **required**): End Date, `YYYY-MM-DD` Format

**Responses**:
- `200`: <strong>Success.</strong>
- `401`
- `403`
- `422`
---
#### `GET /v1/ios/search_ads/history`

Fetches historical search ads share of voice for the particular apps and term.

Retrieve historical share of voice information for the given apps and term, broken down by date.

**Parameters**:
- `app_id` (query, string, **required**): ID of App
- `term` (query, string, **required**): Keyword to lookup
- `country` (query, string, **required**): Country code for the history,
<a target='_blank' href='/api/docs/static/country_ids.json'>Country Codes</a>
- `start_date` (query, string, **required**): Start Date, `YYYY-MM-DD` Format
- `end_date` (query, string, **required**): End Date, `YYYY-MM-DD` Format

**Responses**:
- `200`: <strong>Success.</strong>
- `401`
- `403`
- `422`
---



---

*Generated on 2025-07-21 21:03:46*