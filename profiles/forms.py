from django import forms
from django.contrib.auth.models import User
from .models import Profile, Skill, Area




class ProfileModelForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio', 'dp','cp',  'work_area','skills', 'pay_rate', 'occupation', 'education', 'credit_card_no', 'phone_no')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['skills'].queryset = Skill.objects.none()
        if 'work_area' in self.data:
            try:
                area_id = int(self.data.get('work_area'))
                self.fields['skills'].queryset = Skill.objects.filter(area_id=area_id)
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password',
                                widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']


class FreelancerRegistrationForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('occupation', 'education', 'dp', 'cp', 'credit_card_no', 'bio', 'phone_no', 'work_area', 'skills', 'pay_rate')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['skills'].queryset = Skill.objects.none()
        if 'work_area' in self.data:
            try:
                area_id = int(self.data.get('work_area'))
                self.fields['skills'].queryset = Skill.objects.filter(area_id=area_id)
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset



class ClientRegistrationForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('occupation', 'company', 'dp', 'cp', 'bio', 'credit_card_no', 'phone_no')