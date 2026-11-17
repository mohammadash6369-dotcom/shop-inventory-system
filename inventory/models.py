from django.db import models
from django.utils import timezone

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

# Create your models here.
