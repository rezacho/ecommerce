from django import forms
from .models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField


class UserCreationForm(forms.ModelForm):
	password1 = forms.CharField(label='password', widget=forms.PasswordInput)
	password2 = forms.CharField(label='confirm password', widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = ('email', 'phone_number', 'full_name')

	def clean_password2(self):
		password1 = self.cleaned_data.get("password1")
		password2 = self.cleaned_data.get("password2")
		if password1 and password2 and password1 != password2:
			raise ValidationError("Passwords don't match")
		return password2

	def save(self, commit=True):
		user = super().save(commit=False)
		user.set_password(self.cleaned_data['password1'])
		if commit:
			user.save()
		return user


class UserChangeForm(forms.ModelForm):
	password = ReadOnlyPasswordHashField(help_text="Change password using <a href=\"../password/\">this form</a>.")

	class Meta:
		model = User
		fields = ('email', 'phone_number', 'full_name', 'password', 'last_login')


class UserRegistrationForm(forms.Form):
	email = forms.EmailField()
	full_name = forms.CharField(label='full name')
	phone_number = forms.CharField(max_length=11)
	password = forms.CharField(widget=forms.PasswordInput)

	def clean_email(self):
		email = self.cleaned_data['email']
		user = User.objects.filter(email=email).exists()
		if user:
			raise ValidationError('This email already exists')
		return email

	def clean_phone(self):
		phone = self.cleaned_data['phone_number']
		user = User.objects.filter(phone_number=phone).exists()
		if user:
			raise ValidationError('This phone number already exists')
		return phone


class VerifyCodeForm(forms.Form):
	code = forms.IntegerField()
