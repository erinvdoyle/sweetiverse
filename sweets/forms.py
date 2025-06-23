from django import forms
from .models import Sweet, Category, SweetReview
from .widgets import CustomClearableFileInput
from django.core.exceptions import ValidationError


class SweetForm(forms.ModelForm):
    class Meta:
        model = Sweet
        fields = '__all__'
        widgets = {
            'image': CustomClearableFileInput()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if 'categories' in self.fields:
            categories = Category.objects.all()
            self.fields['categories'].queryset = categories
            self.fields['categories'].label_from_instance = lambda obj: obj.get_friendly_name()

        for field_name, field in self.fields.items():
            css_classes = 'form-control border-pink rounded-pill shadow-sm'

            if isinstance(field.widget, forms.Textarea):
                css_classes += ' ps-4'
                field.widget.attrs['style'] = 'padding-left: 1.25rem;'
                field.widget.attrs['rows'] = 4

            if not isinstance(field.widget, CustomClearableFileInput):
                field.widget.attrs['class'] = css_classes

    def clean(self):
        cleaned_data = super().clean()
        price = cleaned_data.get('price')
        quantity = cleaned_data.get('quantity')

        if price is not None and price < 0:
            self.add_error('price', ValidationError("Price cannot be negative."))

        if quantity is not None and quantity < 0:
            self.add_error('quantity', ValidationError("Quantity cannot be negative."))

        return cleaned_data


class SweetReviewForm(forms.ModelForm):
    RATING_CHOICES = [
        (5, '⭐️⭐️⭐️⭐️⭐️'),
        (4, '⭐️⭐️⭐️⭐️'),
        (3, '⭐️⭐️⭐️'),
        (2, '⭐️⭐️'),
        (1, '⭐️'),
    ]

    rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'star-rating'}),
        label="Your Rating"
    )

    class Meta:
        model = SweetReview
        fields = ['rating', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write your thoughts...'}),
        }


class SweetiSelectorForm(forms.Form):
    fruity_vs_chocolate = forms.BooleanField(
        required=False,
        label="",
        widget=forms.CheckboxInput(attrs={'class': 'django-toggle fruity'})
    )
    texture = forms.BooleanField(
        required=False,
        label="",
        widget=forms.CheckboxInput(attrs={'class': 'django-toggle texture'})
    )
    flavor_age = forms.BooleanField(
        required=False,
        label="",
        widget=forms.CheckboxInput(attrs={'class': 'django-toggle flavor-age'})
    )
    popularity = forms.BooleanField(
        required=False,
        label="",
        widget=forms.CheckboxInput(attrs={'class': 'django-toggle popularity'})
    )