from django.http import HttpResponse

import requests
import json

RANKING_API_URL = "http://lspt-rank1.cs.rpi.edu:5000/search"

STORE_API_URL = "http://lspt-dds1.cs.rpi.edu:8080/"


DOC_COUNT_RETURNED = 10

def search(request):
    #return makeResults(getRawResults(query, weights))
    query = request.GET.get('query', '')
    weights = request.GET.get('weights', '')
    results = DOC_COUNT_RETURNED
    return HttpResponse(f"You searched for {query} with weights {weights} and {results} results")

def getRawResults(query, weights, results):
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
    rank_results_dict = callRanking(query, weights, results)
    print(rank_results_dict)
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
def makeResults(rawDocuments, query):
    # Assuming that the list of documents is given to us in ranked order...
    loadedJSON = json.loads(rawDocuments)
    results = []
    for page in loadedJson:
        url = page["url"]
        title = page["title"]
        body = page["body"]

        # Use the original query to obtain keywords
        #keyWords = parseQuery(query)
        #snip = getSnippet(body, keyWords)

        # Add relevant items to some container to be used in making results page
        # Including: title, url, and snippet, for each page
        # Dependent on what we want to send to the results html

    return results

# Removes all stop words from queries to obtain a list of keywords from the query
# Used in to find where to obtain the snippet for the results page
def parseQuery(query):
    # List of stop words?
    # TODO: Not sure exactly what stopwords we want to ignore, cause some of these may be more relevant in search
    stopwords = ["the", "of", "to", "and", "in", "said", "for", "that", "was", "on", "he", "is", "with", "at", "by", "it", "from", "as", "be", "were", "an", "have", "his", "but", "has", "are", "not", "who", "they", "its", "had", "will", "would", "about", "been", "this", "their", "new", "or", "which", "we", "more", "after", "us", "percent", "up", "one", "people"]

    queryList = query.split()
    keyWords = [word for word in queryList if word.lower() not in stopwords]
    return keyWords

def getSnippet(document, keywords):
    # Find keywords in document if possible, if not found, backup plan
    # TODO: Discuss specifics of finding snippet from keywords
    return

def callRanking(query, weights, results):
    # Call to ranking is a POST
    # where weights is like "weights": {"popularity": "0.87", "recency": "0.45", "exact": "true"}
    payload = {'query': query, 'weights': weights, 'results': results}
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
