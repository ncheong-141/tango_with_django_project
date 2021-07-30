from django import forms
from django.contrib.auth.models import User
from rango.models import Page, Category, UserProfile

class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=Category.maxlength_name, help_text="Please enter the category name")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug  = forms.CharField(widget=forms.HiddenInput(), required=False)

    # An inline class to provide additional information on the form
    class Meta: 
        # Provide an association between the modelform and a model
        model = Category
        fields = ('name',)


class PageForm(forms.ModelForm):
    
    title = forms.CharField(max_length=Page.maxlength_title, help_text="Please enter the title of the page.")
    url = forms.URLField(max_length=Page.maxlength_url, help_text="Please enter the URL of the page.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:

        # Provide an association between the ModelForm and a model
        model = Page

        # Hiding the forieng key from the form (can also use include and not mention category) 
        exclude = ('category',)

    def clean(self):
        cleaned_data = self.cleaned_data

        # Getting the cleaned url data from the ModelForm
        url = cleaned_data.get('url')
       
        # If url is not empty and doesn't start with 'http://',
        # then prepend 'http://'.
        if url and not url.startswith('http://'):
            url = f'http://{url}'
            cleaned_data['url'] = url
       
        return cleaned_data


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
    class Meta: 
        model = UserProfile
        fields = ('website', 'picture')

