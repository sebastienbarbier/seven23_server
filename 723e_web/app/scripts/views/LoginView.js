define([
	'jquery',
	'underscore',
	'backbone',
	'mustache',
	'ws',
	'text!templates/login.mustache',
	'storage'
], function($, _, Backbone, Mustache, ws, loginTemplate, storage) {

	var LoginView = Backbone.View.extend({
		el: $("#page"),

		render: function() {

			var template = Mustache.render(loginTemplate);

			this.$el.html(template);

			$("#login_form").submit(function(){

				ws.post({
					url: ws.v1.login,
					data: $("#login_form").serialize()
				}).done(function(json){
						// We save token in sessionStorage
						ws.setToken(json.token);
						storage.init(json.id, function(){
							Backbone.history.navigate("#/dashboard", {trigger: true});
						});

				});

				return false;
			});
		}
	});

	return LoginView;

});
