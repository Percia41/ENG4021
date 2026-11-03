from decimal import Decimal

from django import forms

from .models import Defeito, Product


def discount_preview(original_price, tipo, localizacao, extensao):
    """Use o próprio model: não mantenha uma segunda fórmula no formulário.

    Monta um Product e um Defeito não salvos, ligados em memória: isso não
    toca o banco e o cálculo fica inteiramente a cargo das properties do model.
    """
    product = Product(original_price=original_price)
    product.defeito = Defeito(tipo=tipo, localizacao=localizacao, extensao=extensao)
    return {
        'severity': product.severity,
        'severity_label': product.severity_label,
        'discount': product.suggested_discount,
        'original_price': product.original_price,
        'final_price': product.suggested_price,
    }


class DefectFieldsMixin(forms.Form):
    """Os três critérios do defeito, usados pelo simulador e pelo cadastro de peça."""
    defect_type = Defeito._meta.get_field('tipo').formfield()
    defect_location = Defeito._meta.get_field('localizacao').formfield()
    defect_extent = Defeito._meta.get_field('extensao').formfield()


class DiscountSimulationForm(DefectFieldsMixin):
    original_price = Product._meta.get_field('original_price').formfield(required=True, min_value=Decimal('0.01'))
    field_order = ['original_price', 'defect_type', 'defect_location', 'defect_extent']

    def preview(self):
        data = self.cleaned_data
        return discount_preview(data['original_price'], data['defect_type'], data['defect_location'], data['defect_extent'])


class ProductForm(DefectFieldsMixin, forms.ModelForm):
    """Cadastro e edição de peça pelo vendedor.

    O preço final e o vendedor são definidos no servidor, nunca pelo POST:
    o preço vem da severidade do defeito e o vendedor vem da view.
    """
    field_order = [
        'name', 'brand', 'category', 'size', 'condition', 'measurements',
        'description', 'original_price', 'defect_type', 'defect_location',
        'defect_extent', 'defect_measure_cm', 'visible_when_worn', 'stock', 'is_active',
    ]

    class Meta:
        model = Product
        fields = [
            'name', 'brand', 'category', 'size', 'condition', 'measurements',
            'description', 'original_price', 'defect_measure_cm', 'visible_when_worn',
            'stock', 'is_active',
        ]
        labels = {'name': 'Nome da peça', 'description': 'Descrição da peça e do defeito',
                  'is_active': 'Exibir na vitrine'}
        help_texts = {'original_price': 'O preço final será calculado pela regra de severidade do model.'}
        widgets = {'description': forms.Textarea(attrs={'rows': 4}),
                   'measurements': forms.Textarea(attrs={'rows': 2})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['original_price'].required = True
        self.fields['original_price'].widget.attrs['min'] = '0.01'
        self.fields['defect_measure_cm'].widget.attrs['min'] = '0'
        self.fields['stock'].min_value = 1
        self.fields['stock'].widget.attrs['min'] = '1'
        defeito = getattr(self.instance, 'defeito', None)
        if defeito is not None:
            self.initial.update(defect_type=defeito.tipo, defect_location=defeito.localizacao,
                                defect_extent=defeito.extensao)

    def clean_stock(self):
        stock = self.cleaned_data['stock']
        if stock < 1:
            raise forms.ValidationError('Informe pelo menos uma peça em estoque.')
        return stock

    def clean(self):
        cleaned = super().clean()
        fields = ['original_price', 'defect_type', 'defect_location', 'defect_extent']
        if all(cleaned.get(name) is not None for name in fields):
            # Liga o defeito à peça em memória antes das validações do model,
            # para que o preço sugerido já possa ser calculado.
            defeito = getattr(self.instance, 'defeito', None) or Defeito()
            defeito.tipo = cleaned['defect_type']
            defeito.localizacao = cleaned['defect_location']
            defeito.extensao = cleaned['defect_extent']
            self.instance.defeito = defeito
            # O ModelForm só copia os campos para o model depois do clean().
            self.instance.original_price = cleaned['original_price']
            self.instance.price = self.instance.suggested_price
        return cleaned

    def save(self, commit=True):
        product = super().save(commit=commit)
        if commit:
            product.defeito.product = product
            product.defeito.save()
        return product
