//Filename: router.js

define([
		'jquery',
		'underscore',
		'backbone',
		'loginView',
		'ws',
		'dashboardView',
		'transactionsView',
		'debitscreditsFormView',
		'changesFormView',
		'categoriesView',
		'categoriesFormView',
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
		DebitscreditsFormView,
		ChangesFormView,
		CategoriesView,
		CategoriesFormView,
		InitView,
		SettingsView) {

		var AppRouter = Backbone.Router.extend({
			routes: {
				// Define some URL routes
				'home': 'home',
				'dashboard': 'dashboard',
				'transactions': 'transactions',
				'transactions/:year': 'transactions',
				'transactions/:year/:month': 'transactions',
				'transactions/:year/:month/debitscredits/add': 'debitcreditsForm',
				'transactions/:year/:month/debitscredits/edit/:id': 'debitcreditsForm',
				'transactions/:year/:month/changes/add': 'changesForm',
				'transactions/:year/:month/changes/edit/:id': 'changesForm',
				'categories': 'categories',
				'categories/add': 'categoriesForm',
				'categories/edit/:id': 'categoriesForm',
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

			// As above, call render on our loaded module
			// 'views/users/list'
			app_router.on('route:dashboard', function() {
				var dashboardView = new DashboardView();
				dashboardView.render();
			});

			app_router.on('route:transactions', function(year, month) {
				var transactionView = new TransactionsView();
				transactionView.render(year, month);
			});

			app_router.on('route:debitcreditsForm', function(year, month, id) {
				var transactionView = new DebitscreditsFormView();
				transactionView.render(year, month, id);
			});

			app_router.on('route:changesForm', function(year, month, id) {
				var transactionView = new ChangesFormView();
				transactionView.render(year, month, id);
			});

			app_router.on('route:categories', function() {
				var dashboardView = new CategoriesView();
				dashboardView.render();
			});

			app_router.on('route:categoriesForm', function(categorie_id) {
				var dashboardView = new CategoriesFormView();
				dashboardView.render(categorie_id);
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
