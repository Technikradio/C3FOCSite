# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-10-05 15:06

from django.contrib.auth.models import User
from frontpage.models import Profile, Settings


def init_db(suppress_warnings=False):
    # add a default user 'admin' using password 'password' and set default values for the header and footer settings
    # Profile = apps.get_model('frontpage', 'Profile')
    # Settings = apps.get_model('frontpage', 'Settings')
    # User = apps.get_model('auth', 'User')
    u = User.objects.create_superuser('admin', 'mail@example.com', 'password')
    u.save()
    u = User.objects.all()[0]
    p = Profile()
    p.authuser = u
    p.active = True
    p.dect = 0
    p.displayName = "Admin"
    p.rights = 4
    p.notes = 'Please change the default login credentials and mail address.'
    p.save()
    p = Profile.objects.all()[0]
    bs = Settings()
    bs.changedByUser = p
    bs.property = '''[{
            "type":"link",
            "href":"example.com","text":"Visit example.com"
        },{"type":"link","text":"Visit the top level website",
        "href":".."}]'''
    bs.SName = 'frontpage.ui.navbar.content'
    bs.requiredLevel = 0
    bs.changeReason = "initial setup"
    fs = Settings()
    fs.changedByUser = p
    fs.property = '''[{
                "type":"link",
                "href":"example.com","text":"Visit example.com"
            },{"type":"link","text":"Visit the top level website",
            "href":".."}]'''
    fs.SName = 'frontpage.ui.footer.content'
    fs.requiredLevel = 0
    fs.changeReason = "initial setup"
    bs.save()
    fs.save()
    ms = Settings()
    ms.SName = "frontpage.store.open"
    ms.property = "true"
    ms.requiredLevel = 0
    ms.changeReason = "Initial setup"
    ms.changedByUser = p
    ms.save()
    cs = Settings()
    cs.SName = "frontpage.chestsize"
    cs.property = "50"
    cs.requiredLevel = 1
    cs.changeReason = "Initial setup"
    cs.changedByUser = p
    cs.save()
    if not suppress_warnings:
        print('created default user \'admin\' with password \'password\' and an random mail address.')
        print('Make sure to change both the password and the mail address.')
    pass

# init_db()
