from django import forms
from emoji_picker.widgets import EmojiPickerTextareaAdmin
from .models import Commentaire_Article, Commentaire_Video, Abonnee
from django.core.validators import RegexValidator



class CommentFormArticle(forms.ModelForm):
    class Meta:  
        model = Commentaire_Article
        fields = ('nom', 'commentaire')
        
    def clean_nom(self):
        nom = self.cleaned_data['nom']
        if len(nom) < 2:
            raise forms.ValidationError("Le nom doit comporter au moins 3 caractères")
        return nom
        
    def clean_commentaire(self):
        commentaire = self.cleaned_data['commentaire']
        if len(commentaire) < 6:
            raise forms.ValidationError("Le commentaire doit comporter au moins 10 caractères")
        return commentaire
    


class CommentFormVideo(forms.ModelForm):
    class Meta:
        model = Commentaire_Video
        fields = ('nom', 'commentaire')
        
    def clean_nom(self):
        nom = self.cleaned_data['nom']
        if len(nom) < 2:
            raise forms.ValidationError("Le nom doit comporter au moins 3 caractères")
        return nom
        
    def clean_commentaire(self):
        commentaire = self.cleaned_data['commentaire']
        if len(commentaire) < 6:
            raise forms.ValidationError("Le commentaire doit comporter au moins 10 caractères")
        return commentaire
    
    
class AbonneeForm(forms.ModelForm):
    class Meta:
        model = Abonnee
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={
                'placeholder': 'Enter your email',
                'class': 'px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 mb-4',
                'required': True,
            })
        }
