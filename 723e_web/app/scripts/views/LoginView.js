define([
	'jquery',
	'underscore',
	'backbone',
	'mustache',
	'ws',
	'text!templates/login.mustache'
], function($, _, Backbone, Mustache, Ws, loginTemplate) {

	var LoginView = Backbone.View.extend({
		el: $("#page"),

		render: function() {
			console.log(Ws.v1.login);

			var template = Mustache.render(loginTemplate, {
				"url": Ws.v1.login
			});

			this.$el.html(template);
		}
	});

	return LoginView;

});
