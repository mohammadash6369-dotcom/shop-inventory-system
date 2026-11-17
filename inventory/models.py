from django.db import models
from django.utils import timezone

# Create your Product
class Product(models.Model):
    # مشخصات پایه و مشترک بین تمام اصناف
    name = models.CharField(max_length=255, verbose_name="نام کالا")
    barcode = models.CharField(max_length=100, unique=True, blank=True, null=True, verbose_name="بارکد")
    purchase_price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="قیمت خرید")
    selling_price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="قیمت فروش")
    stock = models.IntegerField(default=0, verbose_name="موجودی فعلی")

    # فیلدهای هوشمند برای سیستم هشدار (AI / Rule-based Alerts)
    min_stock_alert = models.IntegerField(default=5, verbose_name="حداقل موجودی مجاز (آلارم اتمام)")
    last_sold_date = models.DateTimeField(default=timezone.now, verbose_name="تاریخ آخرین فروش")

    # ستون انعطاف‌پذیر برای ویژگی‌های اختصاصی هر صنف (مثل سایز، تاریخ انقضا، مدل خودرو و...)
    extra_attributes = models.JSONField(default=dict, blank=True, verbose_name="ویژگی‌های اختصاصی")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} (موجودی: {self.stock})"

# Create your Custumer
class Customer(models.Model):
    # اطلاعات مشتریان برای اطلاع‌رسانی تخفیف‌ها و اجناس جدید
    name = models.CharField(max_length=255, verbose_name="نام مشتری")
    phone_number = models.CharField(max_length=15, unique=True, verbose_name="شماره تماس")
    email = models.EmailField(blank=True, null=True, verbose_name="ایمیل")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ثبت")

    def __str__(self):
        return f"{self.name} ({self.phone_number})"

# Create your Invoice
class Invoice(models.Model):
    # فاکتور فروش
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="مشتری")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="تاریخ فاکتور")
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="مبلغ کل (تومان)")
    is_paid = models.BooleanField(default=True, verbose_name="وضعیت پرداخت")

    def __str__(self):
        return f"فاکتور شماره {self.id} - تاریخ: {self.created_at.strftime('%Y-%m-%d')}"


class InvoiceItem(models.Model):
    # اقلام داخل هر فاکتور (هر کالایی که در فاکتور فروخته می‌شود)
    invoice = models.ForeignKey(Invoice, related_name='items', on_delete=models.CASCADE, verbose_name="فاکتور")
    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name="کالا")
    quantity = models.IntegerField(default=1, verbose_name="تعداد فروخته شده")
    unit_price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="قیمت واحد در زمان فروش")

    def __str__(self):
        return f"{self.quantity} عدد از {self.product.name}"

# Create your models here.
