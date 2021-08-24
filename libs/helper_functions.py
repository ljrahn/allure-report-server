from flask import request
from urllib.parse import urlparse

def get_base_url_port():
    """ 
    :param request: flask request object
    :returns: full base url + port
    """
    url_obj = urlparse(request.base_url)
    return f'{url_obj.scheme}://{url_obj.hostname}:{url_obj.port}'

def get_base_url_port_conditional():
    """ 
    :param request: flask request object
    :returns: full base url + port if hostname is localhost, else full base url
    """
    url_obj = urlparse(request.base_url) 
    if url_obj.hostname == 'localhost' or url_obj.hostname == '127.0.0.1':
        return f'{url_obj.scheme}://{url_obj.hostname}:{url_obj.port}'
    else:
        return f'{url_obj.scheme}://{url_obj.hostname}'