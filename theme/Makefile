SASS=/usr/bin/env sass
STYLESHEET=static/styles/theme.scss
OUTPUT=static/styles/theme.css

default:
	$(SASS) --style compressed $(STYLESHEET) $(OUTPUT)

watch:
	$(SASS) --watch $(STYLESHEET) $(OUTPUT)

static/style/theme.scss: default
