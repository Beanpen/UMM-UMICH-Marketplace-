from django import forms

# TODO: I added ImageFormSet
# from django.forms import formset_factory
# class ImageUploadForm(forms.Form):
#     pic = forms.FileField(widget=forms.ClearableFileInput(attrs={"multiple": True}))
# ImageFormSet = formset_factory(ImageUploadForm, extra=3)  # Change `extra` according to your needs


CATEGORY_CHOICES = (
    ('electronic_device', 'Electronic Device'),
    ('health_beauty', 'Health & Beauty'),
    ('fashion', 'Fashion'),
    ('sports', 'Sports'),
    ('groceries', 'Groceries'),
    ('food', 'Food'),
    ('book', 'Book'),
    ('stationary', 'Stationary'),
    ('others', 'Others')
)

ACCEPT_DECLINE_CHOICES = (
    ('1', 'Accept'),
    ('2', 'Decline')
)


class postForm(forms.Form):
    productname = forms.CharField(max_length=100)
    price = forms.FloatField()
    quantity = forms.IntegerField()
    category = forms.ChoiceField(choices=CATEGORY_CHOICES)
    description = forms.CharField(max_length=200, widget=forms.Textarea)
    pic = forms.FileField(required = True)
    # TODO: this is broke. check out "Saved progress on multi-image upload" in products/views.py
    # pics = forms.FileField(widget=forms.ClearableFileInput(attrs={"allow_multiple_selected": True}), required=False)

class OrderForm(forms.Form):
    message = forms.CharField(max_length=250, widget=forms.Textarea)
    quantity = forms.IntegerField()

class confirmationForm(forms.Form):
    Options = forms.ChoiceField(widget=forms.RadioSelect, choices=ACCEPT_DECLINE_CHOICES)

class updateForm(forms.Form):
    new_price = forms.FloatField()
    new_quantity = forms.IntegerField()
    new_description = forms.CharField(max_length=200, widget=forms.Textarea)
