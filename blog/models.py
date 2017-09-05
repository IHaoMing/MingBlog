#coding:utf-8
import markdown
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.six import python_2_unicode_compatible
from django.utils.html import strip_tags


# Create your models here.
#分类模型
@python_2_unicode_compatible
class Category(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    
#标签模型
@python_2_unicode_compatible
class Tag(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

#文章模型
@python_2_unicode_compatible
class Post(models.Model):
    #文章标题
    title = models.CharField(max_length=70)
    #文章正文
    body = models.TextField()
    #文章创建时间
    created_time = models.DateTimeField()
    #文章修改时间
    modified_time = models.DateTimeField()
    #文章摘要,允许空值
    excerpt = models.CharField(max_length=200, blank=True)
    #文章分类，使用外键与Category模型联系
    category = models.ForeignKey(Category)
    #文章标签,文章与标签是多对多关系，且允许为空
    tags = models.ManyToManyField(Tag, blank=True)
    # 新增 views 字段记录阅读量
    views = models.PositiveIntegerField(default=0)
    #文章作者，使用外键与User模型（自有）联系起来,注意在文件头部导入User模型
    author = models.ForeignKey(User)
    def __str__(self):
        return self.title
    #自定义get_absolute_url方法
    #注意头部导入reverse函数
    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})
    #阅读数量字段的方法
    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])
    #文章摘要的方法
    def save(self, *args, **kwargs):    
        # 如果没有填写摘要
        if not self.excerpt:
            # 首先实例化一个 Markdown 类，用于渲染 body 的文本
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
            ])
            # 先将 Markdown 文本渲染成 HTML 文本
            # strip_tags 去掉 HTML 文本的全部 HTML 标签
            # 从文本摘取前 54 个字符赋给 excerpt
            self.excerpt = strip_tags(md.convert(self.body))[:54]

        # 调用父类的 save 方法将数据保存到数据库中
        super(Post, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-created_time']

    
