import datetime
import os

from flask import Flask, render_template, request
from google.cloud import datastore
from google.cloud.datastore import query
from google.cloud.datastore.query import Query

from google.auth.transport import requests
import google.oauth2.id_token

datastore_client = datastore.Client()

app = Flask(__name__)

firebase_request_adapter = requests.Request()


def get_required_env_var(varname, default=None):
    env_value = os.getenv(varname, default)
    if env_value is None:
        raise Exception(f"Required env var {varname} is not defined. Aborting!")
    return env_value


DATASTORE_KIND = "schedulemanager_usershift"
ICS_FILES_BUCKET = get_required_env_var("ICS_FILES_BUCKET")
ICS_PATH_PREFIX = get_required_env_var("ICS_PATH_PREFIX")


@app.route("/")
def root():
    # Verify Firebase auth.
    id_token = request.cookies.get("token")
    error_message = None
    claims = None
    times = None
    shift_datehours = None

    if id_token:
        try:
            # Verify the token against the Firebase Auth API. This example
            # verifies the token on each page load. For improved performance,
            # some applications may wish to cache results in an encrypted
            # session store (see for instance
            # http://flask.pocoo.org/docs/1.0/quickstart/#sessions).
            claims = google.oauth2.id_token.verify_firebase_token(
                id_token, firebase_request_adapter
            )
            store_time(claims["email"], datetime.datetime.now(tz=datetime.timezone.utc))
            times = fetch_visit_times(claims["email"], 10)
            # TODO: log with email truncated
            usershift_record = fetch_shifts(claims["email"])
            shift_datehours = usershift_record["shifts"]
            ics_files = usershift_record["ics"]
            ics_fullpaths = [
                f"https://storage.googleapis.com/{ICS_FILES_BUCKET}/{ICS_PATH_PREFIX}{ics_filename}"
                for ics_filename in ics_files
            ]
            shifts_with_ics = zip(shift_datehours, ics_fullpaths)
        except ValueError as exc:
            # This will be raised if the token is expired or any other
            # verification checks fail.
            # TODO: do sth when token expired
            error_message = str(exc)

    return render_template(
        "index.html",
        user_data=claims,
        error_message=error_message,
        shifts=shifts_with_ics,
    )


def store_time(email, dt):
    entity = datastore.Entity(key=datastore_client.key("User", email, "visit"))
    entity.update({"timestamp": dt})
    datastore_client.put(entity)


def fetch_visit_times(email, limit):
    ancestor = datastore_client.key("User", email)
    query = datastore_client.query(kind="visit", ancestor=ancestor)
    query.order = ["-timestamp"]
    times = query.fetch(limit=limit)
    return times


def get_current_schedule_identifier():
    # TODO: make decision whether it should be dynamic current month or last from datastore index
    return "202303"


def fetch_shifts(email):
    schedule_id = get_current_schedule_identifier()
    email_scheduleid_key = datastore_client.key(
        DATASTORE_KIND, f"{email}_{schedule_id}"
    )
    # query = datastore_client.query(kind=DATASTORE_KIND)
    # query.order = ["-timestamp"]
    # query = query.add_filter("email", "=", email)
    shifts_record = datastore_client.get(email_scheduleid_key)
    print(email_scheduleid_key)
    # query.key_filter(email_scheduleid_key, "=")
    # records = query.fetch(limit=limit)
    return shifts_record


if __name__ == "__main__":
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host="127.0.0.1", port=8080, debug=True)

