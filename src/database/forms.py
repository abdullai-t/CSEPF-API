from django import forms
from .models import Project, Testimonial


class TestimonialForm(forms.ModelForm):
	class Meta:
		model = Testimonial
		fields = ['fellow', 'content', "media","is_featured"]
		

class ProjectForm(forms.ModelForm):
	class Meta:
		model = Project
		fields = ["fellow", 'title', 'summary', 'document', 'is_featured']
		widgets = {
			'summary': forms.Textarea(attrs={'rows': 5})
		}
