from django.contrib import admin
from django.contrib.auth.models import Group
from apps.models import *

admin.site.site_header = 'Django Market Administration'
admin.site.site_title = 'Django Market Administration'
admin.site.index_title = 'Django Market Administration'
admin.site.unregister(Group)


class ProductImageInline(admin.StackedInline):
    model = ProductImage
    extra = 1


class OptionInline(admin.StackedInline):
    model = Option
    extra = 1


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'phone_number', 'balance', 'is_active')
    search_fields = ('email', 'phone_number')
    list_filter = ('is_active',)
    ordering = ('-id',)
    readonly_fields = ('last_login', 'date_joined')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'quantity', 'price', 'seller', 'creat_at', 'seller_price', 'discount')
    list_filter = ('category', 'creat_at')
    search_fields = ('name',)
    ordering = ('-creat_at',)
    inlines = [ProductImageInline]
    readonly_fields = ('creat_at',)


@admin.register(ProductTag)
class ProductTagAdmin(admin.ModelAdmin):
    list_display = ('id', 'tag', 'product')
    search_fields = ('tag__name', 'product__name')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone_number', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('name', 'phone_number')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'amount', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__email', 'user__phone_number')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)

    def save_model(self, request, obj, form, change):
        data = form.cleaned_data
        if change and data.get('status') == Payment.StatusType.CANCELED.value:
            user = data.get('user')
            user.balance += data.get('amount')
            user.save()
        super().save_model(request, obj, form, change)


@admin.register(Charity)
class CharityAdmin(admin.ModelAdmin):
    list_display = ('id', 'amount', 'stream_id')
    ordering = ('-id',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'username_tg', 'region')
    list_filter = ('region',)
    search_fields = ('name', 'username_tg')


@admin.register(Penalty)
class PenaltyAdmin(admin.ModelAdmin):
    list_display = ('id', 'description', 'type', 'amount')
    list_filter = ('type',)
    search_fields = ('description',)


@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    inlines = [OptionInline]
    search_fields = ('name',)


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'region')
    list_filter = ('region',)
    search_fields = ('name',)


@admin.register(Stream)
class StreamAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'user', 'operator', 'created_at')
    list_filter = ('created_at',)
    ordering = ('-created_at',)
    search_fields = ('name', 'user__email')
    readonly_fields = ('created_at',)


@admin.register(Settings)
class SettingAdmin(admin.ModelAdmin):
    list_display = ('id', 'phone_number', 'tg_ling', 'tg_bot', 'delivery_price')


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_at')
    search_fields = ('title',)
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)
