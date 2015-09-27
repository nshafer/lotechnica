Title: Colophon
Date: 2015-09-26
Modified: 2015-09-26
Status: published

This site began life at [Blogger](http://www.blogger.com), but I found that platform to be more of a hindrance than a help in publishing articles.
And any stumbling block raises the barrier-of-laziness, and thus I don't write articles.

In September of 2015 I finally got around to migrating it to a static site, using [Pelican](http://www.getpelican.com).
I like this platform for a few reasons:

1. I can write in **markdown** format.  Everything is done in markdown these days, and it's quick and easy to use.  Blogger forced me to write in HTML, which is great for web pages, not so great for publishing.
2. There are no moving parts to be hacked.  It's just a bunch of static files.
3. Local dev server to preview articles in the site locally.  No internet connection required.  That, and Blogger's preview function *always* took a minimum of 30 seconds to render for me.
4. I can host it anywhere, even free places like GitHub.
5. Integrated MathJax!  I can just inline formulas with `$`.
6. Fast!  No server-side processing required.  Just serve up the files.

So with the migration I decided to build the entire site up from scratch as a way to try out some new tech.  So this will hopefully get me writing more.

## Components

I started with Pelican's `simple` theme for the templates, and customized it to meet my needs.
A few elements of the [pelican-bootstrap3](https://github.com/DandyDev/pelican-bootstrap3) theme for Pelican were borrowed.

I wrote all of the stylesheets in [SCSS](http://sass-lang.com/), using
[Bourbon](http://bourbon.io/), [Bourbon Neat](http://neat.bourbon.io/) for responsiveness, and [Bitters](http://bitters.bourbon.io/) for a reset.
The end result is one CSS file for the entire site that's a fraction of the size of bootstrap.min.css.

All fonts are from [Google Fonts](https://www.google.com/fonts).  Icons are from [Font Awesome](http://fontawesome.io/).

No javascript or third party stylesheets included.

The result is that every page is about 100kb in size for all HTML, CSS and images plus whatever is in each article.

## Tools

My IDE of choice is the ridiculously awesome [PyCharm](https://www.jetbrains.com/pycharm/) from JetBrains.  It even has a Markdown preview built-in.
For all graphical work I prefer to use [GIMP](http://www.gimp.org/), [Inkscape](https://inkscape.org) and [Blender](http://www.blender.org/).
All on [Linux Mint](http://www.linuxmint.com/) of course.

## Source

If you're interested, the source for this blog is available on [github](https://github.com/nshafer/lotechnica).