from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os, time, random


class FileStorage(FileSystemStorage):
    def __init__(self, location=settings.MEDIA_ROOT, base_url=settings.MEDIA_URL):
        super(FileStorage, self).__init__(location, base_url)

    def _save(self, name, content):
        # 文件扩展名
        ext = os.path.splitext(name)[1]
        # 文件目录
        d = os.path.dirname(name)
        # 定义文件名，年月日时分秒随机数
        fn = time.strftime('%Y%m%d%H%M%S')
        fn = fn + '_%d' % random.randint(0, 100)
        # name为上传文件名称
        name = os.path.join(d, fn + ext)
        return super(FileStorage, self)._save(name, content)
