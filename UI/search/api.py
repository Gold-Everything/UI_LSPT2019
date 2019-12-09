from django.http import HttpResponse

import requests
import json

#verified for ranking1
RANKING_API_URL = "http://lspt-rank1.cs.rpi.edu:5000/search"
#RANKING_API_URL = "lspt-rank2.cs.rpi.edu"

STORE_API_URL = "http://lspt-dds1.cs.rpi.edu:8080/"

# fixed number of results to ask for per query, for testing purposes
DOC_COUNT_RETURNED = 10


def search(request):
    '''
    Dummy functions to test Query page. Checks that we recieved query and send verification
    to the user. Does not call other search engine components
    Input: http request object
    Output: HttpResponse object containing string reporting search to user
    Modifies: none
    Requires: none
    '''
    #return makeResults(getRawResults(query, weights))
    query = request.GET.get('query', '')
    weights = request.GET.get('weights', '')
    results = DOC_COUNT_RETURNED
    return HttpResponse(f"You searched for {query} with weights {weights} and {results} results")

def getRawResults(query, weights, results):
    '''
    Function to be trigger by query request, will call callDocstore and callRanking
    Inputs:
        1. query(string) - query entered by user
        2. weights( json/dict ) - weights for search, takes the form:
            {"popularity": "0.87", "recency": "0.45", "exact": "true"}
        2. results(int) - number of results to get
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
    Modifies: none
    Requires: args not null

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

def makeResults(rawDocuments, query):
    '''
    Make results takes the documents returned from getRawresults and the query and generates
    the data needed to populate the results page. It will call parseQuery and getSnippet
    Inputs:
        1. rawDocuments - json of the form:
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
       2. query(string)
    Returns:
        Dictionary of the following form:
        context = {
                    "resultsDict":
                    {
                        'a':
                        {
                        "id": 1,
                        "score": 2,
                        "url": "www.rpi.edu",
                        "title": "The Honorable",
                        "body": "Shirley"
                        },
                     ...
                    }
                  }
    Modifies: none
    Requires: valid input format
    '''
    # Assuming that the list of documents is given to us in ranked order...
    loadedJSON = json.loads(rawDocuments)
    results = []
    for page in loadedJson:
        url = page["url"]
        title = page["title"]
        body = page["body"]
                
        # Use the original query to obtain keywords
        keyWords = parseQuery(query)
        snip = getSnippet(body, keyWords)

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

# Function to produce a snippet of text from the document to display to the user
def getSnippet(document, query):
    # Find keywords in document if possible, if not found, backup plan
    # TODO: Discuss specifics of finding snippet from keywords
    index = document.lower().find(query.lower())
    snippet = ""
    # Make sure document is at least 100 characters
    # If not, return entire document
    if len(document) < 100:
        return document
    # If the query was found, exact match, return a valid snippet
    if index != 0:
        # Case: query in first 50 chars, return first 100 chars of document
        if index < 50:
            snippet = document[0:100]
        # Case: query in last 50 characters, return last 100 chars of document
        elif index > (len(document) - 50):
            snippet = document[len(document)-101:len(document)-1]
        # Case: query in middle of document anywhere, return 50 before and 50 after index of query
        else:
            snippet = document[index-50:index+50] 
    # If query not found in document, return first 100 chars
    else:
        snippet = document[0:100]    

    return snippet
    

def callRanking(query, weights, results):
    '''
    This function calles the ranking components API and returns their results
    Inputs:
        1. query(string) - query entered by user
        2. weights( json/dict ) - weights for search, takes the form:
            {"popularity": "0.87", "recency": "0.45", "exact": "true"}
        2. results(int) - number of results to get
    Outputs: dict of id's to scores in order of rank in the form (if results was 300)
         {"1": "0.57", "2": "0.87", "3": "0.05", ..., "300": "0.45"}
    Modifies: none
    Requires: RANKING_API_URL is correct
    '''
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
    calls to DDS are done piecemeal. In the final version we will need to loop through
    multiple calls in order to put together all of the results
    {
      "documents": [
          {
              "url": "some url"
              "title": "RPI Computing",
              "body": "html source here...",
          }
      ]
    }
    Inputs: Dict from callRanking of form:
         {"1": "0.57", "2": "0.87", "3": "0.05", ..., "300": "0.45"}
    Outputs: Dict of same form as response from DDS
    Modifies: none
    Requires: none
    '''
    # Call to data store is a GET
    response = requests.get(STORE_API_URL, params={'id': docIds})
    if (response):
        content = response.content
        # should get back documents json
        return json.loads(content)
    else:
        raise Exception("No response from data store")