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
                'style': 'width: 75px; height: 29px;'
            }
        )
    )

    class Meta:
        model = Review
        fields = ['title', 'rank', 'content',]
        widgets = {
            'title': forms.TextInput(
                attrs={
                    'style': 'width: 634px; height: 29px;',
                }
            ),
            'content': forms.Textarea(
                attrs={
                    'style': 'width: 634px; height: 283px; resize: none;',
                }
            )
        }
        

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        exclude = ['review', 'user',]
        widgets = {
            'content': forms.Textarea(
                attrs={
                    'style': 'width: 500px; height: 120px; resize: none;',
                    'placeholder': '내용을 작성해주세요.',
                }
            )
        }