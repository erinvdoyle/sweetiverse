from django import forms
from .models import Sweet, Category
from .widgets import CustomClearableFileInput


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
