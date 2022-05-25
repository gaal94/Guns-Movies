from tkinter import Widget
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
        fields = ['title', 'rank', 'content',]
        

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        exclude = ['review', 'user',]
        widgets = {
            'content': forms.TextInput(
                attrs={
                    'style': 'width: 500px; height: 40px;',
                    'placeholder': '내용을 작성해주세요.',
                }
            )
        }