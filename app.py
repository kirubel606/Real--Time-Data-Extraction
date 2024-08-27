from flask import Flask, request, jsonify
import sqlite3
import logging
import subprocess
import sys

app = Flask(__name__)

# Set up logging
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

# Connect to SQLite database
def get_db_connection():
    try:
        conn = sqlite3.connect('kobodata.db')
        return conn
    except sqlite3.Error as e:
        logging.error(f"Database connection error: {str(e)}")
        raise

# Define the POST endpoint to receive data
@app.route('/api', methods=['POST'])
def receive_data():
    if not request.json:
        logging.error("No JSON data received")
        return jsonify({"error": "Invalid data format. JSON required."}), 400

    try:
        # Get the JSON data from the POST request
        data = request.json
        
        # Basic validation: Ensure required fields are present
        required_fields = ['_id', '_submission_time', '_status', 'meta/instanceID', '_xform_id_string']
        for field in required_fields:
            if field not in data:
                logging.error(f"Missing field: {field}")
                return jsonify({"error": f"Missing field: {field}"}), 400

        # Save the data to the SQLite database
        conn = get_db_connection()
        cur = conn.cursor()

        # Insert into submissions table
        cur.execute('''
            INSERT OR IGNORE INTO submissions (submission_id, form_uuid, submission_time, status, instance_id, xform_id_string)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            data['_id'],  # submission_id
            data.get('formhub/uuid'),  # form_uuid
            data['_submission_time'],  # submission_time
            data['_status'],  # status
            data['meta/instanceID'],  # instance_id
            data['_xform_id_string']  # xform_id_string
        ))

        # Commit the changes and close the connection
        conn.commit()
        conn.close()

        # Log success
        logging.info(f"Data saved successfully for submission_id: {data['_id']}")
        return jsonify({"message": "Data saved successfully"}), 200

    except sqlite3.Error as e:
        logging.error(f"Database error: {str(e)}")
        return jsonify({"error": "Database error occurred"}), 500


    except Exception as e:
        logging.error(f"Error saving data: {str(e)}", exc_info=True)  # Log full stack trace
        return jsonify({"error": "An error occurred"}), 500

def run_fetch():
    """Run fetch.py to update data"""
    try:
        result = subprocess.run([sys.executable, 'fetch.py'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        logging.info(f"fetch.py output: {result.stdout.decode()}")
    except subprocess.CalledProcessError as e:
        logging.error(f"fetch.py failed: {e.stderr.decode()}")


if __name__ == '__main__':
    run_fetch()
    app.run(debug=True)
