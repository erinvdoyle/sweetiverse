from django import forms

CANDY_CHOICES = [
    ('chocolate', 'Chocolate'),
    ('hard', 'Hard Candy'),
    ('gummies', 'Gummies'),
    ('chewy', 'Chewy Candy'),
    ('gum', 'Gum'),
]

FREQ_CHOICES = [
    ('monthly', 'Every Month'),
    ('bimonthly', 'Every 2 Months'),
]

class SubscriptionForm(forms.Form):
    candy_types = forms.MultipleChoiceField(
        choices=CANDY_CHOICES, 
        widget=forms.CheckboxSelectMultiple,
        label="My Favorite Sweetis"
    )
    flavor_preferences = forms.MultipleChoiceField(
        choices=[],
        widget=forms.CheckboxSelectMultiple,
        label="My Favorite Flavors"
    )
    frequency = forms.ChoiceField(choices=FREQ_CHOICES, widget=forms.RadioSelect)

class PickNMixForm(forms.Form):
    CANDY_TYPE_CHOICES = [
        ('chocolate', '🍫 Chocolate'),
        ('hard_candy', '🍬 Hard Candy'),
        ('gummies', '🐻 Gummies'),
        ('chewy', '🌀 Chewy Candy'),
        ('gum', '💨 Gum'),
    ]

    DELIVERY_CHOICES = [
        ('weekly', 'Weekly'),
        ('biweekly', 'Every 2 Weeks'),
        ('monthly', 'Monthly'),
    ]

    sweet_types = forms.MultipleChoiceField(
        choices=CANDY_TYPE_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        label="My Favorite Sweetis (Pick 1 or 2)",
    )

    flavor_preferences = forms.MultipleChoiceField(
        choices=[],
        widget=forms.CheckboxSelectMultiple,
        label="My Favorite Flavors (Pick 1 or 2)"
    )

    explorer = forms.BooleanField(
        required=False,
        label="Include Sweeti Explorer? (Surprise Picks!)"
    )

    delivery_frequency = forms.ChoiceField(
        choices=DELIVERY_CHOICES,
        widget=forms.RadioSelect,
        label="Choose Delivery Frequency"
    )