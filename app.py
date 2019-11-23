from flask import Flask, request, jsonify;
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
from flask_cors import CORS
import psycopg2

import pandas as pd



app = Flask(__name__)
CORS(app)



@app.route('/api', methods=['POST'])
def predict():
    DATABASE_URL =b'postgres://nmqpakpthcuntd:ffc1433121c94ae86c30d33d81e07ff304a85c0dbfd8231943863bc0aad82f6c@ec2-54-221-195-148.compute-1.amazonaws.com:5432/davdmlmq9b29mi'
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor()
    data = request.get_json(force=True)
    print("wow", data)
    number = [data["Region"], data["Majors"], data["College"]]
    def region (Region):
        cur.execute('SELECT public."Region"."Average" ''FROM public."Region" ''WHERE public."Region"."region"'f"='{Region}'")
        people = cur.fetchall()
        per=0
        for person in people:
            per=person[0]+per
        return round((per/len(people)))


    def majors (Majors):
        cur.execute('SELECT public."Majors"."Average"''FROM public."Majors"''WHERE public."Majors"."name"'f"='{Majors}'")
        people = cur.fetchall()
        return round(people[0][0])

    def college (College):
        cur.execute('SELECT public."College"."Average"''FROM public."College"''WHERE public."College"."name"'f"='{College}'")
        people = cur.fetchall()
        return round(people[0][0])

    def Avg(Region, Majors, College):
        return (region(Region)+majors(Majors)+college(College))/3
        # predictions

    output = {"Salary": int(Avg(number[0], number[1], number[2]))}
    return jsonify(results=output)



if __name__ == '__main__':
    app.run()