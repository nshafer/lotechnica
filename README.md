Lotechnica
==========

This is my blog.  You can see it live [here](http://blog.lotech.org).

Feel free to use any of this for your own, but please give me credit where due.  All files are licensed under the
[Creative Commons Attribution 4.0 International License](http://creativecommons.org/licenses/by/4.0/)

## Jumbo images

Jumbo images must conform to this spec:

Article metadata:
    Jumbo_image: images/article-slug/image.jpg
    Jumbo_color: [dark|light]
    Jumbo_attr: Text goes here
    Jumbo_attr_link: http://full.url/and/path
    Small_image: images/article-slug/image.jpg

Jumbo_image should be 1920x1080

Small_image should be 768x432

## Dev

Run pelican and dev server on port 7000

```bash
make devserver
```

[Open in browser](http://localhost:7000/)

## Publish

```bash
make clean
make publish
make rsync_upload
```
