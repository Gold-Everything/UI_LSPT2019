from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import api


def index(request):
    template = loader.get_template('index.html')
    context = {
        # 'showings_list': showings_list,
    }
    return HttpResponse(template.render(context, request))
    '''
    # replace bylaws.html with whatever html you want to load
    # context is a dictionary, put what you want in it then you can use
    # the context data in the html.

    template = loader.get_template('bylaws.html')
    context = {
        # 'showings_list': showings_list,
    }
    return HttpResponse(template.render(context, request))
    '''

def search_results(request):
    '''
    I think this is the entry point for running our API calls and generating search results?
    We do the following:
    1. pull up the template (html file for results)
    2. set the context using the results of calling getRawResults and makeResults
    '''
    template = loader.get_template('results.html')
    
    #not sure what the request argument is or how to get the form data
    raw_results = api.getRawResults(query, weights)
    
    finale_result = api.makeResults(raw_results)

    #add a function to transform the list of jsons returned from makeResults into the actual context Dict?
    context = transformResults(final_results)

    #context = {
        # 'showings_list': showings_list,
    #}
    
    return HttpResponse(template.render(context, request))
    
    #return HttpResponse('Here are your results')
