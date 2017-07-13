#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Nathan Shafer'
SITENAME = u'Lotechnica'
SITESUBTITLE = u"Technical writings by Nathan Shafer"
SITEURL = 'http://blog.lotech.org'

PATH = 'content'
STATIC_PATHS = ['images', 'static']
STATIC_EXCLUDES = ['.sass-cache']
AUTHOR_SAVE_AS = ''

USE_FOLDER_AS_CATEGORY = True

# Locale settings
TIMEZONE = 'America/Phoenix'
DEFAULT_LANG = u'en'
DEFAULT_DATE_FORMAT = '%B %-d, %Y'

# Theme settings
THEME = "theme"
PYGMENTS_STYLE = "native"
DISPLAY_PAGES_ON_MENU = False
DISPLAY_CATEGORIES_ON_MENU = True
USE_OPEN_GRAPH = True

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (
    ('Normal Technologies LLC', 'http://www.normal-tech.com/'),
    ('Type-in Games', 'http://www.typeingames.com/'),
    ('AnswerCast', 'http://www.typeingames.com/answercast/'),
)

# Social widget
SOCIAL = (
    ('GitHub', 'https://www.github.com/nshafer'),
    ('Google Plus', 'https://www.google.com/+NathanShafer'),
)

DEFAULT_PAGINATION = 40

DEFAULT_METADATA = {
    'status': "draft",
}

# Plugins
PLUGIN_PATHS = ['pelican-plugins']
PLUGINS = ["render_math"]
MD_EXTENSIONS = ['codehilite(css_class=highlight)', 'extra', 'markdown-figures.captions']

# MathJax
MATH_JAX = {
    'responsive': True
}

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True
