from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from datetime import datetime
from rango.models import Category, Page, UserProfile
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from rango.bing_search import run_query
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User


class IndexView(View):
    def get(self, request):
        category_list = Category.objects.order_by('-likes')[:5]
        page_list = Page.objects.order_by('-views')[:5]

        context_dict = {}
        context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
        context_dict['categories'] = category_list
        context_dict['pages'] = page_list
        context_dict['extra'] = 'From the model solution on GitHub'

        visitor_cookie_handler(request)

        return render(request, 'rango/index.html', context=context_dict)


class AboutView(View):
    def get(self, request):
        context_dict = {}
        visitor_cookie_handler(request)
        context_dict['visits'] = request.session['visits']

        return render(request, 'rango/about.html', context=context_dict)


class ShowCategoryView(View):
    def create_context_dict(self, category_name_slug):
        context_dict = {}

        try:
            category = Category.objects.get(slug=category_name_slug)
            pages = Page.objects.filter(category=category).order_by('-views')

            context_dict['pages'] = pages
            context_dict['category'] = category
        except Category.DoesNotExist:
            context_dict['pages'] = None
            context_dict['category'] = None

        return context_dict

    def get(self, request, category_name_slug):
        context_dict = self.create_context_dict(category_name_slug)
        return render(request, 'rango/category.html', context_dict)

    @method_decorator(login_required)
    def post(self, request, category_name_slug):
        context_dict = self.create_context_dict(category_name_slug)
        query = request.POST['query'].strip()

        if query:
            context_dict['result_list'] = run_query(query)
            context_dict['query'] = query

        return render(request, 'rango/category.html', context_dict)


class AddCategoryView(View):
    @method_decorator(login_required)
    def get(self, request):
        form = CategoryForm()
        return render(request, 'rango/add_category.html', {'form': form})

    @method_decorator(login_required)
    def post(self, request):
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return redirect(reverse('rango:index'))
        else:
            print(form.errors)

        return render(request, 'rango/add_category.html', {'form': form})


class AddPageView(View):
    def get_category_name(self, category_name_slug):
        try:
            return Category.objects.get(slug=category_name_slug)
        except Category.DoesNotExist:
            return None

    @method_decorator(login_required)
    def get(self, request, category_name_slug):
        category = self.get_category_name(category_name_slug)
        if category is None:
            return redirect('/rango/')

        form = PageForm()
        context_dict = {'form': form, 'category': category}
        return render(request, 'rango/add_page.html', context=context_dict)

    @method_decorator(login_required)
    def post(self, request, category_name_slug):
        category = self.get_category_name(category_name_slug)
        if category is None:
            return redirect('/rango/')

        form = PageForm(request.POST)

        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()

                return redirect(reverse('rango:show_category', kwargs={'category_name_slug': category_name_slug}))
        else:
            print(form.errors)
        context_dict = {'form': form, 'category': category}
        return render(request, 'rango/add_page.html', context=context_dict)


class RestrictedView(View):
    @method_decorator(login_required)
    def get(self, request):
        return render(request, 'rango/restricted.html')


class SearchView(View):
    @method_decorator(login_required)
    def post(self, request):
        """

        :param request: object containing metadata about the request
        :return: Given template rendered with the given context
        """
        result_list = []
        query = ''

        # strip() removes any whitespace
        query = request.POST['query'].strip()

        if query:
            result_list = run_query(query)

        return render(request, 'rango/search.html', {'result_list': result_list, 'query': query})


class GotoView(View):
    @method_decorator(login_required)
    def get(self, request):
        page_id = request.GET.get('page_id')

        try:
            selected_page = Page.objects.get(id=page_id)
        except Page.DoesNotExist:
            return redirect(reverse('rango:index'))

        selected_page.views = selected_page.views + 1
        selected_page.save()

        return redirect(selected_page.url)


class RegisterProfileView(View):
    @method_decorator(login_required)
    def get(self, request):
        form = UserProfileForm()
        context_dict = {'form': form}
        return render(request, 'rango/profile_registration.html', context_dict)

    @method_decorator(login_required)
    def post(self, request):
        form = UserProfileForm(request.POST, request.FILES)

        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = request.user
            user_profile.save()

            return redirect(reverse('rango:index'))
        else:
            print(form.errors)

        context_dict = {'form': form}
        return render(request, 'rango/profile_registration.html', context_dict)


class ProfileView(View):
    def get_user_details(self, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None

        user_profile = UserProfile.objects.get_or_create(user=user)[0]
        form = UserProfileForm({'website': user_profile.website,
                                'picture': user_profile.picture})

        return user, user_profile, form

    @method_decorator(login_required)
    def get(self, request, username):
        try:
            (user, user_profile, form) = self.get_user_details(username)
        except TypeError:
            return redirect(reverse('rango:index'))

        context_dict = {'user_profile': user_profile,
                        'selected_user': user,
                        'form': form}

        return render(request, 'rango/profile.html', context_dict)

    @method_decorator(login_required)
    def post(self, request, username):
        try:
            (user, user_profile, form) = self.get_user_details(username)
        except TypeError:
            return redirect(reverse('rango:index'))

        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)

        if form.is_valid():
            form.save(commit=True)
            return redirect(reverse('rango:profile',
                                    kwargs={'username': username}))
        else:
            print(form.errors)

        context_dict = {'user_profile': user_profile,
                        'selected_user': user,
                        'form': form}

        return render(request, 'rango/profile.html', context_dict)


