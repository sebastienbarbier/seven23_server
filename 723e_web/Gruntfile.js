'use strict';
var LIVERELOAD_PORT = 35729;
var SERVER_PORT = 9000;
var lrSnippet = require('connect-livereload')({
	port: LIVERELOAD_PORT
});
var mountFolder = function(connect, dir) {
	return connect.static(require('path').resolve(dir));
};

// # Globbing
// for performance reasons we're only matching one level down:
// 'test/spec/{,*/}*.js'
// use this if you want to match all subfolders:
// 'test/spec/**/*.js'
// templateFramework: 'lodash'

module.exports = function(grunt) {
	// show elapsed time at the end
	require('time-grunt')(grunt);
	// load all grunt tasks
	require('load-grunt-tasks')(grunt);

	// grunt.loadNpmTasks('grunt-contrib-less');

	// configurable paths
	var yeomanConfig = {
		app: 'app',
		dist: 'dist'
	};

	grunt.initConfig({
		yeoman: yeomanConfig,
		watch: {
			options: {
				nospawn: true,
				livereload: true
			},
			livereload: {
				options: {
					livereload: grunt.option('livereloadport') || LIVERELOAD_PORT
				},
				files: [
					'<%= yeoman.app %>/*.html',
					'{.tmp,<%= yeoman.app %>}/styles/css/{,*/}*.css',
					'{.tmp,<%= yeoman.app %>}/scripts/{,*/}*.js',
					'<%= yeoman.app %>/images/{,*/}*.{png,jpg,jpeg,gif,webp}',
					'<%= yeoman.app %>/scripts/templates/{,*/}*.{ejs,mustache,hbs}',
					'test/spec/**/*.js'
				]
			},
			jst: {
				files: [
					'<%= yeoman.app %>/scripts/templates/*.ejs'
				],
				tasks: ['jst']
			},
			less2css: {
				files: ['<%= yeoman.app %>/styles/less/{,*/}*.less'],
				tasks: ['less:production']
			},
			test: {
				files: ['<%= yeoman.app %>/scripts/{,*/}*.js', 'test/spec/**/*.js'],
				tasks: ['test:true']
			}
		},
		connect: {
			options: {
				port: grunt.option('port') || SERVER_PORT,
				// change this to '0.0.0.0' to access the server from outside
				hostname: '0.0.0.0'
			},
			livereload: {
				options: {
					middleware: function(connect) {
						return [
							lrSnippet,
							mountFolder(connect, '.tmp'),
							mountFolder(connect, yeomanConfig.app),
							mountFolder(connect, '.')
						];
					}
				}
			},
			test: {
				options: {
					port: 9001,
					middleware: function(connect) {
						return [
							lrSnippet,
							mountFolder(connect, '.tmp'),
							mountFolder(connect, 'test'),
							mountFolder(connect, yeomanConfig.app)
						];
					}
				}
			},
			dist: {
				options: {
					middleware: function(connect) {
						return [
							mountFolder(connect, yeomanConfig.dist)
						];
					}
				}
			}
		},
		open: {
			server: {
				path: 'http://localhost:<%= connect.options.port %>'
			},
			test: {
				path: 'http://localhost:<%= connect.test.options.port %>'
			}
		},
		clean: {
			dist: ['.tmp', '<%= yeoman.dist %>/*'],
			server: '.tmp'
		},
		jshint: {
			options: {
				jshintrc: '.jshintrc',
				reporter: require('jshint-stylish')
			},
			all: [
				'Gruntfile.js',
				'<%= yeoman.app %>/scripts/{,*/}*.js',
				'!<%= yeoman.app %>/scripts/vendor/*',
				'test/spec/{,*/}*.js'
			]
		},
		mocha: {
			all: {
				options: {
					run: true,
					urls: ['http://localhost:<%= connect.test.options.port %>/index.html']
				}
			}
		},
		requirejs: {
			dist: {
				// Options: https://github.com/jrburke/r.js/blob/master/build/example.build.js
				options: {
					baseUrl: '<%= yeoman.app %>/scripts',
					optimize: 'none',
					mainConfigFile: 'app/scripts/main.js',
					// TODO: Figure out how to make sourcemaps work with grunt-usemin
					// https://github.com/yeoman/grunt-usemin/issues/30
					//generateSourceMaps: true,
					// required to support SourceMaps
					// http://requirejs.org/docs/errors.html#sourcemapcomments
					preserveLicenseComments: false,
					useStrict: true,
					wrap: true
					//uglify2: {} // https://github.com/mishoo/UglifyJS2
				}
			}
		},
		useminPrepare: {
			html: '<%= yeoman.app %>/index.html',
			options: {
				dest: '<%= yeoman.dist %>'
			}
		},
		usemin: {
			html: ['<%= yeoman.dist %>/{,*/}*.html'],
			options: {
				dirs: ['<%= yeoman.dist %>']
			}
		},
		imagemin: {
			dist: {
				files: [{
					expand: true,
					cwd: '<%= yeoman.app %>/images',
					src: '{,*/}*.{png,jpg,jpeg}',
					dest: '<%= yeoman.dist %>/images'
				}]
			}
		},
		htmlmin: {
			dist: {
				options: {
					/*removeCommentsFromCDATA: true,
                    // https://github.com/yeoman/grunt-usemin/issues/44
                    //collapseWhitespace: true,
                    collapseBooleanAttributes: true,
                    removeAttributeQuotes: true,
                    removeRedundantAttributes: true,
                    useShortDoctype: true,
                    removeEmptyAttributes: true,
                    removeOptionalTags: true*/
				},
				files: [{
					expand: true,
					cwd: '<%= yeoman.app %>',
					src: '*.html',
					dest: '<%= yeoman.dist %>'
				}]
			}
		},
		copy: {
			dist: {
				files: [{
					expand: true,
					dot: true,
					cwd: '<%= yeoman.app %>',
					dest: '<%= yeoman.dist %>',
					src: [
						'*.{ico,txt}',
						'.htaccess',
						'scripts/requirejs.js',
						'images/{,*/}*.{webp,gif}',
						'styles/fonts/{,*/}*.*',
						'config.js',
					]
				},
				{
					expand: true,
					dot: true,
					cwd: '.',
					dest: '<%= yeoman.dist %>',
					src: [
						'bower_components/requirejs/require.js',
						'bower_components/moment/locale/fr',
						'bower_components/mjolnic-bootstrap-colorpicker/dist/img/bootstrap-colorpicker/saturation.png',
						'bower_components/bootstrap-iconpicker/bootstrap-iconpicker/js/bootstrap-iconpicker.min.js',
						'bower_components/mjolnic-bootstrap-colorpicker/dist/css/bootstrap-colorpicker.min.css',
						'bower_components/bootstrap-iconpicker/bootstrap-iconpicker/js/iconset/iconset-fontawesome-4.2.0.min.js',
						'bower_components/mjolnic-bootstrap-colorpicker/dist/js/bootstrap-colorpicker.min.js',
						'bower_components/mjolnic-bootstrap-colorpicker/dist/img/bootstrap-colorpicker/hue.png',
						'bower_components/mjolnic-bootstrap-colorpicker/dist/img/bootstrap-colorpicker/alpha.png',
						'bower_components/bootstrap-iconpicker/bootstrap-iconpicker/css/bootstrap-iconpicker.min.css'
					]
				},
				{
					expand: true,
					dot: true,
					cwd: 'bower_components/mjolnic-bootstrap-colorpicker/dist/img/bootstrap-colorpicker',
					dest: '<%= yeoman.dist %>/styles/img/bootstrap-colorpicker/',
					src: [
						'{,*/}*.png'
					]
				}]
			}
		},
		bower: {
			all: {
				rjsConfig: '<%= yeoman.app %>/scripts/main.js'
			}
		},
		jst: {
			options: {
				amd: true
			},
			compile: {
				files: {
					'.tmp/scripts/templates.js': ['<%= yeoman.app %>/scripts/templates/*.ejs']
				}
			}
		},
		rev: {
			dist: {
				files: {
					src: [
						'<%= yeoman.dist %>/scripts/{,*/}*.js',
						'<%= yeoman.dist %>/styles/{,*/}*.css',
						'<%= yeoman.dist %>/images/{,*/}*.{png,jpg,jpeg,gif,webp}',
						'/styles/fonts/{,*/}*.*',
					]
				}
			}
		},
		less: {
			production: {
				options: {
					paths: ["app/styles/less"],
					cleancss: true,
					compress: true
				},
				files: {
					"app/styles/css/main.css": "app/styles/less/main.less"
				}
			}
		}
	});


	grunt.registerTask('server', function(target) {
		grunt.log.warn('The `server` task has been deprecated. Use `grunt serve` to start a server.');
		grunt.task.run(['serve' + (target ? ':' + target : '')]);
	});

	grunt.registerTask('serve', function() {
		grunt.log.warn('You are using serve as a shortcut to serve-dev. You can also use serve-dist to run builded app.');
		grunt.task.run(['serve-dev']);
	});

	grunt.registerTask('serve-dist', function(target) {
		return grunt.task.run(['build', 'open:server', 'connect:dist:keepalive']);
	});

	grunt.registerTask('serve-dev', function(target) {

		if (target === 'test') {
			return grunt.task.run([
				'clean:server',
				'jst',
				'connect:test',
				'open:test',
				'watch'
			]);
		}

		grunt.task.run([
			'clean:server',
			'jst',
			'connect:livereload',
			'open:server',
			'watch'
		]);
	});

	grunt.registerTask('test', function(isConnected) {
		isConnected = Boolean(isConnected);
		var testTasks = [
			'clean:server',
			'jst',
			'connect:test',
			'mocha',
		];

		if (!isConnected) {
			return grunt.task.run(testTasks);
		} else {
			// already connected so not going to connect again, remove the connect:test task
			testTasks.splice(testTasks.indexOf('connect:test'), 1);
			return grunt.task.run(testTasks);
		}
	});

	grunt.registerTask('build', [
		'clean:dist',
		'less',
		'jst',
		'useminPrepare',
		'requirejs',
		'imagemin',
		'htmlmin',
		'concat',
		'cssmin',
		'uglify',
		'copy',
		'rev',
		'usemin'
	]);

	grunt.registerTask('default', [
		'jshint',
		'test',
		'build'
	]);
};
