from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for, abort, make_response
import sqlalchemy
from .models import Month, Build, ExecutionRun, all_build_schema, build_schema, all_month_schema, month_schema, all_execution_run_schema, execution_run_schema
from . import db
from libs.internal_api.internal_api import InternalAPI
from libs.helper_functions import get_base_url_port_conditional

api = Blueprint('api', __name__)


# Get month api
@api.route('/date', methods=['GET'])
def get_month_api():
    """
    api endpoint for querying month api. option to specify 'month' query parameter to filter for a specific month name
    """
    if 'month' in request.args:  # check if month is in query arguments else fetch all month objects
        return __fetch_db_data_single(table_to_filter='month', query_params={'month': request.args['month']}, 
                                    one_to_many_associated_lists=['build', 'execution_run'])
    else:
        return __fetch_db_data_multiple(table_to_filter='month', one_to_many_associated_lists=['build', 'execution_run'])


# Get month api
@api.route('/build', methods=['GET'])
def get_build_api():
    """
    api endpoint for querying build api. option to specify 'build_name' query parameter to filter for a specific build name
    """
    if 'build_name' in request.args:  # check if build is in query arguments else fetch all build objects
        return __fetch_db_data_single(table_to_filter='build', query_params={'build_name': request.args['build_name']}, 
                                    one_to_many_associated_lists=['execution_run'], replace_param_id_with_name=['month'])
    else:
        return __fetch_db_data_multiple(table_to_filter='build', one_to_many_associated_lists=['execution_run'], replace_param_id_with_name=['month'])


# Get month api
@api.route('/run', methods=['GET'])
def get_run_api():
    """
    api endpoint for querying execution run api. option to specify 'run_name' query parameter to filter for a specific execution run name
    """
    if 'execution_run_name' in request.args:  # check if load is in query arguments else fetch all load objects
        return __fetch_db_data_single(table_to_filter='execution_run', query_params={'execution_run_name': request.args['execution_run_name']}, 
                                    replace_param_id_with_name=['build', 'month'])
    else:
        return __fetch_db_data_multiple(table_to_filter='execution_run', replace_param_id_with_name=['build', 'month'])


def __fetch_db_data_single(table_to_filter=None, query_params=None, one_to_many_associated_lists=None, replace_param_id_with_name=None):
    """ This function if for querying a database with specific query parameters, and returning the database params in a restful format. 
    This function is used for querying a unique parameter such as the name column in db table. eg usage.
    fetch_db_data_single(table_to_filter='month', query_params={'month': request.args['month']}, one_to_many_associated_lists=['build', 'execution_run']),
    fetch_db_data_single(table_to_filter='build', query_params={'build_name': request.args['build_name']}, 
                         one_to_many_associated_lists=['execution_run'], replace_param_id_with_name=['month'])

    :param table_to_filter: The table that you want to be filtered. options: 'month', 'build', 'execution_run'

    :param query_params: The parameters that you want to filter from the db. Data must be of type dict(). eg.
    query_params={'build_name': request.args['build_name']}

    :param one_to_many_associated_lists: all of the elements you wish to display the relationships of. This would show 
    all the many relationships associated with the one db table row. Data must be of type list(). eg. 
    one_to_many_associated_lists=['build', 'execution_run']

    :param replace_param_id_with_name: For backref relational mapping, replace the id with the unique name. Note that the 'name' specified must
    be of the format name_id eg. 
    replace_param_id_with_name=['month', 'build'] with replace month_id, build_id with month -> month_name, build -> build_name
    """

    query_param_mapping = {
        'month': {
            'query_param': 'month',
            'db_table': Month,
            'schema': month_schema,
        },
        'build': {
            'query_param': 'build_name',
            'db_table': Build,
            'schema': build_schema
        },
        'execution_run': {
            'query_param': 'execution_run_name',
            'db_table': ExecutionRun,
            'schema': execution_run_schema
        }
    }

    db_table = query_param_mapping[table_to_filter]['db_table']
    schema = query_param_mapping[table_to_filter]['schema']
    
    db_object_filtered = db_table.query.filter_by(**query_params).first()  # fetch filtered db object
    db_object_serialized = schema.dump(db_object_filtered)  # serialize it into a dict
    if db_object_filtered is not None:  # check if that object exists

        if one_to_many_associated_lists is not None:  # check to see if user wants to add association lists to api data
            one_to_many_associated_lists_object = dict()
            
            if 'execution_run' in one_to_many_associated_lists:
                one_to_many_associated_lists_object.update({'execution_run': db_object_filtered.execution_run_backref})
            if 'build' in one_to_many_associated_lists:
                one_to_many_associated_lists_object.update({'build': db_object_filtered.build_backref})

            for key, value in one_to_many_associated_lists_object.items():
                associated_objects_list = list()  # append all execution run names for that load into a list
                for associated_element in value:

                    if key == 'month':
                        association_name = associated_element.month
                        associated_objects_list.append(association_name)
                    if key == 'build':
                        association_name = associated_element.build_name
                        associated_objects_list.append(association_name)
                    if key == 'execution_run':
                        association_name = associated_element.execution_run_name
                        associated_objects_list.append(association_name)
                    

                db_object_serialized.update({key: associated_objects_list})  # add to the serialized object a details key with the list of execution runs
        
        if replace_param_id_with_name is not None:  # check to see if user wants to replace any forein keys with unique name element
            for param_id in replace_param_id_with_name:
                if param_id == 'month':
                    db_object_serialized[param_id] = query_param_mapping[param_id]['db_table'].query.filter_by(id=db_object_serialized[f'{param_id}_id']).first().month  # replace month_id with month name
                elif param_id == 'build':
                    db_object_serialized[param_id] = query_param_mapping[param_id]['db_table'].query.filter_by(id=db_object_serialized[f'{param_id}_id']).first().build_name
                elif param_id == 'execution_run':
                    db_object_serialized[param_id] = query_param_mapping[param_id]['db_table'].query.filter_by(id=db_object_serialized[f'{param_id}_id']).first().execution_run_name
                del db_object_serialized[f'{param_id}_id']

        return jsonify(db_object_serialized)  # jsonify the dict


    else:
        abort(make_response({'status_code': 404, 'message': f'That {table_to_filter} object was not found in the database'}, 404))


