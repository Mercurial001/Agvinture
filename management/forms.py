from .models import Section
from django.forms import Select, DateInput, Textarea, TextInput, ModelForm, SelectMultiple, NumberInput
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth import password_validation
from django.utils.translation import gettext_lazy as _


class AddSectionForm(ModelForm):
    class Meta:
        model = Section
        fields = '__all__'

