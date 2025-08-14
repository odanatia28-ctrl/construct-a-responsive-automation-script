import requests
import json
import time
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///script_tracker.db"
db = SQLAlchemy(app)

class ScriptTracker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    script_name = db.Column(db.String(100), nullable=False)
    automation_status = db.Column(db.String(100), nullable=False)
    last_run_time = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f"ScriptTracker('{self.script_name}', '{self.automation_status}', '{self.last_run_time}')"

@app.route("/new_script", methods=["POST"])
def new_script():
    data = request.get_json()
    script = ScriptTracker(script_name=data["script_name"], automation_status="pending", last_run_time=None)
    db.session.add(script)
    db.session.commit()
    return jsonify({"message": "Script added successfully"}), 201

@app.route("/update_status", methods=["PUT"])
def update_status():
    data = request.get_json()
    script = ScriptTracker.query.filter_by(id=data["id"]).first()
    script.automation_status = data["automation_status"]
    script.last_run_time = time.strftime("%Y-%m-%d %H:%M:%S")
    db.session.commit()
    return jsonify({"message": "Script status updated successfully"}), 200

@app.route("/get_scripts", methods=["GET"])
def get_scripts():
    scripts = ScriptTracker.query.all()
    output = []
    for script in scripts:
        script_data = {}
        script_data["id"] = script.id
        script_data["script_name"] = script.script_name
        script_data["automation_status"] = script.automation_status
        script_data["last_run_time"] = script.last_run_time
        output.append(script_data)
    return jsonify({"scripts": output})

if __name__ == "__main__":
    app.run(debug=True)