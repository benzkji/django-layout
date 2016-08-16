var gulp = require('gulp'),
    sass = require('gulp-sass'),
    consolidate = require('gulp-consolidate'),
    autoprefixer = require('gulp-autoprefixer'),
    shell = require('gulp-shell'),
    jshint= require('gulp-jshint'),
    livereload = require('gulp-livereload'),

    // iconfont = require('gulp-iconfont'),

    // svgstore = require('gulp-svgstore'),
    // svgmin = require('gulp-svgmin'),
    // path = require('path'),

    dummy = 'last';

// fix Promise() error from whiche package again?
require('es6-promise').polyfill();
var static_path = 'apps/{{ project_name }}/static/{{ project_name }}/';

gulp.task('sass', function () {
    gulp.src(static_path + 'sass/screen.sass')
        .pipe(sass().on('error', sass.logError))
        .pipe(autoprefixer("last 2 versions"))
        .pipe(gulp.dest(static_path + 'css/'))
});

// todo: remove FILL!
gulp.task('svgstore', function () {
    return gulp
        .src(static_path + 'svgstore/*.svg')
        .pipe(cheerio({
            run: function ($) {
                //console.log($.xml());
                $('[fill]').removeAttr('fill');
                $('[style]').removeAttr('style');
            },
            parserOptions: { xmlMode: true }
        }))
        .pipe(svgmin(function (file) {
            var prefix = path.basename(file.relative, path.extname(file.relative));
            return {
                plugins: [{
                    cleanupIDs: {
                        prefix: prefix + '-',
                        minify: true
                    }
                }]
            }
        }))
        .pipe(svgstore({'inlineSvg': true}))
        .pipe(gulp.dest(static_path + '../../templates/{{ project_name }}/svgstore/'));
});

gulp.task('icons', function () {
    var runTimestamp = Math.round(Date.now()/1000);
    return gulp.src([static_path + 'iconfont/svg/*.svg'])
        .pipe(iconfont({
                fontName: 'icons', // required
                normalize: true, // recommended option
                appendUnicode: false,
                fontHeight: 1000,
                formats: ['ttf', 'eot', 'woff'], // default, 'woff2' and 'svg' are available
                timestamp: runTimestamp // recommended to get consistent builds when watching files
            }
        )
    ).on('glyphs', function(glyphs, options) {
        // CSS templating, e.g.
        console.log(glyphs, options);
        gulp.src(static_path + 'iconfont/scss/_iconfont.scss')
            .pipe(consolidate('lodash', {
                glyphs: glyphs,
                fontName: 'icons',
                fontPath: '../iconfont/font/',
                className: 'icon'
            })
        )
        .pipe(gulp.dest(static_path + 'sass/'));
    })
    .pipe(gulp.dest(static_path + 'iconfont/font/'));
});

gulp.task('jshint', function () {
    gulp.src(['gulpfile.js', static_path + 'js/**.js'])
        .pipe(jshint())
        .pipe(livereload());
});

gulp.task('flake8', shell.task(
        ['flake8 --ignore=errors']
    )
);

gulp.task('pip-compile', shell.task(
        [
            'pip-compile requirements/dev.in',
            'pip-compile requirements/deploy.in',
            // let it get a bit older, until it really works
            // 'pip-sync requirements/dev.txt',
            'pip install -r requirements/dev.txt',
        ]
    )
);

gulp.task('default', ['sass', 'pip-compile', 'jshint', 'flake8']);

gulp.task('watch', function () {
    livereload.listen();
    gulp.watch(['**/*.html', '**/*.py', '**/*.css']).on('change', livereload.changed);
    gulp.watch(static_path + 'sass/*.sass', ['sass']);
    gulp.watch(['gulpfile.js', static_path + 'js/**.js'], ['jshint']);
    gulp.watch('**/*.py', ['flake8']);
    gulp.watch('requirements/*.in', ['pip-compile']);
});

