from django import forms


class OrderForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields["warehouse"] = forms.IntegerField(label="Sklad")
        self.fields["time"] = forms.DateTimeField(label="Odjezd")
        self.fields["amount"] = forms.IntegerField(label="Množství (ks)", min_value=0)
        self.fields["material"] = forms.CharField(label="Material", widget=forms.TextInput(
            attrs={"list": "materials-list"}
        ))

    def clean(self):
        super().clean()