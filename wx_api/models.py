from django.db import models
from django.db.models.signals import post_delete
from django.dispatch.dispatcher import receiver
import os
from yun_server import settings
from .storage import FileStorage


class AuthCar(models.Model):
    uid = models.AutoField(primary_key=True)
    # 保存用户uid
    car_id = models.CharField(max_length=10, db_index=True)
    # 索引，车牌号
    app_id = models.CharField(max_length=20)
    # 外键连接auth_token,应用id
    created = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        db_table = 'auth_car'


class AuthApp(models.Model):
    app_id = models.CharField(primary_key=True, max_length=20)
    # 应用id
    app_secret = models.CharField(max_length=32)
    # 应用密码(本处出于简单处理，直接明文保存)

    class Meta:
        db_table = 'auth_app'


class CarComputedDate(models.Model):
    uid = models.ForeignKey(AuthCar, on_delete=models.CASCADE)
    # 外键连接auth_car，上传用户uid
    gid = models.IntegerField(db_index=True)
    # 索引，上传的分组
    data_record = models.IntegerField(null=True)
    # 用户上传的实际运动值
    data_computed = models.IntegerField(null=True)
    # 运算的理想运动值
    created = models.DateTimeField(auto_now=True)
    # 上传保存的时间

    class Meta:
        db_table = 'car_computed_data'


class CarData(models.Model):
    uid = models.ForeignKey(AuthCar, on_delete=models.CASCADE)
    # 外键连接auth_car，上传用户uid
    gid = models.IntegerField(db_index=True)
    # 索引，上传的分组
    g_sid = models.IntegerField(db_index=True)
    # 索引，在某分组下的具体序号
    ccd = models.IntegerField(null=True)
    # CCD 数组
    electric = models.IntegerField(null=True)
    # 电感感应值
    acceleration = models.IntegerField(null=True)
    # 加速度值
    speed = models.IntegerField(null=True)
    # 速度编码值
    created = models.DateTimeField(auto_now=True)
    # 上传保存的时间

    class Meta:
        db_table = 'car_data'


class CarImage(models.Model):
    uid = models.ForeignKey(AuthCar, on_delete=models.CASCADE)
    # 外键连接auth_car，上传用户uid
    gid = models.IntegerField(db_index=True)
    # 索引，上传的分组
    g_sid = models.IntegerField(db_index=True)
    # 索引，在某分组下的具体序号
    url = models.ImageField(max_length=50, upload_to="./images_upload/")
    # 图片的url路径，命名方式为/images_upload/{uid}_{gid}_{g_sid}_{created}
    created = models.DateTimeField(auto_now=True)
    # 图片上传保存时间

    class Meta:
        db_table = 'car_image'


@receiver(post_delete, sender=CarImage)
def delete_upload_files(sender, instance, **kwargs):
    files = getattr(instance, 'url', '')
    if not files:
        return
    fname = os.path.join(settings.BASE_DIR, str(files))
    if os.path.isfile(fname):
        os.remove(fname)


class AuthToken(models.Model):
    key = models.CharField(max_length=200, primary_key=True)
    uid = models.OneToOneField(AuthCar, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'auth_token'

    def __str__(self):
        return self.key


class CarFile(models.Model):
    uid = models.ForeignKey(AuthCar, on_delete=models.CASCADE)
    # 外键连接auth_car，上传用户uid
    gid = models.IntegerField(db_index=True)
    # 索引，上传的分组
    g_sid = models.IntegerField(db_index=True)
    # 索引，在某分组下的具体序号
    url = models.FileField(upload_to="./files_upload/", storage=FileStorage())
    # 文件的url路径，命名方式为/files{uid}_{gid}_{g_sid}_{created}
    created = models.DateTimeField(auto_now=True)
    # 文件上传保存时间

    class Meta:
        db_table = 'car_file'
