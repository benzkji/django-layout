var gulp = require('gulp'),
    sass = require('gulp-sass'),
    autoprefixer = require('gulp-autoprefixer'),
    shell = require('gulp-shell'),
    jshint= require('gulp-jshint'),
    livereload = require('gulp-livereload'),
    dummy = 'last';

// fix Promise() error from whiche package again?
require('es6-promise').polyfill();
var static_path = './{{ project_name }}/static/{{ project_name }}/';


gulp.task('sass', function () {
    gulp.src(wti_static + 'sass/screen.sass')
        .pipe(sass().on('error', sass.logError))
        .pipe(autoprefixer("last 2 versions"))
        .pipe(gulp.dest(wti_static + 'css/'))
        .pipe(livereload());
});

gulp.task('jshint', function () {
    gulp.src(['gulpfile.js', wti_static + 'js/**.js'])
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
            'pip-sync requirements/dev.txt',
        ]
    )
);

gulp.task('livereload', function (evt) {
    livereload.changed({
        body: {
            files: [evt.path]
        }
    });
});

gulp.task('default', ['sass', 'jshint', 'flake8']);

gulp.task('watch', function () {
    livereload.listen();
    gulp.watch('**/*.html', ['livereload']);
    gulp.watch(static_path + '**/*.sass', ['sass']);
    gulp.watch(['gulpfile.js', static_path + 'js/**.js'], ['jshint']);
    gulp.watch('./**/*.py', ['flake8', 'livereload']);
    gulp.watch('./requirements/*.in', ['pip-compile']);
});
