from django import forms
from .models import ContactSubmission

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactSubmission
        fields = ['name', 'email', 'phone', 'reason', 'source', 'message']
        widgets = {
            'reason': forms.Select(attrs={'class': 'form-select'}),
            'source': forms.Select(attrs={'class': 'form-select'}),
            'message': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Make fields required explicitly
        self.fields['reason'].required = True
        self.fields['source'].required = True

        # Remove Django's default empty choice and add your custom placeholder
        self.fields['reason'].choices = [('', 'Reason to contact')] + list(self.fields['reason'].choices)[1:]
        self.fields['source'].choices = [('', 'How did you find out about us?')] + list(self.fields['source'].choices)[1:]

        # Add placeholders for inputs
        self.fields['name'].widget.attrs.update({'placeholder': 'Name'})
        self.fields['email'].widget.attrs.update({'placeholder': 'E-mail Address'})
        self.fields['phone'].widget.attrs.update({'placeholder': 'Phone Number'})
        self.fields['message'].widget.attrs.update({'placeholder': 'Message'})
