from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

def index(request):
    return HttpResponse('HELLO WORLD! Your at the search app index view')
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
    return HttpResponse('Here are your results')