def __fetch_db_data_multiple(table_to_filter=None, one_to_many_associated_lists=None, replace_param_id_with_name=None):
    """ This function if for querying a an entire database table, and returning the database params in a restful format. 
    No query parameters are used for this function as it returns all elements in the table. eg usage.
    fetch_db_data_multiple(table_to_filter='month', one_to_many_associated_lists=['build', 'execution_run']),
    fetch_db_data_multiple(table_to_filter='build', one_to_many_associated_lists=['execution_run'], replace_param_id_with_name=['month'])

    :param table_to_filter: The table that you want to be filtered. options: 'month', 'build', 'execution_run'

    :param one_to_many_associated_lists: all of the elements you wish to display the relationships of. This would show 
    all the many relationships associated with the one db table row. Data must be of type list(). eg. 
    one_to_many_associated_lists=['build', 'execution_run']

    :param replace_param_id_with_name: For backref relational mapping, replace the id with the unique name. Note that the 'name' specified must
    be of the format name_id eg. 
    replace_param_id_with_name=['month', 'build'] with replace month_id, build_id with month -> month_name, build -> build_name
    """

    query_param_mapping = {
        'month': {
            'query_param': 'month',
            'db_table': Month,
            'schema': all_month_schema,
        },
        'build': {
            'query_param': 'build_name',
            'db_table': Build,
            'schema': all_build_schema
        },
        'execution_run': {
            'query_param': 'execution_run_name',
            'db_table': ExecutionRun,
            'schema': all_execution_run_schema
        }
    }

    db_table = query_param_mapping[table_to_filter]['db_table']
    schema = query_param_mapping[table_to_filter]['schema']
    
    db_object_all = db_table.query.all()  # fetch filtered db object
    db_object_serialized = schema.dump(db_object_all)  # serialize it into a dict
    if db_object_all is not None:  # check if that object exists

        if one_to_many_associated_lists is not None:  # check to see if user wants to add association lists to api data

            for idx, db_object in enumerate(db_object_all):
                one_to_many_associated_lists_object = dict()
                
                if 'execution_run' in one_to_many_associated_lists:
                    one_to_many_associated_lists_object.update({'execution_run': db_object.execution_run_backref})
                if 'build' in one_to_many_associated_lists:
                    one_to_many_associated_lists_object.update({'build': db_object.build_backref})


                for key, value in one_to_many_associated_lists_object.items():
                    associated_objects_list = list()  # append all execution run names for that load into a list
                    for associated_element in value:

                        if key == 'month':
                            association_name = associated_element.month
                            associated_objects_list.append(association_name)
                        if key == 'build':
                            association_name = associated_element.build_name
                            associated_objects_list.append(association_name)
                        if key == 'execution_run':
                            association_name = associated_element.execution_run_name
                            associated_objects_list.append(association_name)
                        

                    db_object_serialized[idx].update({key: associated_objects_list})  # add to the serialized object a details key with the list of execution runs
        
        if replace_param_id_with_name is not None:  # check to see if user wants to replace any forein keys with unique name element
            for idx, db_object in enumerate(db_object_serialized):
                for param_id in replace_param_id_with_name:
                    if param_id == 'month':
                        db_object_serialized[idx][param_id] = query_param_mapping[param_id]['db_table'].query.filter_by(
                            id=db_object[f'{param_id}_id']).first().month  # replace month_id with month name
                    elif param_id == 'build':
                        db_object_serialized[idx][param_id] = query_param_mapping[param_id]['db_table'].query.filter_by(
                            id=db_object[f'{param_id}_id']).first().build_name
                    elif param_id == 'execution_run':
                        db_object_serialized[idx][param_id] = query_param_mapping[param_id]['db_table'].query.filter_by(
                            id=db_object[f'{param_id}_id']).first().execution_run_name
                    del db_object[f'{param_id}_id']

        return jsonify(db_object_serialized)  # jsonify the dict


    else:
        abort(make_response({'status_code': 404, 'message': f'That {table_to_filter} object was not found in the database'}, 404))