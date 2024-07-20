from django import forms
from .models import Presentation, Project, Staff, Testimonial, UserProfile


class TestimonialForm(forms.ModelForm):
	class Meta:
		model = Testimonial
		fields = ['fellow', 'content', "media", "is_featured", "tags"]
		widgets = {
			'content': forms.Textarea(attrs={'rows': 5}),
			'tags': forms.CheckboxSelectMultiple(),
		}


class ProjectForm(forms.ModelForm):
	class Meta:
		model = Project
		fields = ["fellow", 'title', 'summary', 'document', 'is_featured', "topics"]
		widgets = {
			'summary': forms.Textarea(attrs={'rows': 5}),
			'topics': forms.CheckboxSelectMultiple(),
		}


class StaffForm(forms.ModelForm):
	class Meta:
		model = Staff
		fields = ['user', 'role', 'bio', 'is_featured']
		widgets = {
			'bio': forms.Textarea(attrs={'rows': 5})
		}


class UserProfileForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = ['full_name', 'email', 'picture']
		

class PresentationForm(forms.ModelForm):
	class Meta:
		model = Presentation
		fields = ['title', 'presenter', 'email', 'picture', 'cohort', 'summary', 'document', "is_featured"]
		widgets = {
			'summary': forms.Textarea(attrs={'rows': 5}),
		}
