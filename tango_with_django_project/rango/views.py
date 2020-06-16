from django.shortcuts import render
from django.http import HttpResponse

# Import models
from rango.models import Category
from rango.models import Page


def show_category(request, category_name_slug):
    # Create a context dictionary which we can pass to the template rendering engine.
    context_dict = {}

    try:
        # Can we find category name slug with the given name?
        # If we can't, the .get() method raises a DoesNotExist exception.
        # The .get() method returns one model instance or raises an exception.
        category = Category.objects.get(slug=category_name_slug)

        # Retrieve all of the associated pages.  The filter() will return a list of page objects or an empty list.
        pages = Page.objects.filter(category=category)
        # Adds our results list to the tmeplate context under name pages.
        context_dict['pages'] = pages

        # We also add the category object from the database to the context dictionary.
        # We'll use this in the template to verify that the category exists.
        context_dict['category'] = category
    except Category.DoesNotExist:
        # We get here if we didn't find the specified category
        # Do nothing, template will display the "no category" message for us.
        context_dict['category'] = None
        context_dict['pages'] = None

    # Render the response, return to client.
    return render(request, 'rango/category.html', context=context_dict)


def index(request):
    # Query db for list of all categories/pages currently stored, ordered by likes/title in descending order.
    # the '-' in '-likes' means descending order, without it then it'd be ascending
    # Retrieve top 5 only or all if less than 5.
    # Place the list in context_dict (with boldmessage) that will be passed to the template.
    category_list = Category.objects.order_by('-likes')[:5]
    pages_list = Page.objects.order_by('-views')[:5]

    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage matches to {{ boldmessage }} in the template!
    context_dict = dict()
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['categories'] = category_list
    context_dict['pages'] = pages_list

    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.
    return render(request, 'rango/index.html', context=context_dict)


def about(request):
    context_dict = {'boldmessage': 'This tutorial has been put together by Riccoveigh.'}

    return render(request, 'rango/about.html', context=context_dict)

