from django import forms

from .models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {'comment': forms.Textarea(attrs={'rows': 3, 'maxlength': 1000})}
        help_texts = {'comment': 'Opcional. Conte como a peça chegou em relação ao anúncio.'}
