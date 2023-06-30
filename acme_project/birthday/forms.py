from django import forms

from django.core.mail import send_mail

from django.core.exceptions import ValidationError

from .models import Birthday, Congratulation

PLAYERS = {'Дэвид Бэкхем', 'Зинедин Зидан', 'Карлес Пуйоль', 'Ривалдо Дж.'}


class BirthdayForm(forms.ModelForm):
   

    class Meta:
        model = Birthday
        exclude = ('author',)
        widgets = {
            'birthday': forms.DateInput(attrs={'type': 'date'})
        }


    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        return first_name.split()[0]
    

    def clean(self):
        super().clean()
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']
        if f'{first_name} {last_name}' in PLAYERS:
            send_mail(
                subject='Another football player',
                message=f'{first_name} {last_name} пытался опубликовать запись!',
                from_email='birthday_form@acme.not',
                recipient_list=['admin@acme.not'],
                fail_silently=True,
            )
            raise ValidationError(
                'Мы тоже любим футболистов, но введите, пожалуйста, настоящее имя!'
            )


class CongratulationForm(forms.ModelForm):
    
    class Meta:
        model = Congratulation
        fields = ('text',)