class ListProfilesView(View):
    @method_decorator(login_required)
    def get(self, request):
        profiles = UserProfile.objects.all()

        return render(request, 'rango/list_profiles.html', {'user_profile_list': profiles})


# A helper method
def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val


def visitor_cookie_handler(request):
    # Get number of visits to the site.  We use COOKIES.get() function to obtain visits cookie.
    # If cookie exists, value returned is casted to an integer.
    # If cookie doesn't exist, default value of 1 is used.
    # request.COOKIES.get() returns a string
    visits = int(get_server_side_cookie(request, 'visits', '1'))
    last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')

    # If it's been more than a day since the last visit...
    if (datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
        # Update the last visit cookie now that we have updated the count
        request.session['last_visit'] = str(datetime.now())
    else:
        # Set the last visit cookie
        request.session['last_visit'] = last_visit_cookie
        # Update/set the visits cookie
    request.session['visits'] = visits


# def register(request):
#     # Boolean value for telling the template whether registration was successful.
#     # False initially, True if registration succeeds
#     registered = False
#
#     # If HTTP POST, we're interested in processing form data
#     if request.method == 'POST':
#         # Attempt to grab info from the row form info.
#         # Note that we make use of both UserForm and UserProfileForm.
#         user_form = UserForm(request.POST)
#         profile_form = UserProfileForm(request.POST)
#
#         # If the two forms are valid...
#         if user_form.is_valid() and profile_form.is_valid():
#             # Save user's form data to the database.
#             user = user_form.save()
#
#             # Now we hash the password with the set_password method.
#             # Once hashed, we can update the user object.
#             user.set_password(user.password)
#             user.save()
#
#             # Now sort out the UserProfile instance.
#             # Since we need to set the user attribute ourselves, commit=False.
#             # This delays saving model until we're ready to avoid integrity problems.
#             profile = profile_form.save(commit=False)
#             profile.user = user
#
#             # Did the user provide a profile pic? # If yes, we need to get it from input and
#             # put it in the UserProfile model.
#             if 'picture' in request.FILES:
#                 profile.picture = request.FILES['picture']
#
#             # Now we save the UserProfile model instance.
#             profile.save()
#
#             # Update our variable to indicate that the template registration was successful.
#             registered = True
#         else:
#             # Invalid form or forms - mistakes or something else?
#             # Print problems to the terminal.
#             print(user_form.errors, profile_form.errors)
#     else:
#         # Not a HTTP POST, so we render our form using two ModelForm instances.
#         # These forms will be blank, ready for user input.
#         user_form = UserForm()
#         profile_form = UserProfileForm()
#
#     # Render the templeate depending on the context.
#     return render(request, 'rango/register.html',
#                   context={'user_form': user_form, 'profile_form': profile_form, 'registered': registered})
#
#
# def user_login(request):
#     # If the request is a HTTP POST, try to pull out the relevant info.
#     if request.method == 'POST':
#         # Gather the username and password provided by the user.
#         # This information is obtained from the login form.
#         # We use request.POST.get('<variable>') as opposed
#         # to request.POST['<variable>'], because the
#         # request.POST.get('<variable>') returns None if the
#         # value does not exist, while request.POST['<variable>']
#         # will raise a KeyError exception.
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#
#         # Use Django's machinery to attempt to see if the username/password
#         # combo is valid - a User object is returned if it is.
#         user = authenticate(username=username, password=password)
#
#         # If we have a User object, the details are correct.
#         # If None (Python's way of representing the absence of a value), no user
#         # with matching credentials was found.
#         if user:
#             # Is the account active? It could have been disabled.
#             if user.is_active:
#                 # If the account is valid and active, we can log the user in.
#                 # We'll send the user back to the homepage.
#                 login(request, user)
#                 return redirect(reverse('rango:index'))
#             else:
#                 # Inactive account was used, no logging in!
#                 return HttpResponse("Your Rango account is disabled.")
#         else:
#             # Bad login details were provided.  So we can't log the user in.
#             print(f"Invalid login details: {username}, {password}")
#             return HttpResponse("Invalid login details supplied.")
#     # The request is not a HTTP POST, so display login form.
#     # This scenario would most likely be a HTTP GET.
#     else:
#         # No context variables to pass to the template system, hence the
#         # blank dictionary object...
#         return render(request, 'rango/login.html')


# # Use the login_required() decorator to ensure only those logged in can
# # access the view.
# @login_required
# def user_logout(request):
#     # Since we know the user is logged in, we can now just log them out.
#     logout(request)
#     # Take the user back to the homepage.
#     return redirect(reverse('rango:index'))
