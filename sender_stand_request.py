import configuration
import requests
import data

def post_new_user(user_body):
    return requests.post(configuration.URL_SERVICE + configuration.CREATE_USERS_PATH,
                         json=user_body,
                         headers = data.headers)

response=post_new_user(data.user_body)
print(response.status_code)
print(response.json())

def get_user_table():
    return requests.get(configuration.URL_SERVICE + configuration.USERS_TABLE_PATH)

response = get_user_table()
print(response.status_code)
print(response.text)