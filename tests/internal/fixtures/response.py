import json

import requests

dummyResponse: requests.Response = requests.Response()
dummyResponse._content = json.dumps("content").encode("utf-8")
