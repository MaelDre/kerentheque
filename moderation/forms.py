from django import forms


class ReportForm(forms.Form):
    TARGET_CHOICES = [("item", "Cet objet"), ("user", "Son propriétaire")]

    target = forms.ChoiceField(label="Que signalez-vous ?", choices=TARGET_CHOICES, widget=forms.RadioSelect, initial="item")
    reason = forms.CharField(
        label="Motif",
        max_length=1000,
        widget=forms.Textarea(attrs={"rows": 4, "maxlength": 1000}),
        error_messages={"required": "Indiquez le motif du signalement."},
    )
