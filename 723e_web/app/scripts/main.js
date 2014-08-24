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
		// mocha: '../../bower_components/mocha/mocha',
		// lodash: '../../bower_components/lodash/dist/lodash.compat',
		// chai: '../../bower_components/chai/chai',
		// fastclick: '../../bower_components/fastclick/lib/fastclick',
		// App structure
		app: 'app',
		router: 'router',
		// Models
		userModel: 'models/userModel',
		// Views
		initView: 'views/InitView',
		loginView: 'views/LoginView',
		dashboardView: 'views/DashboardView',
		transactionsView: 'views/TransactionsView',
		categoriesView: 'views/CategoriesView',
		settingsView: 'views/SettingsView',
	}
});

require(['app'], function(App) {

	// We first intialize our application.
	App.initialize();

	// Supposed to implement fastclick.
	// var attachFastClick = require(['fastclick']);
	// attachFastClick(document.body);


});
