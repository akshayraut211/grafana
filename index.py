#! /usr/local/bin/python
# -*- coding: utf-8 -*-
from git import *
from calendar import timegm
from datetime import datetime
import _strptime  # https://bugs.python.org/issue7980
from flask import Flask, request, jsonify
app = Flask(__name__)

app.debug = True


def convert_to_time_ms(timestamp):
    return 1000 * timegm(datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%fZ').timetuple())


@app.route('/')
def health_check():
    return 'This datasource is healthy.'


@app.route('/search', methods=['POST'])
def search():
    data= ["Total Commits","Past 1 Week Commits","Past 2 Weeks Commits","Past 3 Weeks Commits","Past 4 Weeks Commits"]
    return jsonify(data)


@app.route('/query', methods=['POST'])
def query():
    req = request.get_json()
    target=req['targets'][0]['target']
    type=req['targets'][0]['type']
    if target =='Past 1 Week Commits':
        data=get_commit_activity(target,1)
    elif target =='Past 2 Weeks Commits':
        data=get_commit_activity(target,2)
    elif target =='Past 3 Weeks Commits':
        data=get_commit_activity(target,3)
    elif target =='Past 4 Weeks Commits':
        data=get_commit_activity(target,4)
    elif target=='Total Commits':
        data=get_commits_metrics() 
    return jsonify(data)


@app.route('/annotations', methods=['POST'])
def annotations():
    req = request.get_json()
    data = [
        {
            "annotation": 'This is the annotation',
            "time": (convert_to_time_ms(req['range']['from']) +
                     convert_to_time_ms(req['range']['to'])) / 2,
            "title": 'Deployment notes',
            "tags": ['tag1', 'tag2'],
            "text": 'Hm, something went wrong...'
        }
    ]
    return jsonify(data)


@app.route('/tag-keys', methods=['POST'])
def tag_keys():
    data = [
        {"type": "string", "text": "City"},
        {"type": "string", "text": "Country"}
    ]
    return jsonify(data)


@app.route('/tag-values', methods=['POST'])
def tag_values():
    req = request.get_json()
    if req['key'] == 'City':
        return jsonify([
            {'text': 'Tokyo'},
            {'text': 'São Paulo'},
            {'text': 'Jakarta'}
        ])
    elif req['key'] == 'Country':
        return jsonify([
            {'text': 'China'},
            {'text': 'India'},
            {'text': 'United States'}
        ])


if __name__ == '__main__':
    app.run(host='0.0.0.0',port='5000')
