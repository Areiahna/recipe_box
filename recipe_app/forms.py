from django import forms
from recipe_app.models import Recipe, Author


class AddRecipeForm(forms.Form):
    title= forms.CharField(max_length=50)
    author= forms.ModelChoiceField(queryset=Author.objects.all())
    description= forms.CharField(widget=forms.Textarea)
    instructions= forms.CharField(widget=forms.Textarea)
    time= forms.CharField(max_length=30)

class AddAuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ["name","bio"]
       
    
    
