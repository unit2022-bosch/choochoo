from django import forms


class Datalist(forms.Select):
    input_type = "text"
    template_name = "components/datalist.html"
    option_template_name = "components/datalist_options.html"
    add_id_index = False
    checked_attribute = {"selected": True}
    option_inherits_attrs = False


class DatalistField(forms.ChoiceField):
    widget = Datalist
    default_error_messages = {
        "invalid_choice": "Select a valid choice. %(value)s is not one of the available choices.",
    }

    def __init__(self, choices, **kwargs):
        super().__init__(**kwargs)
        self.choices = choices


class OrderForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["warehouse"] = forms.IntegerField(label="Sklad")
        self.fields["amount"] = forms.IntegerField(label="Množství (ks)", min_value=0)
        self.fields["material"] = forms.CharField(label="Material")
        self.fields["material"].widget = forms.TextInput(
            attrs={"list": "materials-list"}
        )

    def clean(self):
        super().clean()