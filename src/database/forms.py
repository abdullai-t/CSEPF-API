from django import forms
from .models import Testimonial


class TestimonialForm(forms.ModelForm):
	class Meta:
		model = Testimonial
		fields = ['user', 'content', "is_featured"]
