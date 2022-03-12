from flask import Blueprint, render_template, request, flash, jsonify, send_file, abort, redirect
from werkzeug.utils import secure_filename
import json
import datetime
from flask.helpers import url_for
import os, sys
from subprocess import Popen, PIPE
from . import app
from libs.internal_api.internal_api import InternalAPI

views = Blueprint('views', __name__)

ALLOWED_EXTENSIONS = ['gz', 'png', 'jpg', 'jpeg']

app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'uploads')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.errorhandler(404)
def not_found(e):
    return render_template("404.html")

@views.route('/')
def month_listing():
    internal_api = InternalAPI()
    month_objects = internal_api.get_months().json()
    month_list = [month['month'] for month in month_objects]

    return render_template('month_display.html', month_list=sorted(month_list))

@views.route('/builds')
def builds_listing():
    internal_api = InternalAPI()
    month = request.args.get('month')
    
    build_object = internal_api.get_builds().json()

    if month is None:  # check if query parameter exists
        return render_template('404.html')

    # check if the specified month exists and api does not return 404 not found
    if internal_api.get_months(month=month).status_code != 200:
        return render_template('404.html')

    # create a list of builds that only belong to the specified month
    build_list = [build['build_name'] for build in build_object if build['month'] == month]

    return render_template('builds_display.html', build_list=sorted(build_list), month=month)

@views.route('/runs')
def execution_runs_listing():
    internal_api = InternalAPI()
    month = request.args.get('month')
    build = request.args.get('build')
    run_object = internal_api.get_runs().json()

    if month is None or build is None:  # check if query parameter exists
        return render_template('404.html')

    # check if the specified month and build exists and api does not return 404 not found
    if internal_api.get_months(month=month).status_code != 200 or internal_api.get_builds(build=build).status_code != 200:
        return render_template('404.html')
    
    # check the build has a relationship to the month and if not return 404 not found page
    if build not in internal_api.get_months(month=month).json()['build']:
        return render_template('404.html')
        
    # create a list of executions that only belong to the specified month and build
    run_list = [run['execution_run_name'] for run in run_object if run['month'] == month and run['build'] == build]

    return render_template('runs_display.html', run_list=sorted(run_list), month=month, build=build)



@views.route('/upload-file', methods=['GET'])
def upload_form():
    return render_template('upload.html')


@views.route('/upload-file', methods=['POST'])
def upload_file():
    print(f'upload_file: {request.method}')
    if request.method == 'POST':
        # check if the post request has the file part
        
        files = request.files.getlist('files[]')
        file = request.files['files[]']
        print(files)
        print(file)
        # if user does not select file, browser also
        # submit an empty part without filename
        if 'files[]' not in request.files:
            flash('No file part')
            return abort(400)
        print(files)
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                os.system(f'mkdir -p {app.config["UPLOAD_FOLDER"]}')
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    return redirect(url_for('views.upload_form'))


# @views.route('/allure-report', methods=['GET'])
# def allure_report():

#     process = Popen(['allure', 'serve', f'{request.args["path"]}', '--output', f'{app.config["UPLOAD_FOLDER"]}'], stdout=PIPE, stderr=PIPE)
#     os.system(f'allure generate --output /Users/lucasrahn/misc/LOCATION {request.args["path"]}')
#     # os.system(f'allure open /Users/lucasrahn/misc/LOCATION')
#     process = Popen(['allure', 'open', f'/Users/lucasrahn/misc/LOCATION'], stdout=PIPE, stderr=PIPE)
#     return 'success'
#     stdout, stderr = process.communicate()
#     print(stdout)
#     print(stderr)
#     print(process.pid)

