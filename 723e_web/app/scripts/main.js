/*global require*/
'use strict';

require.config({
	paths: {
		// Librairies dependancies
		jquery                    : '../../bower_components/jquery/dist/jquery',
		underscore                : '../bower_components/lodash/dist/lodash',
		backbone                  : '../../bower_components/backbone/backbone',
		css                       : '../../bower_components/require-css/css',
		text                      : '../../bower_components/requirejs-text/text',
		requirejs                 : '../../bower_components/requirejs/require',
		mustache                  : '../../bower_components/mustache.js/mustache',
		modernizr                 : '../../bower_components/modernizr/modernizr',
		moment                    : '../../bower_components/moment/moment',
		bootstrap                 : '../../bower_components/bootstrap/dist/js/bootstrap.min',
		'bootstrap-iconpicker'    : '../../bower_components/bootstrap-iconpicker/bootstrap-iconpicker/js/bootstrap-iconpicker.min',
		'bootstrap-iconpicker-fa' : '../../bower_components/bootstrap-iconpicker/bootstrap-iconpicker/js/iconset/iconset-fontawesome-4.2.0.min',
		'bootstrap-colorpicker'   : '../../bower_components/mjolnic-bootstrap-colorpicker/dist/js/bootstrap-colorpicker.min',
		// mocha                  : '../../bower_components/mocha/mocha',
		// lodash                 : '../../bower_components/lodash/dist/lodash.compat',
		// chai                   : '../../bower_components/chai/chai',
		// fastclick              : '../../bower_components/fastclick/lib/fastclick',
		// App structure
		app                       : 'app',
		router                    : 'router',
		// Models
		userModel                 : 'models/userModel',
		categoryModel             : 'models/categoryModel',
		changesModel              : 'models/changesModel',
		debitsCreditsModel        : 'models/debitsCreditsModel',
		currencyModel             : 'models/currencyModel',
		// Collections
		categoryCollection        : 'collections/categoryCollection',
		debitsCreditsCollection   : 'collections/debitsCreditsCollection',
		changesCollection         : 'collections/changesCollection',
		currenciesCollection      : 'collections/currenciesCollection',
		// Views
		initView                  : 'views/InitView',
		loginView                 : 'views/LoginView',
		dashboardView             : 'views/DashboardView',
		transactionsView          : 'views/TransactionsView',
		categoriesView            : 'views/categories/categoriesView',
		categoriesFormView        : 'views/categories/categoriesFormView',
		settingsView              : 'views/SettingsView',
	},
	shim: {
		'bootstrap-iconpicker': {
			deps: ['bootstrap', 'bootstrap-iconpicker-fa'],
		},
		'bootstrap-colorpicker': {
			deps: ['css!../../bower_components/mjolnic-bootstrap-colorpicker/dist/css/bootstrap-colorpicker.min.css'],
		}
	}
});

require(['app'], function(App, moment) {
	// We first intialize our application.
	App.initialize();

	// Supposed to implement fastclick.
	// var attachFastClick = require(['fastclick']);
	// attachFastClick(document.body);

});
