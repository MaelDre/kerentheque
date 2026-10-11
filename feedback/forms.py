from django import forms


class FeedbackForm(forms.Form):
    message = forms.CharField(
        label="Votre message",
        widget=forms.Textarea(
            attrs={"rows": 6, "placeholder": "Une question, une idée d'amélioration, un commentaire..."}
        ),
        error_messages={"required": "Écrivez un message avant d'envoyer."},
    )
