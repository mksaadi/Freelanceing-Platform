from django import forms
from .models import Post, Comment, Job , JobAppointment
from profiles.models import Skill, Area

class PostModelForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Post Something!','rows': 2}))
    class Meta:
        model = Post
        fields = ('content', 'image')


class JobModelForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Job Description!', 'rows': 2}))

    class Meta:
        model = Job
        fields = ('title', 'description', 'image', 'work_area', 'skills', 'salary')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['skills'].queryset = Skill.objects.none()
        if 'work_area' in self.data:
            try:
                area_id = int(self.data.get('work_area'))
                self.fields['skills'].queryset = Skill.objects.filter(area_id=area_id)
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset


class CommentModelForm(forms.ModelForm):
    body = forms.CharField(label="",widget=forms.TextInput(attrs={'placeholder': 'Say something inspirational'}))

    class Meta:
        model = Comment
        fields = ('body',)


class AppointmentForm(forms.ModelForm):
    content = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder': 'Congratulate Your newest Employee'}))
    class Meta:
        model = JobAppointment
        fields = ('content',)

