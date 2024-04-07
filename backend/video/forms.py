from django import forms
from .models import Video, Comment
from django.core.exceptions import ValidationError


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)


class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'video_file', 'description', 'type', 'tags']
        labels = {
            'title': 'Tytuł',
            'video_file': 'Plik wideo',
            'description': 'Opis',
            'type': 'Typ',
            'tags': 'Tagi',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'video_file': forms.FileInput(attrs={'class': 'form-control-file'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'tags': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tag1, Tag2, Tag3'}),
        }

    def clean_video_file(self):
        video_file = self.cleaned_data.get('video_file', False)
        if video_file:
            allowed_extensions = ['mp4', 'mov', 'avi', 'wmv']
            file_extension = video_file.name.split('.')[-1].lower()
            if file_extension not in allowed_extensions:
                raise ValidationError("Dozwolone rozszerzenia to: MP4, MOV, AVI, WMV.")
        return video_file
