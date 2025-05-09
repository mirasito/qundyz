from django import forms

class PlanUploadForm(forms.Form):
    plan_file = forms.FileField(
        label='Файл чертежа',
        help_text='Загрузите PDF или изображение с планом квартиры'
    )