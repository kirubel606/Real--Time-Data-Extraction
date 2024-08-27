import requests
import sqlite3

# Fetch data from KoboToolbox API
url = "https://kf.kobotoolbox.org/api/v2/assets/aW9w8jHjn4Cj8SSQ5VcojK/data.json"
payload = ""
headers = {
    'Authorization': 'Token f24b97a52f76779e97b0c10f80406af5e9590eaf',
    'Cookie': 'django_language=en'
}

response = requests.get(url, headers=headers, data=payload)
data = response.json()

# Step 1: Connect to SQLite database (or create it)
conn = sqlite3.connect('kobodata.db')

# Step 2: Create a cursor object to execute SQL commands
cur = conn.cursor()

# Step 3: Create tables if they don't exist
cur.execute('''
CREATE TABLE IF NOT EXISTS submissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    submission_id INTEGER UNIQUE,
    form_uuid TEXT,
    submission_time TEXT,
    status TEXT,
    instance_id TEXT,
    xform_id_string TEXT
);
''')

cur.execute('''
CREATE TABLE IF NOT EXISTS clients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    submission_id INTEGER,
    client_name TEXT,
    client_id_manifest TEXT,
    location TEXT,
    phone TEXT,
    alt_phone TEXT,
    phone_smart_feature TEXT,
    gender TEXT,
    age INTEGER,
    nationality TEXT,
    strata TEXT,
    disability TEXT,
    education TEXT,
    client_status TEXT,
    sole_income_earner TEXT,
    howrespble_pple INTEGER,
    FOREIGN KEY (submission_id) REFERENCES submissions(submission_id)
);
''')

cur.execute('''
CREATE TABLE IF NOT EXISTS business (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    submission_id INTEGER,
    cohort TEXT,
    program TEXT,
    biz_status TEXT,
    biz_operating TEXT,
    FOREIGN KEY (submission_id) REFERENCES submissions(submission_id)
);
''')

cur.execute('''
CREATE TABLE IF NOT EXISTS surveys (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    submission_id INTEGER,
    survey_date TEXT,
    biz_country_name TEXT,
    biz_region_name TEXT,
    start_time TEXT,
    end_time TEXT,
    FOREIGN KEY (submission_id) REFERENCES submissions(submission_id)
);
''')

# Step 4: Loop over the results and insert data into tables
for result in data['results']:
    # Insert into submissions table
    cur.execute('''
        INSERT OR IGNORE INTO submissions (submission_id, form_uuid, submission_time, status, instance_id, xform_id_string)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        result['_id'], 
        result.get('formhub/uuid'), 
        result.get('_submission_time'), 
        result.get('_status'), 
        result.get('meta/instanceID'), 
        result.get('_xform_id_string')
    ))

    # Insert into clients table
    cur.execute('''
        INSERT INTO clients (submission_id, client_name, client_id_manifest, location, phone, alt_phone, phone_smart_feature, gender, age, nationality, strata, disability, education, client_status, sole_income_earner, howrespble_pple)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        result['_id'],
        result.get('sec_c/cd_client_name'),
        result.get('sec_c/cd_client_id_manifest'),
        result.get('sec_c/cd_location'),
        result.get('sec_c/cd_clients_phone'),
        result.get('sec_c/cd_phoneno_alt_number'),
        result.get('sec_c/cd_clients_phone_smart_feature'),
        result.get('sec_c/cd_gender'),
        result.get('sec_c/cd_age'),
        result.get('sec_c/cd_nationality'),
        result.get('sec_c/cd_strata'),
        result.get('sec_c/cd_disability'),
        result.get('sec_c/cd_education'),
        result.get('sec_c/cd_client_status'),
        result.get('sec_c/cd_sole_income_earner'),
        result.get('sec_c/cd_howrespble_pple')
    ))

    # Insert into business table
    cur.execute('''
        INSERT INTO business (submission_id, cohort, program, biz_status, biz_operating)
        VALUES (?, ?, ?, ?, ?)
    ''', (
        result['_id'],
        result.get('sec_b/cd_cohort'),
        result.get('sec_b/cd_program'),
        result.get('group_mx5fl16/cd_biz_status'),
        result.get('group_mx5fl16/bd_biz_operating')
    ))

    # Insert into surveys table
    cur.execute('''
        INSERT INTO surveys (submission_id, survey_date, biz_country_name, biz_region_name, start_time, end_time)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        result['_id'],
        result.get('cd_survey_date'),
        result.get('sec_a/cd_biz_country_name'),
        result.get('sec_a/cd_biz_region_name'),
        result.get('starttime'),
        result.get('endtime')
    ))

# Commit the changes
conn.commit()

# Step 5: Query the database to verify data insertion
cur.execute('SELECT * FROM clients')
rows = cur.fetchall()

# Print the results
for row in rows:
    print(row)

# Step 6: Close the connection
conn.close()
