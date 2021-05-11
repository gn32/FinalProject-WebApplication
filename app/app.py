from __future__ import print_function
from __future__ import print_function
import datetime
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from typing import List, Dict
import simplejson as json
from flask import Flask, request, Response, redirect,json, jsonify
from flask import render_template
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor
from google_auth_oauthlib.flow import InstalledAppFlow
import json


app = Flask(__name__)
mysql = MySQL(cursorclass=DictCursor)



app.config['MYSQL_DATABASE_HOST'] = 'db'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_DB'] = 'records'
mysql.init_app(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about/')
def about():
    return render_template('about.html')

@app.route('/academics/')
def academics():
    return render_template('academics.html')


@app.route('/gallery/')
def gallery():
    return render_template('gallery.html')

@app.route('/calendar/')
def calendar():
    return render_template('calendar.html')

@app.route('/covid/')
def covid():
    return render_template('covid.html')


@app.route('/Faculty/')
def Faculty():
    return render_template('Faculty.html')

@app.route('/records/', methods=['GET'])
def course():
    user = {'username': 'Rutgers'}
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblrecords')
    result = cursor.fetchall()
    return render_template('records.html', title='Home', user=user, records=result)

@app.route('/chart/')
def chart():
    legend = "Student Age Ratio"
    labels = list()
    values = list()
    cursor = mysql.get_db().cursor()
    #labels = [1,2,3,4,5,6]
    #values = [41, 30, 39, 30, 26, 30]

    cursor.execute('SELECT * from tblrecords')
    result1 = cursor.fetchall()
    for i in result1:
        labels.append(i['Name'])
        values.append(i['Age'])

    print(labels)
    print(values)
    return render_template('chart.html', values=values, labels=labels, legend=legend)

@app.route('/view/<int:record_id>', methods=['GET'])
def view(record_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblrecords WHERE id=%s', record_id)
    result = cursor.fetchall()
    return render_template('view.html', title='View Form', record=result[0])


@app.route('/edit/<int:record_id>', methods=['GET'])
def form_edit_get(record_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblrecords WHERE id=%s', record_id)
    result = cursor.fetchall()
    return render_template('edit.html', title='Edit Form', record=result[0])


@app.route('/edit/<int:record_id>', methods=['POST'])
def form_update_post(record_id):
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('Name'), request.form.get('Sex'),
                 request.form.get('Age'),request.form.get('Height_in'),
                 request.form.get('Weight_lbs'), record_id)
    sql_update_query = """UPDATE tblrecords t SET t.Name = %s, t.Sex = %s,
     t.Age = %s, t.Height_in = %s, t.Weight_lbs = %s 
     WHERE t.id = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    return redirect("/records/", code=302)


@app.route('/records/new', methods=['GET'])
def form_insert_get():
    return render_template('new.html', title='New Course Form')


@app.route('/records/new', methods=['POST'])
def form_insert_post():
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('Name'), request.form.get('Sex'),
                 request.form.get('Age'), request.form.get('Height_in'),
                 request.form.get('Weight_lbs'))

    sql_insert_query = """INSERT INTO tblrecords 
    (Name,Sex,Age,Height_in,Weight_lbs) 
    VALUES (%s, %s,%s,%s, %s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    return redirect("/records/", code=302)


@app.route('/delete/<int:record_id>', methods=['POST'])
def form_delete_post(record_id):
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM tblrecords WHERE id = %s """
    cursor.execute(sql_delete_query, record_id)
    mysql.get_db().commit()
    return redirect("/records/", code=302)


@app.route('/api/v1/records', methods=['GET'])
def api_browse() -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblrecords')
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/records/<int:record_id>', methods=['GET'])
def api_retrieve(record_id) -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblrecords WHERE id=%s', record_id)
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/records', methods=['POST'])
def api_add() -> str:
    content = request.json

    cursor = mysql.get_db().cursor()
    inputData = (content['Name'], content['Age'],
                 content['Sex'], content ['Height_in'],
                 content['Weight_lbs'])


    sql_insert_query = """INSERT INTO tblrecords
        (Name,Age,Sex,Height_in,Weight_lbs) 
        VALUES (%s, %s,%s, %s, %s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    resp = Response(status=201, mimetype='application/json')
    return resp


@app.route('/api/v1/records/<int:record_id>', methods=['PUT'])
def api_edit(record_id) -> str:
    cursor = mysql.get_db().cursor()
    content = request.json
    inputData = (content['Name'], content['Sex'], content['Age'],  content ['Height_in'],
                 content['Weight_lbs']
                 , record_id)
    sql_update_query = """UPDATE tblrecords t SET t.Name = %s, 
    t.Sex = %s, t.Age = %s,t.Height_in = %s, t.Weight_lbs = %s 
         WHERE t.id = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    resp = Response(status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/records/<int:record_id>', methods=['DELETE'])
def api_delete(record_id) -> str:
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM tblrecords WHERE id = %s """
    cursor.execute(sql_delete_query, record_id)
    mysql.get_db().commit()
    resp = Response(status=200, mimetype='application/json')
    return resp



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

    # If modifying these scopes, delete the file token.json.
    SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

    def main():
        """Shows basic usage of the Google Calendar API.
        Prints the start and name of the next 10 events on the user's calendar.
        """
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        service = build('calendar', 'v3', credentials=creds)

        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        print('Getting the upcoming 10 events')
        events_result = service.events().list(calendarId='primary', timeMin=now,
                                              maxResults=10, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])

    if __name__ == '__main__':
        main()