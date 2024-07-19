from django import forms
from .models import Testimonial


class TestimonialForm(forms.ModelForm):
	class Meta:
		model = Testimonial
		fields = ['fellow', 'content', "is_featured"]
