from django import forms


class ContactRequestForm(forms.Form):
    message = forms.CharField(
        label="Message",
        required=False,
        max_length=500,
        widget=forms.Textarea(attrs={"rows": 3, "maxlength": 500, "placeholder": "Ex. : ce serait pour samedi, pour deux heures."}),
    )
    consent = forms.BooleanField(
        label="J'accepte que mes coordonnées ci-dessus soient transmises au propriétaire",
        required=True,
        error_messages={"required": "Vous devez accepter la transmission de vos coordonnées pour envoyer la demande."},
    )
