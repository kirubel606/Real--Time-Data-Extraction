
# Documentation

## Project Overview

This project involves extracting data from KoboToolbox and saving it into a SQLite database using a Python script (`fetch.py`). A Flask application (`app.py`) is used to receive real-time data via POST requests and trigger the data extraction process. The project includes error handling, logging, and basic validation.

## Setup

### 1. Prerequisites

- **Python**: Ensure you have Python 3.7 or higher installed.
- **Dependencies**: Install the required Python packages. You can do this using `pip`:
  ```bash
  pip install requests flask
  ```

### 2. Configuration

- **API Token**: Update the `Authorization` header in `fetch.py` with your KoboToolbox API token.
- **Database**: The SQLite database file `kobodata.db` will be created automatically.

### 3. File Structure

- **`fetch.py`**: A script that fetches data from KoboToolbox, processes it, and inserts it into an SQLite database.
- **`app.py`**: A Flask application with an endpoint to receive real-time data and trigger the `fetch.py` script.
- **`app.log`**: Log file for Flask application errors and activities.
- **`fetch.log`**: Log file for `fetch.py` script errors and activities.

## Usage

### Running the Fetch Script

To manually fetch and insert data into the database, execute:
```bash
python fetch.py
```

### Running the Flask Application

Start the Flask application with:
```bash
python app.py
```
The Flask app will be available at `http://127.0.0.1:5000`.

Hosted Endpoint that has been registered `https://dbede9a9-b3d5-46ac-a0a2-fc96c1b4f533-00-hminyejwck5p.janeway.replit.dev:3001/api`

### API Endpoints

- **POST /api**: Receives JSON data and inserts it into the database.
  - **Request Body**:
    ```json
    {
      "_id": "submission_id",
      "_submission_time": "submission_time",
      "_status": "status",
      "meta/instanceID": "instance_id",
      "_xform_id_string": "xform_id_string",
      "formhub/uuid": "form_uuid"  // Optional
    }
    ```
  - **Response**:
    - `200 OK` if data is successfully saved.
    - `400 Bad Request` if required fields are missing.
    - `500 Internal Server Error` for database or server errors.

- **GET /api/fetch**: Triggers the `fetch.py` script to update the database with the latest data from KoboToolbox.

## Database Schema

### `submissions`

- **id**: `INTEGER PRIMARY KEY AUTOINCREMENT`
- **submission_id**: `INTEGER UNIQUE`
- **form_uuid**: `TEXT`
- **submission_time**: `TEXT`
- **status**: `TEXT`
- **instance_id**: `TEXT`
- **xform_id_string**: `TEXT`

### `clients`

- **id**: `INTEGER PRIMARY KEY AUTOINCREMENT`
- **submission_id**: `INTEGER`
- **client_name**: `TEXT`
- **client_id_manifest**: `TEXT`
- **location**: `TEXT`
- **phone**: `TEXT`
- **alt_phone**: `TEXT`
- **phone_smart_feature**: `TEXT`
- **gender**: `TEXT`
- **age**: `INTEGER`
- **nationality**: `TEXT`
- **strata**: `TEXT`
- **disability**: `TEXT`
- **education**: `TEXT`
- **client_status**: `TEXT`
- **sole_income_earner**: `TEXT`
- **howrespble_pple**: `INTEGER`
- **FOREIGN KEY (submission_id)**: References `submissions(submission_id)`

### `business`

- **id**: `INTEGER PRIMARY KEY AUTOINCREMENT`
- **submission_id**: `INTEGER`
- **cohort**: `TEXT`
- **program**: `TEXT`
- **biz_status**: `TEXT`
- **biz_operating**: `TEXT`
- **FOREIGN KEY (submission_id)**: References `submissions(submission_id)`

### `surveys`

- **id**: `INTEGER PRIMARY KEY AUTOINCREMENT`
- **submission_id**: `INTEGER`
- **survey_date**: `TEXT`
- **biz_country_name**: `TEXT`
- **biz_region_name**: `TEXT`
- **start_time**: `TEXT`
- **end_time**: `TEXT`
- **FOREIGN KEY (submission_id)**: References `submissions(submission_id)`

## Assumptions

1. **Data Format**: The data received from KoboToolbox is in JSON format with the expected field names. Adjustments are required if the data structure changes.
2. **Database Integrity**: The SQLite database is used for simplicity and is assumed to be sufficient for the expected volume of data.
3. **Error Handling**: The script and application are designed to handle common errors but might need adjustments for specific edge cases or additional requirements.


## Conclusion

This documentation provides a comprehensive overview of setting up and using the project, including the database schema and assumptions. If any changes occur in the KoboToolbox data structure or additional features are required, updates to the code and documentation may be necessary.

--- 
