/*global require*/
'use strict';

require.config({
	paths: {
		// Librairies dependancies
		jquery: '../../bower_components/jquery/dist/jquery',
		underscore: '../bower_components/lodash/dist/lodash',
		backbone: '../../bower_components/backbone/backbone',
		'requirejs-text': '../../bower_components/requirejs-text/text',
		requirejs: '../../bower_components/requirejs/require',
		mustache: '../../bower_components/mustache.js/mustache',
		modernizr: '../../bower_components/modernizr/modernizr',
		mocha: '../../bower_components/mocha/mocha',
		lodash: '../../bower_components/lodash/dist/lodash.compat',
		chai: '../../bower_components/chai/chai',
		// App structure
		app: 'app',
		router: 'router',
		// Models
		userModel: 'models/userModel',
		// Views
		loginView: 'views/LoginView',
		dashboardView: 'views/DashboardView',
		// Library
		'eve': 'libs/eve',
		'raphael-core': 'libs/raphael.core',
		'raphael-svg': 'libs/raphael.svg',
		'raphael-vml': 'libs/raphael.vml',
		'raphael': 'libs/raphael.amd',
		'livicons': 'libs/livicons-1.3.min'
	},
	shim: {
		'raphael': {
			exports: "Raphael"
		},
		'livicons': {
			deps: ['raphael']
		}
	}
});

require(['app'], function(App) {
	// We first intialize our apllication.
	App.initialize();

	require(['livicons']);
});
