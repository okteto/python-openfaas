import os, json
from pymongo import MongoClient

def get_uri():
    with open('/var/openfaas/secrets/mongodb-password', 'r') as file:
        password = file.read().replace('\n', '')
    return "mongodb://root:{password:s}@mongodb".format(password=password)


def handle(req):
    """handle a request to the function
    Args:
        req (str): request body
    """

    uri = get_uri()
    client = MongoClient(uri)
    db = client['attendees']
    method = os.getenv("Http_Method")
    if method == "POST":
      a = {"githubid": req.strip()}
      db.attendees.insert_one(a)
      return "ok"

    elif method == "GET":
      result = []
      for a in db.attendees.find():
             result.append({"githubid": a[u'githubid']})
      return json.dumps(result)

    return "method not supported"