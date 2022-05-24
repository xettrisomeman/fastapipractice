import requests


token = requests.post(
    url="http://localhost:8000/api/login",
    data={
        'username': 'john',
        'password': 'eightyeight'
    }
).json()


access_token = token.get("access_token", None)

if access_token:
    # print(access_token)
    headers = {
        "Authorization": f'Bearer {access_token}',
        "accept": "application/json"
    }
    data = {
        "title": "Nothing lasts forever",
        "body": "if everything is here, where to find something that you need?"
    }
    url = "http://localhost:8000/api/posts"
    make_login = requests.post(
        url=url,
        data=data,
        headers=headers
    ).json()

    print(make_login)
