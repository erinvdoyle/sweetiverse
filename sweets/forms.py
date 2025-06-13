from django import forms
from .models import Sweet, Category

class SweetForm(forms.ModelForm):
    class Meta:
        model = Sweet
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if 'categories' in self.fields:
            categories = Category.objects.all()
            friendly_names = [(c.id, c.get_friendly_name()) for c in categories]
            self.fields['categories'].queryset = categories
            self.fields['categories'].label_from_instance = lambda obj: obj.get_friendly_name()

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control border-pink rounded-pill shadow-sm'