from django.db.models import Model, CharField, ForeignKey, CASCADE, ImageField, EmailField, DecimalField, IntegerField
from django.db.models import PositiveIntegerField, BooleanField,TextField,DateField
from django.db.models import DateTimeField, FileField, URLField, SET_NULL
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import UserManager, AbstractUser
from django.db.models.enums import TextChoices
from ckeditor_uploader.fields import RichTextUploadingField


class CustomUserManager(UserManager):

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The given email must be set")

        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    class RoleType(TextChoices):
        SELLER = 'seller', "Seller"
        OPERATOR = 'operator', "Operator"
        ADMIN = 'admin', "Admin"
        DELIVER = 'deliver', "Deliver"

    username = None
    email = EmailField(unique=True, null=True)
    phone_number = CharField(max_length=20, null=True, blank=True)
    password = CharField(max_length=128, null=True, blank=True)
    district = ForeignKey('apps.District', on_delete=CASCADE, related_name='users', null=True, blank=True)
    image = ImageField(upload_to='users', null=True, blank=True)
    balance = IntegerField(default=0)
    role = CharField(max_length=30, choices=RoleType.choices, default=RoleType.SELLER)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()


class Product(Model):
    name = CharField(max_length=255)
    quantity = IntegerField(default=1)
    description = RichTextUploadingField()
    video = FileField(upload_to='product', null=True, blank=True)
    discount = PositiveIntegerField(default=0)
    price = DecimalField(max_digits=10, decimal_places=2)
    main_image = ImageField(upload_to='product/')
    creat_at = DateTimeField(auto_now_add=True)
    seller_price = DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    category = ForeignKey('apps.Category', on_delete=CASCADE, related_name='products')
    attribute = ForeignKey('apps.Attribute', on_delete=CASCADE, related_name='products', null=True, blank=True)
    seller = ForeignKey('apps.Seller', on_delete=CASCADE, related_name='products')
    order_count = PositiveIntegerField(default=0)
    visit_count = PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    @property
    def discount_price(self):
        price = int(self.price)
        return price - price * (self.discount / 100)

    @property
    def sell_percentage(self):
        if self.visit_count == 0:
            return 0
        percent = int(round((self.order_count / self.visit_count) * 100))
        if percent == 0 and self.order_count > 0:
            return 1  # eng kamida 1%
        return percent


class ProductTag(Model):
    tag = ForeignKey('apps.Product', on_delete=CASCADE, related_name='tags')
    product = ForeignKey('apps.Tag', on_delete=CASCADE, related_name='products')


class Tag(Model):
    name = CharField(max_length=255)

    def __str__(self):
        return self.name


class Order(Model):
    class StatusType(TextChoices):
        NEW = 'new', 'New',
        REDY_TO_DELIVER = 'ready to deliver', 'Ready to deliver',
        DELIVERING = 'delivering', 'Delivering',
        DELIVERED = 'delivered', 'Delivered',
        COMPLETED = 'completed', 'Completed',
        COME_BACK = 'come back', 'Come back',
        ARCHIVE = 'archive', 'Archive',
        HOLD = 'hold', 'Hold'

    name = CharField(max_length=100)
    phone_number = CharField(max_length=20)
    total = DecimalField(max_digits=10, decimal_places=2)
    quantity = PositiveIntegerField(default=1)
    status = CharField(max_length=100, choices=StatusType.choices, default=StatusType.NEW)
    comment = TextField(null=True, blank=True)
    delivery_time = DateField(null=True, blank=True)
    stream = ForeignKey('apps.Stream', on_delete=SET_NULL, related_name='orders', null=True, blank=True)
    product = ForeignKey(Product, on_delete=SET_NULL, related_name='orders', null=True, blank=True)
    region = ForeignKey('apps.Region', on_delete=SET_NULL, related_name='orders', null=True, blank=True)
    owner = ForeignKey(User, on_delete=SET_NULL, related_name='orders', null=True, blank=True)
    district = ForeignKey('apps.District', on_delete=SET_NULL, related_name='orders', null=True, blank=True)
    updated_at = DateTimeField(auto_now=True)
    created_at = DateTimeField(auto_now_add=True)

