#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Nathan Shafer'
SITENAME = u'Lotechnica'
# SITESUBTITLE = u"By Nathan Shafer"
SITESUBTITLE = u"Technical writings by Nathan Shafer"
SITEURL = ''
# ABOUT_ME = "Hacker making stuff"

PATH = 'content'
# ARTICLE_PATHS = ['articles']
STATIC_PATHS = ['images', 'static']
STATIC_EXCLUDES = ['.sass-cache']
AUTHOR_SAVE_AS = ''

USE_FOLDER_AS_CATEGORY = True

TIMEZONE = 'America/Phoenix'

DEFAULT_LANG = u'en'

# Theme settings
THEME = "theme"
PYGMENTS_STYLE = "native"
DISPLAY_PAGES_ON_MENU = False
DISPLAY_CATEGORIES_ON_MENU = True

# pelican-bootstrap3 theme settings
BOOTSTRAP_THEME = "flatly"
CUSTOM_CSS = "static/custom.css"
GITHUB_USER = "nshafer"
GITHUB_REPO_COUNT = 5
GITHUB_SKIP_FORK = True
# GITHUB_SHOW_USER_LINK = True
SHARIFF = True
SHARIFF_LANG = "en"
SHOW_ARTICLE_AUTHOR = False
SHOW_ARTICLE_CATEGORY = True
SHOW_DATE_MODIFIED = True
DISPLAY_TAGS_ON_SIDEBAR = True
DISPLAY_TAGS_INLINE = True
DISPLAY_RECENT_POSTS_ON_SIDEBAR = True
CC_LICENSE = "CC-BY"

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

# ASSET_CONFIG = (
# 	('cleancss_bin', "theme/node_modules/clean-css/bin/cleancss"),
# 	# ('sass_style', "compressed"),
# 	('sass_debug_info', True),
# )
# # ASSET_DEBUG = True

# MathJax
MATH_JAX = {
    'responsive': True
}

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True
