import json
from iqvia.application import create_app


def post(url, data):
    response = app.test_client().post(url, data=json.dumps(data), headers={'content-type': 'application/json'})
    data = json.loads(response.get_data(as_text=True)) if response.data else None
    return response.status_code, data


def get(url):
    response = app.test_client().get(url)
    data = json.loads(response.get_data(as_text=True)) if response.data else None
    return response.status_code, data


def delete(url):
    response = app.test_client().delete(url)
    return response.status_code


app = create_app('testing')

