from .models import Tweet

from django import forms

MAX_SPIRIT_LENGTH = 240
class SpiritForm(forms.ModelForm):
        class Meta:
            model = Tweet
            fields = ['content']

        def clean_content(self):
            content = self.cleaned_data.get('content')
            if len(content) > MAX_SPIRIT_LENGTH:
                raise forms.ValidationError("This tweet is too long")
            return content

