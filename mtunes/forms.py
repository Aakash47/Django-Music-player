from django import forms
from . models import Song

class UploadSongForm(forms.ModelForm):
    class Meta:
        model = Song
        exclude =['song_id','uploaded_by',]