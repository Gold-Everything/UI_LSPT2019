from django.http import HttpResponse

import requests
import json

RANKING_API_URL = "http://lspt-rank2.cs.rpi.edu"
#RANKING_API_URL = "lspt-rank1.cs.rpi.edu"

STORE_API_URL = ""


DOC_COUNT_RETURNED = 300

def search(request):
    #return makeResults(getRawResults(query, weights))
    query = request.GET.get('query', '')
    weights = request.GET.get('weights', '')
    return HttpResponse(f"You searched for {query} with weights {weights}")

def getRawResults(query, weights):
    '''
    Function to be trigger by query request, will call callDocstore and callRanking
    Inputs: Form data from user: string query, list of weights
    Returns:
       JSON of merged data of the form:
       { rank :
             {
               "id": <id>,
               "score": <score>,
               "url": <url>,
               "title": <title>,
               "body": <body>
             },
             ...
       }
    '''
    # Get back JSON response of ranked doc ids (identifier->scores)
    rank_results_dict = callRanking(query, weights)
    # as of python 3.7 dict should maintain order of insertions so assuming that
    # docIds_list will be in order of url ranking high to low
    docIds_list = rank_results_dict.keys()
    # Get back JSON response of document objects for each docId
    doc_results_dict = callDocstore(docIds_list)

    # merge both jsons from callDocstore and callRanking and return result
    total_results = len(docIds_list)
    merged_results = {}
    for rank in range (1, total_results+1):
        #adding key and empty dict for current rank
        merged_results[rank] = {}
        merged_results[rank]["id"] = docIds_list[rank-1]
        merged_results[rank]["score"] = rank_results_dict[docIds_list[rank-1]]
        # (assumes list of results from DDS are also in ascending sorted,
        #  i.e. matching the order of ranking)
        merged_results[rank]["url"] = doc_results_dict["documents"][rank-1]["url"]
        merged_results[rank]["title"] = doc_results_dict["documents"][rank-1]["title"]
        merged_results[rank]["body"] = doc_results_dict["documents"][rank-1]["body"]

    return json.dumps(merged_results)

# makeResults calls parseQuery, getSnippet
# rawDocuments is the JSON object returned by getRawResults
# def makeResults(rawDocuments):

# def parseQuery(query):

# def getSnippet(document, keywords):


def callRanking(query, weights):
    # Call to ranking is a POST
    # where weights is like "weights": {"popularity": "0.87", "recency": "0.45", "exact": "true"}
    payload = {'query': query, 'weights': weights, 'results': DOC_COUNT_RETURNED}
    response = requests.post(RANKING_API_URL, data=json.dumps(payload))
    if (response):
        content = response.content
        # should get back something like {"1": "0.57", "2": "0.87", "3": "0.05", ..., "300": "0.45"}
        return json.loads(content)
    else:
        raise Exception("No response from ranking")

def callDocstore(docIds):
    '''
    DDS wants us to specify the fields we want,
    http://docdatastore/documents?id=someID,anotherID,andtheotherIDs&fields=url,title,body
    response will look like
    {
      "documents": [
          {
              "url": "some url"
              "title": "RPI Computing",
              "body": "html source here...",
          }
      ]
    }
    '''
    # https://errose28.github.io/lspt-doc-data-store/#get
    # Call to data store is a GET
    response = requests.get(STORE_API_URL, params={'id': docIds})
    if (response):
        content = response.content
        # should get back documents json
        return json.loads(content)
    else:
        raise Exception("No response from data store")
