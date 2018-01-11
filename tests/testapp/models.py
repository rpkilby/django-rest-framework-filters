from django.contrib.auth.models import User
from django.db import models, connections


class ExplainQuerySet(models.QuerySet):

    def explain(self):
        cursor = connections[self.db].cursor()
        query, params = self.query.sql_with_params()
        cursor.execute('explain query plan %s' % query, params)
        return '\n'.join('|'.join([str(e) for e in line]) for line in cursor.fetchall())


class Note(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)


class Post(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    content = models.TextField()
    date_published = models.DateField(null=True)


class Cover(models.Model):
    comment = models.CharField(max_length=100)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


class Page(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    previous_page = models.ForeignKey('self', null=True, on_delete=models.CASCADE)


class A(models.Model):
    title = models.CharField(max_length=100)
    b = models.ForeignKey('B', null=True, on_delete=models.CASCADE)


class C(models.Model):
    title = models.CharField(max_length=100)
    a = models.ForeignKey(A, null=True, on_delete=models.CASCADE)


class B(models.Model):
    name = models.CharField(max_length=100)
    c = models.ForeignKey(C, null=True, on_delete=models.CASCADE)


class Person(models.Model):
    name = models.CharField(max_length=100)
    best_friend = models.ForeignKey('self', null=True, on_delete=models.CASCADE)

    date_joined = models.DateField(auto_now_add=True)
    time_joined = models.TimeField(auto_now_add=True)
    datetime_joined = models.DateTimeField(auto_now_add=True)


class Tag(models.Model):
    name = models.CharField(max_length=100)


class BlogPost(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    tags = models.ManyToManyField(Tag)
    publish_date = models.DateField(null=True)


class Blog(models.Model):
    name = models.CharField(max_length=100)

    objects = ExplainQuerySet.as_manager()


class Entry(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    headline = models.CharField(max_length=240)
    pub_date = models.DateField(null=True)

    objects = ExplainQuerySet.as_manager()
