from django import forms

class AddLeagueForm(forms.Form):
    teamid = forms.IntegerField(label='Enter league id to add')