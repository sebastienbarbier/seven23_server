/*global require*/
'use strict';

require.config({
    paths: {
        // Librairies dependancies
		jquery                  : '../../bower_components/jquery/dist/jquery',
		underscore              : '../bower_components/lodash/dist/lodash',
		backbone                : '../../bower_components/backbone/backbone',
		css                     : '../../bower_components/require-css/css',
		text                    : '../../bower_components/requirejs-text/text',
		requirejs               : '../../bower_components/requirejs/require',
		mustache                : '../../bower_components/mustache.js/mustache',
		modernizr               : '../../bower_components/modernizr/modernizr',
		moment                  : '../../bower_components/moment/moment',
		bootstrap               : '../../bower_components/bootstrap/dist/js/bootstrap.min',
		'bootstrap-iconpicker'  : '../../bower_components/bootstrap-iconpicker/bootstrap-iconpicker/js/bootstrap-iconpicker.min',
		'bootstrap-colorpicker' : '../../bower_components/mjolnic-bootstrap-colorpicker/dist/js/bootstrap-colorpicker.min',
		'bootstrap-datepicker'  : '../../bower_components/bootstrap-datepicker/js/bootstrap-datepicker',
		// mocha                : '../../bower_components/mocha/mocha',
		// lodash               : '../../bower_components/lodash/dist/lodash.compat',
		// chai                 : '../../bower_components/chai/chai',
		// fastclick            : '../../bower_components/fastclick/lib/fastclick',
		// App structure
		app                     : 'app',
		router                  : 'router',
		storage                 : 'storage',
		// Models
		userModel               : 'models/userModel',
		categoryModel           : 'models/categoryModel',
		changesModel            : 'models/changesModel',
		debitsCreditsModel      : 'models/debitsCreditsModel',
		currencyModel           : 'models/currencyModel',
		// Collections
		categoryCollection      : 'collections/categoryCollection',
		debitsCreditsCollection : 'collections/debitsCreditsCollection',
		changesCollection       : 'collections/changesCollection',
		currenciesCollection    : 'collections/currenciesCollection',
		// Views
		initView                : 'views/InitView',
		loginView               : 'views/LoginView',
		dashboardView           : 'views/DashboardView',
		yearView                : 'views/transactions/YearView',
		transactionsView        : 'views/transactions/TransactionsView',
		debitscreditsFormView   : 'views/transactions/DebitsCreditsFormView',
		changesFormView         : 'views/transactions/ChangesFormView',
		categoriesView          : 'views/categories/categoriesView',
		categoriesFormView      : 'views/categories/categoriesFormView',
		settingsView            : 'views/SettingsView',
		'404View'               : 'views/404View',
    },
    shim: {
    	'bootstrap': {
			deps: ['jquery'],
    	},
        'bootstrap-iconpicker': {
            deps: ['bootstrap', '../../bower_components/bootstrap-iconpicker/bootstrap-iconpicker/js/iconset/iconset-fontawesome-4.2.0.min'],
        },
        'bootstrap-colorpicker': {
            deps: ['css!../../bower_components/mjolnic-bootstrap-colorpicker/dist/css/bootstrap-colorpicker.min.css'],
        },
        'bootstrap-datepicker': {
            deps: ['css!../../bower_components/bootstrap-datepicker/css/datepicker3.css'],
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
