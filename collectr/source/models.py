# python
from urlparse import urlparse
from datetime import datetime

# django
from django.db import models
from django.contrib.auth.models import User

# app

FILTERFIELDCHOICES = (
    ('tags', 'tags'),
    ('link', 'link'),
    ('summary', 'summary'),
    ('title', 'title'),
    ('content', 'content'),
    ('origin', 'origin'),
    ('source', 'source'),
    ('author', 'author'),
)

class Collection(models.Model):
    user = models.ForeignKey(User, null=True, blank=True)
    name = models.CharField(max_length=128)

    def __unicode__(self):
        return "%s (%d)" % (self.name, self.user_id or 0)

class Filter(models.Model):
    user = models.ForeignKey(User, null=True, blank=True)
    regexp = models.CharField(max_length=64)
    field = models.CharField(choices=FILTERFIELDCHOICES, max_length=32)
    to_delete = models.BooleanField(default=False)
    to_collection = models.ForeignKey(Collection, null=True, blank=True)
    xpath = models.TextField(null=True, blank=True)

    def __unicode__(self):
        if self.to_delete:
            return u"delete match %s (%d)" % (self.regexp, self.user_id or 0)
        return u"move match %s to %d (%d)" % (self.regexp, self.to_collection_id, self.user_id or 0)

class Source(models.Model):
    name = models.CharField(max_length=32)
    slug = models.CharField(max_length=32, unique=True)

    def __unicode__(self):
        return self.name

class Origin(models.Model):
    name = models.CharField(max_length=128)

class UrlViews(models.Model):
    count = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Url View'
        verbose_name_plural = 'Url Views'

    def __unicode__(self):
        return u"%d" % self.count

class Tag(models.Model):
    name = models.CharField(max_length=128, unique=True)

    def __unicode__(self):
        return self.name

class Url(models.Model):
    link = models.TextField(unique=True)
    views = models.ForeignKey(UrlViews)
    tags = models.ManyToManyField(Tag)
    raw_tags = models.TextField()
    content = models.TextField()
    image = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return self.link

class Author(models.Model):
    name = models.CharField(max_length=64, unique=True)
    source = models.ForeignKey(Source)

class LinkSum(models.Model):
    tags = models.TextField()
    summary = models.TextField(null=True)
    title = models.TextField()
    link = models.TextField()
    url = models.ForeignKey(Url, null=True, blank=True)
    origin = models.ForeignKey(Origin, null=True)
    source = models.ForeignKey(Source, null=True)
    read = models.BooleanField(default=False)
    recommanded = models.IntegerField(default=1)
    collection = models.ForeignKey(Collection, null=True)
    inserted_at = models.DateTimeField(default=datetime.now)
    user = models.ForeignKey(User)
    authors = models.ManyToManyField(Author, related_name="authors")
    hidden = models.BooleanField(default=False)

    class Meta:
        unique_together = ("url", "user")

    def __unicode__(self):
        return u'%s - user(%d) collection(%d)' % (self.link, self.user_id, self.collection_id)

    def reco(self):
        return """%d""" % self.recommanded
    reco.short_description = "Reco"

    def link_title(self):
        return """<a href="%s" target="_blank">%s</a>""" % (self.link, self.title)
    link_title.short_description = "Title"
    link_title.allow_tags = True

    def get_tags(self):
        if self.tags:
            return self.tags.split(',')
        return []

class Rss(models.Model):
    link = models.URLField(verify_exists=False, max_length=1024, unique=True)
    name = models.CharField(max_length=128)
    users = models.ManyToManyField(User)
    etag = models.CharField(max_length=128, null=True, blank=True)

    class Meta:
        verbose_name = u'Rss'
        verbose_name_plural = u'Rss'

    def __unicode__(self):
        return self.name