class Charity(Model):
    class Meta:
        verbose_name_plural = "Charities"
        default_related_name = 'charities'

    amount = PositiveIntegerField()
    stream_id = ForeignKey('apps.Stream', on_delete=SET_NULL, null=True, blank=True)
    created_at = DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.amount)


class Payment(Model):
    class StatusType(TextChoices):
        CANCELED = 'canceled', 'Canceled'
        UNDER_VIEW = 'under view', 'Under View'
        COMPLETED = 'completed', 'Completed'

    card_number = CharField(max_length=16)
    user = ForeignKey(User, on_delete=CASCADE, related_name='payments')
    amount = PositiveIntegerField()
    message = RichTextUploadingField(null=True, blank=True)
    status = CharField(max_length=50, choices=StatusType, default=StatusType.UNDER_VIEW)
    updated_at = DateTimeField(auto_now=True)
    created_at = DateTimeField(auto_now_add=True)


class Category(Model):
    class Meta:
        verbose_name_plural = "Categories"

    image = ImageField(upload_to='categories', null=True, blank=True)
    name = CharField(max_length=100)

    def __str__(self):
        return self.name


class Seller(Model):
    name = CharField(max_length=100)
    username_tg = CharField(max_length=100)
    region = ForeignKey('apps.Region', on_delete=CASCADE, related_name='sellers')

    def __str__(self):
        return self.name


class Penalty(Model):
    class Meta:
        verbose_name_plural = "Penalties"

    description = RichTextUploadingField()
    type = CharField(max_length=255)
    response = CharField(max_length=255)
    stream = ForeignKey('apps.Stream', on_delete=CASCADE, related_name='penalties')
    amount = DecimalField(max_digits=10, decimal_places=2)


class ProductImage(Model):
    image = ImageField(upload_to='images/')
    product = ForeignKey('apps.Product', on_delete=CASCADE, related_name='images')


class Attribute(Model):
    name = CharField(max_length=120)

    def __str__(self):
        return self.name


class Option(Model):
    attribute_id = ForeignKey('apps.Attribute', on_delete=CASCADE, related_name='options')
    name = CharField(max_length=120)

    def __str__(self):
        return self.name


class Region(Model):
    name = CharField(max_length=255)
    order_count=PositiveIntegerField(default=0)

    def __str__(self):
        return self.name


class District(Model):
    name = CharField(max_length=255)
    region = ForeignKey('apps.Region', CASCADE, related_name='districts')

    def __str__(self):
        return self.name


class Stream(Model):
    product = ForeignKey('apps.Product', on_delete=CASCADE, related_name='streams')
    user = ForeignKey(User, on_delete=CASCADE, related_name='streams')
    name = CharField(max_length=255)
    operator = BooleanField(default=False)
    is_region=BooleanField(default=False)
    visit_count = PositiveIntegerField(default=0)
    created_at = DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Settings(Model):
    phone_number = CharField(max_length=20)
    tg_ling = URLField(max_length=255)
    tg_bot = CharField(max_length=255)
    ling_bot = URLField(max_length=255, null=True, blank=True)
    delivery_price = DecimalField(max_digits=10, decimal_places=2, default=0)
    description = RichTextUploadingField(null=True, blank=True)


class News(Model):
    class Meta:
        verbose_name_plural = "News"

    title = CharField(max_length=255)
    description = RichTextUploadingField()
    image = URLField(null=True, blank=True)
    created_at = DateTimeField(auto_now_add=True)


class Transaction(Model):
    type=CharField(max_length=5)
    user=ForeignKey(User,on_delete=CASCADE,related_name='transactions')
    amount=DecimalField(max_digits=10, decimal_places=2)
    message=CharField(max_length=255)
    created_at=DateTimeField(auto_now_add=True)
