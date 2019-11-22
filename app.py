from flask import Flask, request, jsonify;
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
import sqlite3
from flask_cors import CORS

import pandas as pd



app = Flask(__name__)
CORS(app)



@app.route('/api', methods=['POST'])
def predict():
    conn = sqlite3.connect('TestDB.db')
    cur = conn.cursor()
    data = request.get_json(force=True)
    print(data)
    number = [data["Region"], data["Majors"], data["College"]]
    def region (Region):
        cur.execute(f'SELECT Average FROM Region WHERE region="{Region}"')
        people = cur.fetchall()
        per=0
        for person in people:
            per=person[0]+per
        return round((per/len(people)))


    def majors (Majors):
        cur.execute(f'SELECT Average FROM Majors WHERE name="{Majors}"')
        people = cur.fetchall()
        return round(people[0][0])

    def college (College):
        cur.execute(f'SELECT Average FROM College WHERE name="{College}"')
        people = cur.fetchall()
        return round(people[0][0])

    def Avg(Region, Majors, College):
        return (region(Region)+majors(Majors)+college(College))/3
        # predictions

    output = {"Salary": int(Avg(number[0], number[1], number[2]))}
    return jsonify(results=output)



if __name__ == '__main__':
    app.run()