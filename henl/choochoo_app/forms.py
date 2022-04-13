from django import forms


class OrderForm(forms.Form):
    def __init__(self):
        super().__init__()
        self.fields["amount"] = forms.IntegerField(label="Množství (ks)", min_value=0)
        self.fields["material"] = forms.ChoiceField(choices=[(1, "Ano"), (1, "Ne")])

    def clean(self):
        super().clean()