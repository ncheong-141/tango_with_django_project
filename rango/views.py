from django.shortcuts import render
from django.http import HttpResponse

# Import catagory model
from rango.models import Category
from rango.models import Page

# Import form models
from rango.forms import CategoryForm
from rango.forms import PageForm
from rango.forms import UserForm, UserProfileForm

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse

def index(request): 

    # Query the database for a list of ALL categories currently stored.
    # Order the categories by the number of likes in descending order.
    # Retrieve the top 5 only -- or all if less than 5.
    # Place the list in our context_dict dictionary (with our boldmessage!)
    # that will be passed to the template engine.
    category_list = Category.objects.order_by('-likes')[:5]
    pages= Page.objects.order_by('-views')[:5]

    context_dict = {}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['categories'] = category_list
    context_dict['pages'] = pages

    print(context_dict)
    # Return a rendered response to send to the client.
    return render(request, 'rango/index.html', context=context_dict)

def about(request):
    # prints out whether the method is a GET or a POST
    print(request.method)

    # prints out the user name, if no one is logged in it prints `AnonymousUser`
    print(request.user)
    
    # {} since render requires a dictionary parameter, passing an empty dictionary
    return render(request, 'rango/about.html', {})

# Show the category when selected 
def show_category(request, category_name_slug):
    
    # Create a context dictionary which we can pass
    # to the template rendering engine.
    context_dict = {}
    try:
        # Can we find a category name slug with the given name?
        # If we can't, the .get() method raises a DoesNotExist exception.
        # The .get() method returns one model instance or raises an exception.
        category = Category.objects.get(slug=category_name_slug)

        # Retrieve all of the associated pages.
        # The filter() will return a list of page objects or an empty list.
        pages = Page.objects.filter(category=category)

        # Adds our results list to the template context under name pages.
        context_dict['pages'] = pages
        
        # We also add the category object from
        # the database to the context dictionary.
        # We'll use this in the template to verify that the category exists.
        context_dict['category'] = category
        
    except Category.DoesNotExist:
        # We get here if we didn't find the specified category.
        # Don't do anything -
        # the template will display the "no category" message for us.
        context_dict['category'] = None
        context_dict['pages'] = None
    
    # Go render the response and return it to the client.
    return render(request, 'rango/category.html', context=context_dict)

@login_required
def add_category(request):
    
    form = CategoryForm()
    
    # A HTTP POST?
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        
        # Is the form valid?
        if form.is_valid():

            # Save the new category to the database.
            form.save(commit=True)

            # Redirect to index page if sucessful
            return redirect('/rango/')
        else:
            # The supplied form contained errors -# just print them to the terminal.
            print(form.errors)

    # Will handle the bad form, new form, or no form supplied cases.
    # Render the form with error messages (if any).
    return render(request, 'rango/add_category.html', {'form': form})

@login_required
def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None
    
    # You cannot add a page to a Category that does not exist...
    if category is None:
        return redirect('/rango/')
    
    form = PageForm()

    if request.method == 'POST':
        form = PageForm(request.POST)
        
        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()
                
                return redirect(reverse('rango:show_category',kwargs={'category_name_slug': category_name_slug}))
        else:
            print(form.errors)
    
    # Set context dict
    context_dict = {'form': form, 'category': category}
    
    return render(request, 'rango/add_page.html', context=context_dict)


def register(request):

    # Boolean variable to define if a user has been registered (switch to true when successful)
    registered = False

    # If its a http post, process form data
    if request.method == 'POST':

        # Try to get information from the form 
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        # If both forms are valid
        if user_form.is_valid() and profile_form.is_valid():

            # Save the form data to the database
            user = user_form.save()

            # Hash the password with the set_password method of the User model from django
            user.set_password(user.password)
            user.save() 

            # Set user attributes. Delay saving the model to avoid integrity problems 
            profile = profile_form.save(commit=False)
            profile.user = user 

            # If the user saved a profile picture, get it from the input form
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
                
            # With that dealt with, now can safe
            profile.save()

            # Set registration boolean to true to indicate success
            registered = True
        else:
                
            # Invalid form, print problems to termminal
            print(user_form.errors, profile_form.errors)
    else:
        # Not a HTTP POST (get instead), render our forms using ModelForm instances. 
        # Outputs blank forms for user input 

        user_form = UserForm()
        profile_form = UserProfileForm()

    # render the template depending on the context from the control flow above
    return render(request,'rango/register.html', context = {'user_form': user_form, 
                                                            'profile_form': profile_form,
                                                            'registered': registered})


def user_login(request):
    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':

        # Gather the username and password provided by the user.
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Django function to check if username and password is correct
        user = authenticate(username=username, password=password)
        
        # If we have a User object, the details are correct.
        if user:

            # Check if account is active (not disabled)
            if user.is_active:

                # If the account is valid and active, we can log the user in and send back to homepage
                login(request, user)
                return redirect(reverse('rango:index'))
            else:
                # Account is innactive
                return HttpResponse("Your Rango account is disabled.")
        else:
            # Invalid login details, 
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    
    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system
        return render(request, 'rango/login.html')

@login_required
def restricted(request):
    return render(request, 'rango/restricted.html')

@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)
   
    # Take the user back to the homepage.
    return redirect(reverse('rango:index'))