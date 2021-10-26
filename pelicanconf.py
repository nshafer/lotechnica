AUTHOR = 'Nathan Shafer'
SITENAME = 'Lotechnica'
SITESUBTITLE = "Technical writings by Nathan Shafer"
SITEURL = 'https://blog.lotech.org'

PATH = 'content'
STATIC_PATHS = ['images', 'static']
STATIC_EXCLUDES = ['.sass-cache']
AUTHOR_SAVE_AS = ''

USE_FOLDER_AS_CATEGORY = True

# Locale settings
TIMEZONE = 'America/Phoenix'
DEFAULT_LANG = 'en'
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
    ('Normal Technologies LLC', 'https://www.normal.tech/'),
    ('Type-in Games', 'https://www.typeingames.com/'),
    ('AnswerCast', 'https://www.typeingames.com/answercast/'),
)

# Social widget
SOCIAL = (
    ('GitHub', 'https://www.github.com/nshafer'),
)

DEFAULT_PAGINATION = 40

DEFAULT_METADATA = {
    'status': "draft",
}

# Plugins
# PLUGIN_PATHS = ['pelican-plugins']
# PLUGINS = ["render_math"]
# MARKDOWN = {
#     'extension_configs': {
#         'markdown.extensions.codehilite': {'css_class': 'highlight'},
#         'markdown.extensions.extra': {},
#         'markdown.extensions.meta': {},
#     },
#     'output_format': 'html5',
# }
#
# # MathJax
# MATH_JAX = {
#     'responsive': True
# }

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True
