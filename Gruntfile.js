module.exports = function(grunt) {

  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),
    compass: {                              // Task
      dist: {                            // Target
      }
    },
    webfont: {
      icons: {
        src: '{{project_name}}/static/{{project_name}}/iconfont-source/*.svg',
        dest: '{{project_name}}/static/{{project_name}}/iconfont',
        options: {
          font: "icons",
          hashes: true
        }
      }
    },
    jshint: {
      js_file: ['Gruntfile.js',
                '{{project_name}}/static/{{project_name}}/js/*.js'
             ],
      options: {
        // options here to override JSHint defaults
        globals: {
          jQuery: true,
          console: true,
          module: true,
          document: true
        }
      }
    },
    flake8: {
      src: ['**.py']
    },
    githooks: {
      all: {
        // Will run the jshint and test:unit tasks at every commit
        'pre-commit': 'jshint flake8 compass webfont'
      }
    },
    watch: {
      compass: {
        files: ['{{project_name}}/static/{{project_name}}/sass/**'],
        tasks: ['compass'],
        options: {
          spawn: false
        }
      },
      webfont: {
        //files: ['static/cooalaapp/icons/svg/*'],
        files: ['{{project_name}}/static/{{project_name}}/iconfont-source/*.svg'],
        tasks: ['webfont'],
        options: {
          spawn: false
        }
      },
      jshint: {
        files: ['{{project_name}}/static/{{project_name}}/js/**'],
        tasks: ['jshint'],
        options: {
          spawn: false
        }
      },
      flake8: {
        files: ['**.py'],
        tasks: ['flake8'],
        options: {
          spawn: false
        }
      }
    }
  });

  // do something useful
  grunt.loadNpmTasks('grunt-contrib-compass');
  grunt.loadNpmTasks('grunt-webfont');
  // grunt.loadNpmTasks('grunt-svgstore');
  // analyzers
  grunt.loadNpmTasks('grunt-contrib-jshint');
  grunt.loadNpmTasks('grunt-flake8');
  // helpers
  grunt.loadNpmTasks('grunt-contrib-watch');
  grunt.loadNpmTasks('grunt-githooks');

  //grunt.loadNpmTasks('grunt-contrib-concat');
  //grunt.loadNpmTasks('grunt-contrib-uglify');
  //grunt.loadNpmTasks('grunt-contrib-qunit');

  grunt.registerTask('default', ['compass', 'svgstore', 'webfont', 'jshint', 'githooks', 'flake8'  ]);

};


/*
archive:
    svgstore: {
      options: {
        prefix : '', // This will prefix each <g> ID,
        cleanup: ["fill", "stroke"],
        svg: { // will be added as attributes to the resulting SVG
          viewBox : '0 0 100 100',
          xmlns : "http://www.w3.org/2000/svg"
        },
        formatting : {
          indent_size : 2
        }
      },
      default: {
        files: {
          '{{project_name}}/static/{{project_name}}/svg/icons.svg': ['{{project_name}}/static/{{project_name}}/svg_source/*.svg']
        }
      }
    },

    svg: {
      //files: ['static/cooalaapp/icons/svg/*'],
      files: ['{{project_name}}/static/{{project_name}}/svg_source/*.svg'],
      tasks: ['svgstore'],
      options: {
        spawn: true
      }
    },

 */
