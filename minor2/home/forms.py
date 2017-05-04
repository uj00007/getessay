from django import forms


class EssayForm(forms.Form):
    title = forms.CharField(label='', max_length=100,widget=forms.TextInput(attrs={'placeholder':'                     enter essay title','class':'row','style':'border-bottom-style:ridge;border:0;outline:0;background:transparent;border-bottom-left-radius:initial;border-bottom-right-radius:initial;border-bottom:3px solid grey;margin-left:100px;'}))
    length = forms.IntegerField(label='',widget=forms.TextInput(attrs={'placeholder':'                      no. of sentences','class':'row','style':'border-bottom-style:ridge;border:0;outline:0;background:transparent;border-bottom-left-radius:initial;border-bottom-right-radius:initial;border-bottom:3px solid grey;margin-left:100px;'}))
