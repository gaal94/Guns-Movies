from django import forms
from .models import Review, Comment


class ReviewForm(forms.ModelForm):
    rank = forms.FloatField(
        min_value=0,
        max_value=5,
        widget=forms.NumberInput(
            attrs={
                'step': 0.5,
            }
        )
    )

    class Meta:
        model = Review
        fields = ['title', 'rank', 'content']
        

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        exclude = ['review', 'user']
