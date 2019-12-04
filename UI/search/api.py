from django.http import HttpResponse

import requests
import json

<<<<<<< HEAD
RANKING_API_URL = "" # TO BE FILLED IN WITH LOCATION OF RANKING
STORE_API_URL = "" # TO BE FILLED IN WITH LOCATION OF DOC_DATA_STORE
=======
RANKING_API_URL = "lspt-rank2.cs.rpi.edu"
#RANKING_API_URL = "lspt-rank1.cs.rpi.edu"

STORE_API_URL = ""
>>>>>>> ee38a7bafcc12bd77f050c4e79af3277eb246582

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
    rank_results = callRanking(query, weights)
    rank_results_dict = json.loads(rank_results) #convert json of urls->scores to dictionary
    #as of python 3.7 dict should maintain order of insertions so assuming that
    #docIds_list will be in order of url ranking high to lowi
    docIds_list = rank_results_dict.keys()
    doc_results = callDocstore(docIds_list)
    doc_results_dict = json.loads(doc_results)

    #merge both jsons from callDocstore and callRanking and return result
    total_results = len(docIds_list)
    merged_results = {}
    for rank in range (1, total_results+1):
        merged_results[rank] = {} #adding key and empty dict for current rank 
        #append ID
        merged_results[rank]["id"] = docIds_list[rank-1]
        #append score
        merged_results[rank]["score"] = rank_results_dict[docIds_list[rank-1]]
        #append URL (assumes list of results from DDS are also in ascending sorted
        #order by rank
        merged_results[rank]["url"] = doc_results_dict["documents"][rank-1]["url"]
        #append title (same assumption as for url)
        merged_results[rank]["title"] = doc_results_dict["documents"][rank-1]["title"]
        #append doc text (same assumption as for url)
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
        ranked_doc_ids = json.loads(content)
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
        documents = json.loads(content)
    else:
        raise Exception("No response from data store")
