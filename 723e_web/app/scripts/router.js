//Filename: router.js

define([
		'jquery',
		'underscore',
		'backbone',
		'loginView',
		'ws',
		'dashboardView',
		'transactionsView',
		'categoriesView',
		'initView',
		'settingsView'
	],
	function(
		$,
		_,
		Backbone,
		LoginView,
		ws,
		DashboardView,
		TransactionsView,
		CategoriesView,
		InitView,
		SettingsView) {

		var AppRouter = Backbone.Router.extend({
			routes: {
				// Define some URL routes
				'home': 'home',
				'dashboard': 'dashboard',
				'transactions/:year/:month': 'transactions',
				'transactions': 'transactions',
				'categories': 'categories',
				'settings': 'settings',
				// Error
				'error': 'error',
				'login': 'login',
				'logout': 'logout',
				// Default
				'*actions': 'defaultAction'
			}
		});

		var initialize = function() {

			var app_router = new AppRouter;

			app_router.on('route:home', function() {
				// Call render on the module we loaded in via the dependency array
				// 'views/projects/list'
				// var projectListView = new ProjectListView();
				// projectListView.render();
				console.log('Home');
			});
			// As above, call render on our loaded module
			// 'views/users/list'
			app_router.on('route:dashboard', function() {
				var dashboardView = new DashboardView();
				dashboardView.render();
			});

			app_router.on('route:transactions', function() {
				var transactionView = new TransactionsView();
				transactionView.render();
			});

			app_router.on('route:transactions', function(year, month) {
				var transactionView = new TransactionsView();
				transactionView.render(year, month);
			});

			app_router.on('route:categories', function() {
				var dashboardView = new CategoriesView();
				dashboardView.render();
			});

			app_router.on('route:settings', function() {
				var settingsView = new SettingsView();
				settingsView.render();
			});

			app_router.on('route:defaultAction', function(actions) {
				// We have no matching route, lets just log what the URL was
				console.log('No route:', actions);
			});


			app_router.on('route:login', function(actions) {
				// We have no matching route, lets just log what the URL was
				var loginView = new LoginView();
				loginView.render();
			});

			// This wiew delete tokenkey
			app_router.on('route:logout', function() {
				sessionStorage.removeItem("key");
				Backbone.history.navigate("#/login", {
					trigger: true
				});
			});

			app_router.on('route:error', function(actions) {
				alert("Serveur not available");
			});

			Backbone.history.start();
		};

		return {
			initialize: initialize
		};
	});
