Title: formatting
Date: 2015-09-26
Status: draft
Tags: testing

**[Table of Contents](https://python-markdown.github.io/extensions/toc/){:target="_blank"}.**

[TOC]

All of this is [Markdown](https://daringfireball.net/projects/markdown/syntax){:target="_blank"}.

Typography (also a different h1 header)
=======================================

Paragraphs are separated by a blank line.

2nd paragraph. *Italic*, **bold**, and `monospace`. Itemized lists
look like:

* this one
* that one
* the other one

> Block quotes are
> written like so.
>
> They can span multiple paragraphs,
> if you like.


Here's a numbered list:

1. first item
2. second item
3. third item

Code blocks (also another type of h2 header)
--------------------------------------------

Note again how the actual text starts at 4 columns in (4 characters
from the left side). Here's a code sample:

    # Let me re-iterate ...
    for i in 1 .. 10 { do-something(i) }

As you probably guessed, indented 4 spaces. By the way, instead of
indenting the block, you can use delimited blocks, if you like:

```
define foobar() {
    print "Welcome to flavor country!";
}
```

(which makes copying & pasting easier). You can optionally mark the
delimited block to syntax highlight it:

```python
import time
# Quick, count to ten!
for i in range(10):
    # (but not *too* quick)
    time.sleep(0.5)
    print i
```

## Nested lists

Now a nested list:

1. First, get these ingredients:

     * carrots
     * celery
     * lentils

2. Boil some water.

3. Dump everything in the pot and follow
   this algorithm:

        find wooden spoon
        uncover pot
        stir
        cover pot
        balance wooden spoon precariously on pot handle
        wait 10 minutes
        goto first step (or shut off burner when done)

    Do not bump wooden spoon or it will fall.

4. [SuperFences](https://facelessuser.github.io/pymdown-extensions/extensions/superfences/){:target="_blank"}. allows nesting code fences.

    ```python
    def eat(food):
        food.eat()
    ```

6. And they don't interrupt the list numbers

Notice again how text always lines up on 4-space indents (including
that last line which continues item 3 above).

## Links

Here's a link to [a website](http://foo.bar/baz.html), to a [local
doc](local-doc.html), and to a [section heading in the current
doc](#an-h2-header). Here's link [that opens in a new tab](http://foo.bar/baz.html){:target="_blank"}.

You can also put [links elsewhere] by ommitting the parens and putting the square brackets elsewhere in the doc.

[links elsewhere]: #links

## Footnotes

Here's a footnote[^1]

[^1]: Footnote text goes here.

## Abbreviations are supported:

The Markdown extras extension includes [abbreviations](https://python-markdown.github.io/extensions/abbreviations/){:target="_blank"}.

The HTML specification
is maintained by the W3C.

*[HTML]: Hyper Text Markup Language
*[W3C]:  World Wide Web Consortium

# Tables

[Tables](https://python-markdown.github.io/extensions/tables/){:target="_blank"}. can look like this:

size | material    | color
---- | ----------- | ----------
9    | leather     | brown
10   | hemp canvas | natural
11   | glass       | transparent

# Misc stuff

## Horizontal rule

A horizontal rule follows.

***

## Definition lists

Here's a definition list:

apples
  : Good for making applesauce.

oranges
  : Citrus!
  : Colored orange

celery
brocolli
  : Are green!

tomatoes
  : There's no "e" in tomatoe.

## Admonitions

!!! info "Optional explicit title within double quotes"
    Any number of other indented markdown elements.

    This is the second paragraph indented the same amount.

!!! accent "This one is accented to catch the eye"
    You can use the "accent" type for this.

!!! warning "This is a warning"
    You should heed this warning

!!! danger "Super dangerous admonition!!!"
    You should heed this or perish.

    You have been warned.

!!! info "This one has no body"

# Embedded images

Images can be specified like so:

![example image]({static}/images/fixing-sublime-lua/sublime_curly_good.png "An exemplary image")

# Math formulas

Inline math equations go in like so: $\omega = d\phi / dt$. Display
math should get its own line and be put in in double-dollarsigns:

$$I = \int \rho R^{2} dV$$

And note that you can backslash-escape any punctuation characters
which you wish to be displayed literally, ex.: \`foo\`, \*bar\*, etc.

