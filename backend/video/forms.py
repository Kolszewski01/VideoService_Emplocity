from django import forms
from .models import Video
import tempfile
from django.core.exceptions import ValidationError
from moviepy.editor import VideoFileClip
from PIL import Image
import io
from django.core.files.base import ContentFile


def generate_thumbnail(video_file):
    try:
        # Zapisz plik wideo tymczasowo na dysku
        with tempfile.NamedTemporaryFile(suffix='.mp4') as temp_video:
            for chunk in video_file.chunks():
                temp_video.write(chunk)

            # Utwórz obiekt VideoFileClip
            clip = VideoFileClip(temp_video.name)

            # Wybierz klatkę z czasu t=1 (1 sekunda)
            frame = clip.get_frame(1)

            # Konwertuj klatkę na obraz PIL
            image = Image.fromarray(frame)

            # Zapisz obraz jako JPEG do pamięci
            thumbnail_bytes = io.BytesIO()
            image.save(thumbnail_bytes, format='JPEG')

            # Zwróć miniaturkę jako obiekt ContentFile
            thumbnail_content = ContentFile(thumbnail_bytes.getvalue())

        return thumbnail_content
    except Exception as e:
        raise forms.ValidationError("Błąd podczas generowania miniaturki: {}".format(str(e)))


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
                raise forms.ValidationError("Dozwolone rozszerzenia to: MP4, MOV, AVI, WMV.")

            thumbnail = generate_thumbnail(video_file)

            # Przypisz miniaturkę do pola thumbnail w instancji formularza
            self.instance.thumbnail.save(video_file.name + '.png', thumbnail, save=False)

        return video_file