import re

from django.contrib.auth.hashers import make_password, check_password
from django.core.exceptions import ValidationError
from django.forms import CharField, Form, IntegerField
from django.forms.models import ModelForm

from apps.models import User, Payment, Order


class RegisterForm(Form):
    email = CharField(max_length=100, required=True)
    code = CharField(max_length=15, required=True)


class EmailForm(Form):
    email = CharField(max_length=255)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        user_obj = User.objects.filter(email=email)
        if user_obj.exists():
            raise ValidationError(message='Email already exists')
        return email


class LoginForm(Form):
    email = CharField(max_length=100)
    password = CharField(max_length=100)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        query = User.objects.filter(email=email)
        if not query.exists():
            raise ValidationError(message='This email does not exist', code='user_not_exist')
        user = query.first()
        if not check_password(password, user.password):
            raise ValidationError(message='Password error', code='password_error')
        self.user = user
        return super().clean()


class UserModelForm(ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'image', 'district')


class PasswordForm(ModelForm):
    confirm_password = CharField(max_length=20, min_length=8)

    class Meta:
        model = User
        fields = ('password',)

    def clean(self):
        cleaned_data = super().clean()
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise ValidationError('Passwords do not match')
        cleaned_data['password'] = make_password(password)
        return cleaned_data


class PhoneNumberForm(ModelForm):
    class Meta:
        model = User
        fields = ('phone_number',)

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        clean_number = re.sub(r'\D', '', phone_number)
        return clean_number


class PaymentModelForm(ModelForm):
    class Meta:
        model = Payment
        fields = ('amount', 'card_number', 'user')

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        user_id = self.data.get('user')
        user = User.objects.get(id=user_id)
        if amount > user.balance:
            raise ValidationError('Not enough money')
        return amount

    def clean_card_number(self):
        card_number = self.cleaned_data.get('card_number')
        if not card_number.isdigit():
            raise ValidationError('Card number error')
        return card_number


class OrderForm(Form):
    name = CharField(max_length=125, required=True)
    product_id = CharField(max_length=125, required=True)
    phone_number = CharField(max_length=125, required=True)
    region = IntegerField(required=False)
    owner = IntegerField(required=False)
    thread = IntegerField(required=False)

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        clean_number = re.sub(r'\D', '', phone_number)
        return clean_number


class OrderModelForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['quantity'].required = False

    class Meta:
        model = Order
        fields = ('district', 'region', 'delivery_time', 'quantity', 'comment', 'status')
