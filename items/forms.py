from django import forms
from django.db.models import Q

from accounts.models import Neighborhood

from .models import Category, Item


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ["name", "category", "description"]
        widgets = {"description": forms.Textarea(attrs={"rows": 5, "maxlength": 2000})}
        help_texts = {"description": "État, accessoires fournis, conditions de prêt… (2000 caractères maximum)"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["category"].empty_label = "Choisissez une catégorie"
        # Une catégorie désactivée n'est plus proposée, sauf si l'objet l'utilise déjà.
        self.fields["category"].queryset = Category.objects.filter(
            Q(is_active=True) | Q(pk=self.instance.category_id)
        )


class CatalogFilterForm(forms.Form):
    q = forms.CharField(label="Rechercher", required=False, widget=forms.SearchInput(
        attrs={"placeholder": "Perceuse, tente, appareil à raclette…"}
    ))
    category = forms.ModelChoiceField(
        label="Catégorie", queryset=Category.objects.filter(is_active=True), required=False,
        empty_label="Toutes les catégories",
    )
    neighborhood = forms.ModelChoiceField(
        label="Quartier", queryset=Neighborhood.objects.filter(is_active=True), required=False,
        empty_label="Tous les quartiers",
    )
