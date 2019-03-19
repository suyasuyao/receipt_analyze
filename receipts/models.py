# Create your models here.
from django.core.validators import FileExtensionValidator
from django.db import models
from django.urls import reverse


class Receipt(models.Model):
    # レシートタイトル
    title = models.CharField(max_length=255)
    # 保存されたレシート内容
    text = models.TextField()

    # 保存された合計額
    sum_total = models.IntegerField(default=0)

    # 画像保存
    image = models.ImageField(upload_to='images/', blank=True)
    # attach = models.FileField(
    #     upload_to='uploads/%Y/%m/%d/',
    #     verbose_name='添付ファイル',
    #     validators=[FileExtensionValidator(['pdf', ])],
    # )

    # ユーザー
    author = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        # https://docs.djangoproject.com/en/2.0/ref/class-based-views/generic-editing/
        # return reverse('receipts:detail', kwargs={'pk': self.pk})
        return reverse('receipts:index')
