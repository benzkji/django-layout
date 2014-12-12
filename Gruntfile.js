module.exports = function(grunt) {

  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),
//    jshint: {
//      js_file: ['Gruntfile.js',
//                '{{project_name}}/static/{{project_name}}/js/*.js'
//             ],
//      options: {
//        // options here to override JSHint defaults
//        globals: {
//          jQuery: true,
//          console: true,
//          module: true,
//          document: true
//        }
//      }
//    },
    compass: {                              // Task
      dist: {                            // Target
      }
    },
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
          '{{project_name}}/static/{{project_name}}/svg/icons.svg': ['{{project_name}}/static/{{project_name}}/svg-source/*.svg']
        }
      }
    },
    watch: {
      svg: {
        //files: ['static/cooalaapp/icons/svg/*'],
        files: ['{{project_name}}/static/{{project_name}}/svg-source/*.svg'],
        tasks: ['svgstore'],
        options: {
          spawn: true
        }
      },
      sass: {
        files: ['{{project_name}}/static/{{project_name}}/sass/**'],
        tasks: ['compass'],
        options: {
          spawn: true
        }
      }
//      js: {
//        files: ['src/ferienpass/theme/theme/static/js/**'],
//        tasks: ['jshint'],
//        options: {
//          spawn: true
//        }
//      }
    }
  });

  grunt.loadNpmTasks('grunt-contrib-watch');
  //grunt.loadNpmTasks('grunt-contrib-jshint');
  grunt.loadNpmTasks('grunt-contrib-compass');
  grunt.loadNpmTasks('grunt-svgstore');

  //grunt.loadNpmTasks('grunt-contrib-concat');
  //grunt.loadNpmTasks('grunt-contrib-uglify');
  //grunt.loadNpmTasks('grunt-contrib-qunit');

  //grunt.registerTask('test', ['jshint']);
  //grunt.registerTask('default', ['compass', 'svgstore', 'jshint']);
  grunt.registerTask('default', ['compass', 'svgstore'
  ]);

};
