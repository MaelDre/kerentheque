from django import forms
from django.db.models import Q

from .models import Neighborhood, User


class LoginForm(forms.Form):
    email = forms.EmailField(label="Votre adresse email", widget=forms.EmailInput(attrs={"autofocus": True}))

    def clean_email(self):
        return self.cleaned_data["email"].strip().lower()


class ProfileForm(forms.ModelForm):
    accept_terms = forms.BooleanField(
        label="J'accepte les conditions d'utilisation et la politique de confidentialité",
        required=False,
    )

    class Meta:
        model = User
        fields = ["pseudo", "neighborhood", "phone", "share_email", "share_phone"]
        labels = {"phone": "Téléphone"}
        help_texts = {
            "pseudo": "Visible par tous. Entre 3 et 30 caractères.",
            "neighborhood": "Visible par tous, pour indiquer approximativement où vous vous trouvez.",
            "phone": "Jamais affiché publiquement.",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["pseudo"].required = True
        self.fields["neighborhood"].required = True
        self.fields["neighborhood"].empty_label = "Choisissez votre quartier"
        # Un quartier désactivé n'est plus proposé, sauf s'il est déjà celui de l'utilisateur.
        self.fields["neighborhood"].queryset = Neighborhood.objects.filter(
            Q(is_active=True) | Q(pk=self.instance.neighborhood_id)
        )
        if self.instance.terms_accepted_at:
            del self.fields["accept_terms"]

    def clean_pseudo(self):
        pseudo = self.cleaned_data["pseudo"].strip()
        if not 3 <= len(pseudo) <= 30:
            raise forms.ValidationError("Le pseudo doit contenir entre 3 et 30 caractères.")
        if User.objects.filter(pseudo__iexact=pseudo).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Ce pseudo est déjà utilisé.")
        return pseudo

    def clean_phone(self):
        return self.cleaned_data["phone"].strip()

    def clean_accept_terms(self):
        if not self.cleaned_data["accept_terms"]:
            raise forms.ValidationError(
                "Vous devez accepter les conditions d'utilisation et la politique de confidentialité."
            )
        return True

    def clean(self):
        cleaned = super().clean()
        share_email, share_phone = cleaned.get("share_email"), cleaned.get("share_phone")
        if not share_email and not share_phone:
            raise forms.ValidationError("Choisissez au moins un moyen de contact à partager.")
        if share_phone and not cleaned.get("phone"):
            self.add_error("share_phone", "Renseignez un numéro de téléphone pour pouvoir le partager.")
        return cleaned
