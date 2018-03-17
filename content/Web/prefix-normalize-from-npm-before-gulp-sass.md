Title: Prefix normalize.css or sanitize.css before gulp-sass
Date: 2018-03-17
Status: published
Tags: gulp, sass, css

A pretty common setup for front-end design work is to use Sass to compile .scss files into a single .css file.
It's also pretty common to use a CSS Reset, such as [normalize.css](https://github.com/necolas/normalize.css)
or [sanitize.css](https://github.com/jonathantneal/sanitize.css), to reset your CSS to a common base.
For that CSS Reset to work, it needs to be included before any of the app-specific CSS, so you can override it and not
the other way around. You could just copy the **normalize.css** file into your project and link it separately in your
HTML, or you could even stick it in your `scss/` directory and have Sass process it unnecessarily. But what if you want
to just install it from **npm** and have gulp include it in your output `app.css` file? Here's a quick and easy way to
do that in your `gulpfile.js`.

This assumes you have a basic gulp setup with:

```bash
$ npm install -D gulp gulp-sass gulp-concat
```

And assuming you have a `gulp.task()` like the following:

```javascript

var gulp = require('gulp'),
    sass = require('gulp-sass'),
    concat = require('gulp-concat');

gulp.task('css', function () {
    return gulp.src('scss/**/*.scss')
        .pipe(sass().on('error', sass.logError))
        .pipe(concat('app.css'))
        .pipe(gulp.dest('css/'));
});
```

Now you install **normalize.css** with the following:

```bash
$ npm install --save normalize.css
```

which will stick it in your `node_modules/` subdirectory. How do you tell Gulp to just include that file, then run Sass
on your `*.scss` files, and output it all to `css/app.css`? The solution is to create two streams and use the package
[merge-stream](https://github.com/grncdr/merge-stream) to merge them together before concatenating. So install
**merge-stream**:

```bash
$ npm install -D merge-stream
```

Then create 2 separate streams, one for the normalize CSS (and any other NPM installed CSS files you might want to use),
the other for your Sass processed files. Finally merge them, concatenate, and output. Your `gulpfile.js` will look like
the following:

```javascript
var gulp = require('gulp'),
    sass = require('gulp-sass'),
    concat = require('gulp-concat'),
    merge = require('merge-stream');

gulp.task('css', function () {
    const reset = gulp.src('node_modules/normalize.css/normalize.css');

    const scss = gulp.src('scss/**/*.scss')
        .pipe(sass().on('error', sass.logError));

    return merge(reset, scss)
        .pipe(concat('app.css'))
        .pipe(gulp.dest('css/'));
});
```

Your `css/app.css` will now contain the contents of **normalize.css** followed by all of your CSS compiled by Sass.
Whenever you update your **normalize.css** package from NPM, your output will be automatically updated. Unless you pin
a specific version of **normalize.css** which may be a good idea depending on your project.
