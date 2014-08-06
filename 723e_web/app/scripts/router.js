//Filename: router.js

define([
	'jquery',
	'underscore',
	'backbone',
	'loginView',
	'ws',
	'dashboardView'
], function($, _, Backbone, LoginView, ws, DashboardView) {

	var AppRouter = Backbone.Router.extend({
		routes: {
			// Define some URL routes
			'home': 'home',
			'dashboard': 'dashboard',
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
			// var userListView = new UserListView();
			// userListView.render();
			console.log('Dashboard');
			var dashboardView = new DashboardView();
			dashboardView.render();

			ws.get({
				url: ws.v1.accounts,
			}).done(function(json) {
				console.log(json);
			})
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
