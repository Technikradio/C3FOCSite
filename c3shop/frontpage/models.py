from django.db import models
from django.db.models import CASCADE
from django.contrib.auth.models import User

# Create your models here.


class Media(models.Model):
    # MID = models.BigIntegerField(primary_key=True, unique=True, editable=False, help_text="The ID of the image")
    category = models.CharField(max_length=25, help_text="The category of the media")
    headline = models.CharField(max_length=50, help_text="The heading of the image")
    text = models.CharField(max_length=15000, help_text="A longer text matching the image")
    cachedText = models.CharField(max_length=15000, help_text="The compiled version of the markdown >text<")
    lowResFile = models.CharField(max_length=15000, help_text="A link to a low resolution version of the image")
    highResFile = models.CharField(max_length=15000, help_text="A link to a high resolution version of the image")
    # uploadedByUser = models.ForeignKey(Profile)
    uploadTimestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.headline + ": " + str(self.uploadTimestamp)


class Profile(models.Model):
    # changes: username -> authuser; secretkey -> deleted; passphrase -> deleted
    # UID = models.BigIntegerField(primary_key=True, unique=True, editable=False, help_text="The ID of the user")
    authuser = models.OneToOneField(User, on_delete=CASCADE)
    avatarMedia = models.ForeignKey(Media, null=True)
    creationTimestamp = models.DateTimeField(auto_now=True)
    notes = models.CharField(max_length=15000, help_text='some notes on the user (for example additional contact ' +
                                                         'channels)')
    active = models.BooleanField(default=True)
    dect = models.IntegerField()
    rights = models.SmallIntegerField()  # The higher the number the more rights a user will have, see README.md
    displayName = models.CharField(max_length=75)

    def __str__(self):
        return str(self.authuser.username) + ": {active: " + str(self.active) + "}"


class Article(models.Model):
    # AID = models.BigIntegerField(primary_key=True, unique=True, editable=False, help_text="The ID of the article")
    price = models.CharField(max_length=10, help_text="The price of the article")
    largeText = models.CharField(max_length=15000, help_text="The markdown text of the article")
    type = models.SmallIntegerField(help_text="The type of article (e.g. for example a t-shirt")
    description = models.CharField(max_length=100, help_text="A short description of the article (e.g. heading)")
    visible = models.BooleanField(help_text="Should the article be visible to the public yet?")
    quantity = models.IntegerField(help_text="How many articles of this kind are left?")
    size = models.CharField(max_length=10, help_text="The size of the article")
    cachedText = models.CharField(max_length=15000, help_text="The compiled markdown long text")
    addedByUser = models.ForeignKey(Profile)
    flashImage = models.ForeignKey(Media, on_delete=None, null=True)  # The image visible in the list view

    def __str__(self):
        return self.description + ": " + str(self.visible) + "(size: " + str(self.size) + ", type: " + str(self.type)\
               + ")"


class Post(models.Model):
    # PID = models.BigIntegerField(primary_key=True, unique=True, editable=False, help_text="The ID of the post")
    title = models.CharField(max_length=100)
    createdByUser = models.ForeignKey(Profile)
    cacheText = models.CharField(max_length=15000, help_text="The compiled version of the markdown >text<")
    visibleLevel = models.SmallIntegerField(help_text="What access level does the viewer need to have a look at this")
    # putting -1 in the above means that it will be disabled.
    timestamp = models.DateTimeField(auto_now=True)
    text = models.CharField(max_length=15000, help_text="The markdown version of the article text")

    def __str__(self):
        return str(self.title)


class Settings(models.Model):
    SName = models.CharField(max_length=50, primary_key=True, unique=True, editable=False)
    property = models.CharField(max_length=15000)
    requiredLevel = models.SmallIntegerField()
    changeTimestamp = models.DateTimeField(auto_now=True)
    changeReason = models.CharField(max_length=15000, null=True)
    changedByUser = models.ForeignKey(Profile)

    def __str__(self):
        return str(self.SName) + ": " + str(self.property)


class GroupReservation(models.Model):
    # RID = models.BigIntegerField(primary_key=True, unique=True, editable=False, help_text="The ID of the reservation")
    timestamp = models.DateTimeField(auto_now=True)
    ready = models.BooleanField()
    createdByUser = models.ForeignKey(Profile)
    open = models.BooleanField()
    notes = models.CharField(max_length=15000)
    pickupDate = models.DateTimeField()


class ArticleRequested(models.Model):
    RID = models.ForeignKey(GroupReservation)
    AID = models.ForeignKey(Article)
    amount = models.SmallIntegerField()
    notes = models.CharField(max_length=15000)


# further media related to the article only visible in the detailed page
class ArticleMedia(models.Model):
    AID = models.ForeignKey(Article)
    MID = models.ForeignKey(Media)


# The reason why we split this from the media table is due to tree conflicts while creating the database
# This table is to identify which user uploaded which image
class MediaUpload(models.Model):
    MID = models.ForeignKey(Media)
    UID = models.ForeignKey(Profile)
