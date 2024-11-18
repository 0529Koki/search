from django import forms
from .models import Product

#検索キーワードを送信するためのフォームクラスを定義
class SearchForm(forms.Form):
    query = forms.CharField(
        label='検索ワード',#フォームのラベル名を定義
        max_length=100,#最大100文字のテキスト入力が可能
        required=False,
        widget=forms.TextInput(attrs={'placeholder': '検索したいキーワードを入力'}
        )
    )

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'category']