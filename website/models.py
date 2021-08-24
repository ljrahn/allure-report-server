from . import db
from . import ma
from sqlalchemy.sql import func


# # For development purposes
# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_marshmallow import Marshmallow
# app = Flask(__name__)
# DB_NAME = 'database.db'
# app.config['SECRET_KEY'] = 'this_is_my_secret'
# app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
# db = SQLAlchemy(app)
# ma = Marshmallow()
# db.init_app(app)
# # For development purposes \


class Month(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    month = db.Column(db.String(64), unique=True)
    build_backref = db.relationship('Build', backref='month')
    execution_run_backref = db.relationship('ExecutionRun', backref='month')

class Build(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    build_name = db.Column(db.String(128), unique=True)
    execution_run_backref = db.relationship('ExecutionRun', backref='build')
    month_id = db.Column(db.Integer, db.ForeignKey('month.id'))

class ExecutionRun(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    execution_run_name = db.Column(db.String(128))
    build_id = db.Column(db.Integer, db.ForeignKey('build.id'))
    month_id = db.Column(db.Integer, db.ForeignKey('month.id'))


class ExecutionRunSchema(ma.Schema):
    class Meta:
        model = ExecutionRun
        fields = ('id', 'execution_run_name', 'build_id', 'month_id')
        ordered = True

class BuildSchema(ma.Schema):
    class Meta:
        model = Build
        fields = ('id', 'build_name', 'month_id')
        ordered = True


class MonthSchema(ma.Schema):
    executions = ma.Nested(BuildSchema, many=True)
    class Meta:
        model = Month
        fields = ('id', 'month')
        ordered = True

execution_run_schema = ExecutionRunSchema()
all_execution_run_schema = ExecutionRunSchema(many=True)
build_schema = BuildSchema()
all_build_schema = BuildSchema(many=True)
month_schema = MonthSchema()
all_month_schema = MonthSchema(many=True)


if __name__ == '__main__':

    db.create_all()
    july = Month(month='July')
    august = Month(month='August')
    september = Month(month='September')
    commit_1 = Build(build_name='commit_1', month=july)
    commit_2 = Build(build_name='commit_2', month=july)
    commit_3 = Build(build_name='commit_3', month=august)
    commit_4 = Build(build_name='commit_4', month=august)
    commit_5 = Build(build_name='commit_5', month=august)
    commit_6 = Build(build_name='commit_6', month=august)
    commit_7 = Build(build_name='commit_7', month=september)
    commit_8 = Build(build_name='commit_8', month=september)
    commit_9 = Build(build_name='commit_9', month=september)
    commit_10 = Build(build_name='commit_10', month=september)
    run_1 = ExecutionRun(execution_run_name='run_1', build=commit_1, month=july)
    run_2 = ExecutionRun(execution_run_name='run_2', build=commit_1, month=july)
    run_3 = ExecutionRun(execution_run_name='run_3', build=commit_2, month=july)
    run_4 = ExecutionRun(execution_run_name='run_4', build=commit_2, month=july)
    run_5 = ExecutionRun(execution_run_name='run_5', build=commit_3, month=august)
    run_6 = ExecutionRun(execution_run_name='run_6', build=commit_3, month=august)
    run_7 = ExecutionRun(execution_run_name='run_7', build=commit_4, month=august)
    run_8 = ExecutionRun(execution_run_name='run_8', build=commit_4, month=august)
    run_9 = ExecutionRun(execution_run_name='run_9', build=commit_5, month=august)
    run_10 = ExecutionRun(execution_run_name='run_10', build=commit_5, month=august)
    run_11 = ExecutionRun(execution_run_name='run_11', build=commit_6, month=august)
    run_12 = ExecutionRun(execution_run_name='run_12', build=commit_6, month=august)
    run_13 = ExecutionRun(execution_run_name='run_13', build=commit_7, month=september)
    run_14 = ExecutionRun(execution_run_name='run_14', build=commit_7, month=september)
    run_15 = ExecutionRun(execution_run_name='run_15', build=commit_8, month=september)
    run_16 = ExecutionRun(execution_run_name='run_16', build=commit_8, month=september)
    run_17 = ExecutionRun(execution_run_name='run_17', build=commit_9, month=september)
    run_18 = ExecutionRun(execution_run_name='run_18', build=commit_9, month=september)
    run_19 = ExecutionRun(execution_run_name='run_19', build=commit_10, month=september)
    run_20 = ExecutionRun(execution_run_name='run_20', build=commit_10, month=september)
    run_21 = ExecutionRun(execution_run_name='run_21', build=commit_10, month=september)
    db.session.add_all([july, august, commit_1, commit_2, commit_3, commit_4, commit_5, commit_6, commit_7, commit_8, commit_9, commit_10, run_1, run_2, run_3, run_4, run_5, run_6, run_7, run_8, run_9, run_10, run_11, run_12, run_13, run_14, run_15, run_16, run_17, run_18, run_19, run_20, run_21,])
    db.session.commit()
    # july = Month.query.filter_by(month='July').first()
    # august = Month.query.filter_by(month='August').first()
    # commit_1 = Build.query.filter_by(build_name='commit_1').first()
    # commit_2 = Build.query.filter_by(build_name='commit_2').first()
    # commit_3 = Build.query.filter_by(build_name='commit_3').first()
    # commit_4 = Build.query.filter_by(build_name='commit_4').first()
    # commit_5 = Build.query.filter_by(build_name='commit_5').first()
    # run_1 = ExecutionRun.query.filter_by(execution_run_name='run_1').first()
    # run_2 = ExecutionRun.query.filter_by(execution_run_name='run_2').first()
    # run_3 = ExecutionRun.query.filter_by(execution_run_name='run_3').first()
    # run_4 = ExecutionRun.query.filter_by(execution_run_name='run_4').first()
    # run_5 = ExecutionRun.query.filter_by(execution_run_name='run_5').first()
    # run_6 = ExecutionRun.query.filter_by(execution_run_name='run_6').first()
    # run_7 = ExecutionRun.query.filter_by(execution_run_name='run_7').first()
    # run_8 = ExecutionRun.query.filter_by(execution_run_name='run_8').first()
    # run_9 = ExecutionRun.query.filter_by(execution_run_name='run_9').first()
    # run_10 = ExecutionRun.query.filter_by(execution_run_name='run_10').first()