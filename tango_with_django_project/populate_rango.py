import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tango_with_django_project.settings')

django.setup()
from rango.models import Category, Page


def populate():
    """First, we will create lists of dictionaries containing the pages we want to add into each category.
    Then we will create a dictionary of dictionaries for our categories.  This allows us to
    iterate through each data structure and add the data to our models."""
    python_pages = [
        {'title': 'Official Python Tutorial',
         'url': 'http://docs.python.org/3/tutorial/',
         'views': 128},
        {'title': 'How to Think like a Computer Scientist',
         'url': 'http://www.greenteapress.com/thinkpython/',
         'views': 128},
        {'title': 'Learn Python in 10 Minutes',
         'url':'http://www.korokithakis.net/tutorials/python/',
         'views': 128}
    ]

    django_pages = [
        {'title': 'Official Django Tutorial',
         'url': 'https://docs.djangoproject.com/en/2.1/intro/tutorial01/',
         'views': 128},
        {'title': 'Django Rocks',
         'url': 'http://www.djangorocks.com/',
         'views': 128},
        {'title': 'How to Tango with Django',
         'url': 'http://www.tangowithdjango.com/',
         'views': 128},
    ]

    other_pages = [
        {'title': 'Bottle',
         'url': 'http://bottlepy.org/docs/dev/',
         'views': 128},
        {'title': 'Flask',
         'url': 'http://flask.pocoo.org',
         'views': 128}
    ]

    cats = {'Python': {'pages': python_pages, 'views': 128, 'likes': 64},
            'Django': {'pages': django_pages, 'views': 64, 'likes': 32},
            'Other Frameworks': {'pages': other_pages, 'views': 32, 'likes': 16},
            'Pascal': {'pages': ([]), 'views': 0, 'likes': 0},
            'Perl': {'pages': ([]), 'views': 0, 'likes': 0},
            'PHP': {'pages': ([]), 'views': 0, 'likes': 0},
            'Prolog': {'pages': ([]), 'views': 0, 'likes': 0},
            'Postscript': {'pages': ([]), 'views': 0, 'likes': 0},
            'Programming': {'pages': ([]), 'views': 0, 'likes': 0}
            }
    # If you want to add more categories or pages, add them to the dictionaries above

    # This then goes through the cats dict, then adds each cat, and then adds all the associated pages
    # for that cat.

    for cat, cat_data in cats.items():
        c = add_cat(cat, cat_data['views'], cat_data['likes'])
        for p in cat_data['pages']:
            add_page(c, p['title'], p['url'], p['views'])

    # Print out the cats we have added
    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print(f'- {c}: {p}')


def add_page(cat, title, url, views):
    p = Page.objects.get_or_create(category=cat, title=title, views=views)[0]
    p.url = url
    p.views = views
    p.save()
    return p


def add_cat(name, views, likes):
    c = Category.objects.get_or_create(name=name, views=views, likes=likes)[0]
    c.save()
    return c


# Start execution here!
if __name__ == '__main__':
    print('Starting Rango population script...')
    populate()
