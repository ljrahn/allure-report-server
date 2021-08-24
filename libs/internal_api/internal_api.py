import requests
import json
from flask import request

class InternalAPI:
    """
    A class to make REST calls to the internal API.
    :param base_url: The base url of the server
    """
    def __init__(self):
        self.base_url = request.url_root
        self.headers = {
            'Content-Type': 'application/json'
        }
    
    def get_months(self, month=None):
        """
        :param month: optional month param. Specify for specific month obj
        :returns: list of month objs if month is None else return specific month obj
        """
        if month is None:
            response = requests.get(f'{self.base_url}/api/date', headers=self.headers)
        else:
            response = requests.get(f'{self.base_url}/api/date?month={month}', headers=self.headers)
        return response
    
    def get_builds(self, build=None):
        """
        :param build: optional build name. Specify for specific build obj
        :returns: list of build objs if build is None else return specific build obj
        """
        if build is None:
            response = requests.get(f'{self.base_url}/api/build', headers=self.headers)
        else:
            response = requests.get(f'{self.base_url}/api/build?build_name={build}', headers=self.headers)
        return response


    def get_runs(self, run=None):
        """
        :param run: optional run name. Specify for specific run obj
        :returns: list of execution run objs if run is None else return specific run obj
        """
        if run is None:
            response = requests.get(f'{self.base_url}/api/run', headers=self.headers)
        else:
            response = requests.get(f'{self.base_url}/api/run?run_name={run}', headers=self.headers)
        return response

    # def post_tracking_objs(self, body=None):
    #     """
    #     :param body: the payload as a dict consisting of tracking_number, address_from, address_to, tracking_status
    #     :returns: returns back the response from the rest api
    #     """
    #     response = requests.post(f'{self.base_url}/tracking', headers=self.headers, data=json.dumps(body))
         
    #     return response

    # def put_tracking_objs(self, body=None):
    #     """
    #     :param body: the payload as a dict consisting of tracking_number, address_from, address_to, tracking_status
    #     :returns: returns back the response from the rest api
    #     """
    #     response = requests.put(f'{self.base_url}/tracking', headers=self.headers, data=json.dumps(body))
         
    #     return response

    # def delete_tracking_objs(self, tracking_number=None):
    #     """
    #     :param tracking_number: tracking number to delete
    #     :returns: list of tracking objs if tracking_number is None else return specific tracking obj
    #     """
    #     response = requests.delete(f'{self.base_url}/tracking?tracking_number={tracking_number}', headers=self.headers)

    #     return response