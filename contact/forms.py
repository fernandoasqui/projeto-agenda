from django import forms
from contact.models import Contact
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import password_validation


class ContactForm(forms.ModelForm):
    # edita o formato do campo do forms no html

    picture = forms.ImageField(
        widget=forms.FileInput(
            attrs={
                'accept': 'image/*',
            }
        ),
        required=False
    )

    class Meta:
        model = Contact
        fields = ('first_name', 'last_name', 'email',
                  'phone', 'description', 'category', 'picture',)

    def clean(self):

        return super().clean()

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')

        if first_name == 'ABC':
            raise ValidationError('Não digite ABC', code='invalid')
        return first_name


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(
        required=True,
        min_length=3
    )
    last_name = forms.CharField(
        required=True,
        min_length=3
    )
    email = forms.EmailField(
        required=True,
        min_length=3
    )

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'email',
            'username', 'password1', 'password2'
        )

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            self.add_error(
                'email',
                ValidationError('Email já cadastrado', code='invalid')
            )
        return email


class RegisterUpdateForm(forms.ModelForm):
    first_name = forms.CharField(
        required=True,
        min_length=2,
        max_length=30,
        help_text='Required.',
        error_messages={
            'min_lenght': 'Please, add more than 2 letters.'
        }
    )
    last_name = forms.CharField(
        required=True,
        min_length=2,
        max_length=30,
        help_text='Required.',
    )
    password1 = forms.CharField(
        label='Password',
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text=password_validation.password_validators_help_text_html(),
        required=True,
    )
    password2 = forms.CharField(
        label='Password 2',
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text='Use the same password as before.',
        required=False,
    )

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'email', 'username'
        )

    def save(self, commit=True):
        cleaned_data = self.cleaned_data
        user = super().save(commit=False)

        password = cleaned_data.get('password1')

        if password:
            # seta a nova senha do user
            user.set_password(password)

        if commit:
            user.save()

        return user

    def clean(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 or password2:
            if password1 != password2:
                self.add_error(
                    'password2',
                    ValidationError('Passwords do not match', code='invalid')
                )

        return super().clean()

    def clean_email(self):
        email = self.cleaned_data.get('email')
        current_email = self.instance.email

        if current_email != email:

            if User.objects.filter(email=email).exists():
                self.add_error(
                    'email',
                    ValidationError('Email já cadastrado', code='invalid')
                )
        return email

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if password1:
            try:
                password_validation.validate_password(password1)
            except ValidationError as errors:
                self.add_error('password1', ValidationError(errors))

        return password1
