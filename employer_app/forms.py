from django import forms
from job_easy.models import job

class AddJobPostForm(forms.ModelForm):

    class Meta:
        model = job
        exclude = ('user', 'post_date', 'applications')
