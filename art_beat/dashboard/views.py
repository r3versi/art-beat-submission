from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django import template

# Create your views here.
#@login_required(login_url="/login/")
def index(request):
    return render(request, "index.html")


def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]
        html_template = loader.get_template(load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('error-404.html')
        return HttpResponse(html_template.render(context, request))

    except:

        html_template = loader.get_template('error-500.html')
        return HttpResponse(html_template.render(context, request))
