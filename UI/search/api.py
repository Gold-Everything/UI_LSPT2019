from django.http import HttpResponse

import requests
import json

RANKING_API_URL = ""
STORE_API_URL = ""

DOC_COUNT_RETURNED = 300

def search(request):
    #return makeResults(getRawResults(query, weights))
    query = request.GET.get('query', '')
    weights = request.GET.get('weights', '')
    return HttpResponse(f"You searched for {query} with weights {weights}")

# def getRawResults(query, weights):


# def makeResults(rawDocuments):


# def getSnippet(document, keywords):


def callRanking(query, weights):
    # Call to ranking is a POST
    # where weights is like "weights": {"popularity": "0.87", "recency": "0.45", "exact": "true"}
    payload = {'query': query, 'weights': weights, 'results': DOC_COUNT_RETURNED}
    response = requests.post(RANKING_API_URL, data=json.dumps(payload))
    if (response):
        content = response.content
        # should get back something like {"1": "0.57", "2": "0.87", "3": "0.05", ..., "300": "0.45"}
        ranked_doc_ids = json.loads(content)
    else:
        raise Exception("No response from ranking")

def callDocstore(docIds):
    # https://errose28.github.io/lspt-doc-data-store/#get
    # Call to data store is a GET
    response = requests.get(RANKING_API_URL, params={'id': docIds})
    if (response):
        content = response.content
        # should get back documents json
        documents = json.loads(content)
    else:
        raise Exception("No response from data store")