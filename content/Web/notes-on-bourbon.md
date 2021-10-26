Title: A few notes on Bourbon, Neat, Bitters, Refills
Date: 2015-09-29
Status: published
Jumbo_image: images/notes-on-bourbon/whiskey_neat.jpg
Small_image: images/notes-on-bourbon/whiskey_neat_small.jpg
Tags: web design, responsive

When I decided to port this blog to be statically generated, I also decided to redesign it from the ground up.  Since I had recently learned about [Bourbon Neat](http://neat.bourbon.io/), I thought this would be a perfect opportunity to try it out.  These are just a few thoughts on the process and result.

### Context

First, understand that I'm a veteran [Bootstrap](http://getbootstrap.com/) user.  It's where I learned responsive design, and it's the only solution I've ever used for responsive design.  Thus, my experience with Bourbon Neat is going to be in contrast to Bootstrap.

### &lt;awesome&gt;Semantic markup!&lt;/awesome&gt;

Semantic markup is awesome.  This is what attracted me to Bourbon Neat in the first place.  I agree with the premise that HTML should be a structured document of information, and not have any styling information in it.  This is, of course, impossible to get perfectly, but with Neat, I've come the closest I ever have.  As an example, this is the basic document layout for the main index of this blog:

```html
<header id="main-header">
    <ul id="main-menu" role="nav">
        ...
    </ul>
    <section id="masthead">
        <img src="logo.jpg" />
        <h1>Lotechnica</h1>
        <p>Technical writings by Nathan Shafer</p>
    </section>
</header>

<section id="index">
    <section id="articles">
        ...
    </section>
    <aside id="about">
        ...
    </aside>
</section>

<footer id="main-footer">
    <section id="links">
        ...
    </section>
    <section id="copyright">
        ...
    </section>
</footer>
```

The result is very clean and readable, and does not contain deep nesting of responsive `.row` and `.col-xx-xx` classes.

![3D view of site hierarchy]({static}/images/notes-on-bourbon/3d-depth2.jpg "Flat hierarchy"){.pull-right}

Performance wise, this is good because the page remains flatter, thus making it easier for the browser to render.  You can see what this looks like to the right in Firefox's 3D view.  Maintenance wise, this means the presentation logic for the different breakpoints are contained in one place, the `.scss` file.  In the future it will be much easier to tweak this layout, and most likely not require any changes to the HTML.

### Kitchen sink not included

The other way that Bourbon Neat differs from Bootstrap is in the base philosophy of packaging.

With Bootstrap, you're given everything by default... the grid, pretty buttons, tables, forms, and other neat things like responsive navigation, dropdowns, collapsible panels, wells, jumbotrons, alerts, tooltips, badges, etc, etc.  If you don't want all of these things, then you need to remove things from the source files, or use Bootstrap's online customizer.  So in other words, you **start with everything, and reduce down**.

I will often throw a page or site together just using the `boostrap.min.css` hosted on their CDN with no custom CSS.  I just use all the right classes in all the right places, and get a decent looking page as a result.  This is great for little projects or prototypes where I need to get something done sooner than later.  However, as the project grows, and the design dictates changes, I find that I fight against Bootstrap quite a bit and am constantly overriding things in my stylesheet.  The result is that the user has to download a large bootstrap stylesheet, then my stylesheet which just overrides a large portion of the bootstrap stylesheet.  This is not good for performance, both for the download sizes and for the time it takes the browser to render the CSS.

With Bourbon Neat, you're given almost nothing by default.  It is pure SCSS, and there is no pre-compiled version.  Instead you `@import` the mixins you need into your stylesheet as you need it, and the resulting CSS is added.  So you **start with nothing and build up**.  The downside here, is that you don't get anything by default.  Your page will look like vanilla user-agent styling.  If you want pretty buttons, forms, tooltips, a responsive nav menu, etc, you're going to have to roll it yourself.

The [Bourbon](http://bourbon.io/) project does have a couple aids for this, though.  The [Bitters](http://bitters.bourbon.io/) module will add a basically fancy reset and help you start your project with a bunch of typography, color, form, table, list and grid settings that you can then customize from there, but they are nowhere near as comprehensive as Bootstrap's.  For some other elements, you could also look in the [Refills](http://refills.bourbon.io/) project, as they have a bunch of components you can copy and paste into your HTML, SCSS and JS source to get some pre-built elements, such as nav, tabs, accordions, tooltips, and even some things that default Bootstrap doesn't have, such as Parallax areas and sliding panels.

### Efficient results as a side effect

So with fact that you're only adding what you actually use to your stylesheet, you will end up with a much more efficient stylesheet for your site.  And since you're using Sass to build it, it could be just one stylesheet.  For this blog I decided to put all CSS for every page into one file, and didn't break it up by page-type or anything.  This allows the browser to leverage caching better between page views.  However, even though I did that, the stylesheet still came out at only **15KB**, minified.

Compare this to **143KB** for the minified `bootstrap.min.css` and `bootstrap-theme.min.css` that I usually throw in a project.   The result is that the entire style for this whole site is only 10% of the size of just the bootstrap stylesheet.  To get close to that with Bootstrap I would have needed to customize it and go through everything to throw out what I wasn't using.  I haven't actually done that, but I'm willing to guess that the customized `bootstrap.min.css` file would still be larger than 15KB.  

### You want this when?

Without all the components and convenience classes of Bootstrap, you will be responsible for styling *everything*.  You don't get anything for "free."  For example, up in the header of this site is a menu of categories.  With bootstrap, I just need to mark the HTML up with the proper classes in the proper layout, and boom, I have a responsive menu that collapses down to a single hamburger-button that expands the menu for mobile.  With the Bourbon suite I have nothing like that.  Refills currently has a nav component, but it is not responsive.  So you're on your own to implement this feature.  (I ended up just hiding the menu for mobile because I determined that it wasn't necessary and just muddied up the layout.  All the same links are in the footer.)

The end result is that you will need to take more time designing all of the components to the site.  The Bourbon suite of projects is not meant for whipping together quick projects or prototypes.  It is also not very friendly for non-designers to work with, who just want to focus on the code generating the site and not worry so much about designing every little detail of the final result.

### Overall more efficient for larger or more custom projects

If you are going to be working on a larger project, where you know you're going to be customizing almost everything or don't want it to look like a Bootstrap site, then the Bourbon suite is the way to go.  For one, you won't be fighting against existing style rules the whole time, and instead have a cleaner base to work up from.  Also, your end result is going to be a much more minimal set of CSS for the browser to download and process.  And with all the other benefits, such as semantic HTML and cleaner separation of HTML and CSS, the project will most likely be easier to maintain in the long run.  So in that aspect, Bourbon, Neat, Bitters and Refills are the way to go.

### Final thoughts

As with most things, there is "a right tool for job."  The bourbon suite does not replace Bootstrap, or even come close to competing with it for simple projects or prototypes that need to get something decent done in a short amount of time.  Bourbon is also not a good fit for programmers that just need to get something done that looks decent enough.

However, for anything else, Bourbon, Bourbon Neat, Bitters and Refills will overall give you a much better result and be a better base to build on.  Control freaks like me will really appreciate knowing exactly what every line of CSS is doing to the page.

In the end it all depends on the type of project you're working on, and I'm really happy that there is a choice.

If you want to see how I put it all together for a real, working example of Bourbon, you can check out the source for this blog on [GitHub](https://github.com/nshafer/lotechnica/tree/master/theme/static/styles).  Look at `theme.scss`, which is compiled down to `theme.css`.
