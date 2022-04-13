from django import forms


class OrderForm(forms.Form):
    def __init__(self):
        super().__init__()
        self.fields["amount"] = forms.IntegerField(label="Amount", min_value=0)

    def clean(self):
        super().clean()