# Python 3

import jwt, uuid, requests, json  # PyJWT

payload = {
    'access_key': 'c7DrONvxPqeASWMMKZYfeIO0HDw1FQXHBq00Cql1',
    'nonce': str(uuid.uuid4()),
}

jwt_token = jwt.encode(payload, '7dDE5HTzIFRRfxxCrAONZkiKCVzzUPp2tz99Kexd')
authorization_token = 'Bearer {}'.format(jwt_token)

url = "https://api.upbit.com/v1/market/all?isDetails=false"
headers = {"Accept": "application/json"}

response = requests.request("GET", url, headers=headers)
markets = json.loads(response.text)
for item in markets:
    print(item)