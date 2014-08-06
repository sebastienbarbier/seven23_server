module.exports = function( grunt ) {
  'use strict';
  //
  // Grunt configuration:
  //
  // https://github.com/cowboy/grunt/blob/master/docs/getting_started.md
  //
  grunt.loadNpmTasks('grunt-recess');
  grunt.initConfig({

    // Project configuration
    // ---------------------

    // specify an alternate install location for Bower
    bower: {
      dir: 'app/components'
    },

    // Coffee to JS compilation
    coffee: {
      compile: {
        files: {
          'temp/javascripts/*.js': 'app/javascripts/**/*.coffee'
        },
        options: {
          basePath: 'app/javascripts'
        }
      }
    },

    // compile .scss/.sass to .css using Compass
    compass: {
      dist: {
        // http://compass-style.org/help/tutorials/configuration-reference/#configuration-properties
        options: {
          css_dir: 'temp/stylesheets',
          sass_dir: 'app/stylesheets',
          images_dir: 'app/images',
          javascripts_dir: 'temp/javascripts',
          force: true
        }
      }
    },

    // compile .less to .css using Recess
    recess: {
      dist: {
        src: [
          'app/less/app.less'
        ],
        dest: 'app/stylesheets/app.css',
        options: {
          compile: true,
          compress: true
        }
      }
    },

    // generate application cache manifest
    manifest:{
      dest: ''
    },

    // headless testing through PhantomJS
    mocha: {
      all: ['test/**/*.html']
    },

    // default watch configuration
    watch: {
      coffee: {
        files: 'app/javascripts/**/*.coffee',
        tasks: 'coffee reload'
      },
      compass: {
        files: [
          'app/stylesheets/**/*.{scss,sass}'
        ],
        tasks: 'compass reload'
      },
      recess: {
        files: [
          'app/components/bootstrap/less/**/*.less',
          'app/less/**/*.less'
        ],
        tasks: 'recess reload'
      },
      reload: {
        files: [
          'app/*.html',
          'app/stylesheets/**/*.css',
          'app/javascripts/**/*.js',
          'app/images/**/*'
        ],
        tasks: 'reload'
      }
    },

    // default lint configuration, change this to match your setup:
    // https://github.com/cowboy/grunt/blob/master/docs/task_lint.md#lint-built-in-task
    lint: {
      files: [
        'Gruntfile.js',
        'app/javascripts/**/*.js',
        'spec/**/*.js'
      ]
    },

    // specifying JSHint options and globals
    // https://github.com/cowboy/grunt/blob/master/docs/task_lint.md#specifying-jshint-options-and-globals
    jshint: {
      options: {
        curly: true,
        eqeqeq: true,
        immed: true,
        latedef: true,
        newcap: true,
        noarg: true,
        sub: true,
        undef: true,
        boss: true,
        eqnull: true,
        browser: true
      },
      globals: {
        jQuery: true
      }
    },

    // Build configuration
    // -------------------

    // the staging directory used during the process
    staging: 'temp',
    // final build output
    output: 'dist',

    mkdirs: {
      staging: 'app/'
    },

    // Below, all paths are relative to the staging directory, which is a copy
    // of the app/ directory. Any .gitignore, .ignore and .buildignore file
    // that might appear in the app/ tree are used to ignore these values
    // during the copy process.

    // concat css/**/*.css files, inline @import, output a single minified css
    css: {
      'stylesheets/app.css': ['stylesheets/**/*.css']
    },

    // renames JS/CSS to prepend a hash of their contents for easier
    // versioning
    rev: {
      js: 'javascripts/**/*.js',
      css: 'stylesheets/**/*.css',
      img: 'images/**'
    },

    // usemin handler should point to the file containing
    // the usemin blocks to be parsed
    'usemin-handler': {
      html: 'index.html'
    },

    // update references in HTML/CSS to revved files
    usemin: {
      // html: ['**/*.html'],
      css: ['**/*.css']
    },

    // HTML minification
    html: {
      // files: ['**/*.html']
    },

    // Optimizes JPGs and PNGs (with jpegtran & optipng)
    img: {
      dist: '<config:rev.img>'
    },

    // rjs configuration. You don't necessarily need to specify the typical
    // `path` configuration, the rjs task will parse these values from your
    // main module, using http://requirejs.org/docs/optimization.html#mainConfigFile
    //
    // name / out / mainConfig file should be used. You can let it blank if
    // you're using usemin-handler to parse rjs config from markup (default
    // setup)
    rjs: {
      optimize: 'none',  // no minification, is done by the min task
      // optimize: 'uglify',  // minify
      baseUrl: './javascripts',
      wrap: true,
      name: 'main',
      mainConfigFile: './javascripts/main.js',
      pragmasOnSave: {
        excludeJade : true
      },
      paths: {
        backbone: '../components/backbone/backbone-min'
      , bootstrap: '../components/bootstrap/bootstrap/js/bootstrap.min'
      , jade: '../components/require-jade/jade'
      , jquery: '../components/jquery/jquery.min'
      , underscore: '../components/underscore/underscore-min'
      },
      out: 'app.min.js'
    },

    // While Yeoman handles concat/min when using
    // usemin blocks, you can still use them manually
    concat: {
      dist: ''
    },

    min: {
      dist: ''
    }
  });

  // Alias the `test` task to run the `mocha` task instead
  grunt.registerTask('test', 'server:phantom mocha');

  // Create new `recess-init` task to run `recess` during initial init
  grunt.registerTask('recess-init', function() {
    grunt.loadNpmTasks('grunt-recess');
    grunt.task.run('recess');
  });
};
