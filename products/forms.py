from django import forms


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


class uploadImgForm(forms.Form):
    Upload_your_item_picture = forms.FileField(required = True)

class postForm(forms.Form):
    product_name = forms.CharField(max_length=100)
    price = forms.FloatField()
    quantity = forms.IntegerField()
    category = forms.ChoiceField(choices=CATEGORY_CHOICES)
    description = forms.CharField(max_length=500, widget=forms.Textarea)
    # pic = forms.FileField(required = True)

class OrderForm(forms.Form):
    message = forms.CharField(max_length=250, widget=forms.Textarea)
    quantity = forms.IntegerField()


class confirmationForm(forms.Form):
    Options = forms.ChoiceField(widget=forms.RadioSelect, choices=ACCEPT_DECLINE_CHOICES)


class updateForm(forms.Form):
    new_price = forms.FloatField()
    new_quantity = forms.IntegerField()
    new_description = forms.CharField(max_length=200, widget=forms.Textarea)