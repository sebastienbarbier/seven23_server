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
			//alert('TEST');

			setTimeout(function() {
				$('#login_page').removeClass('not_loaded');
			}, 200);

			$("#login_form").submit(function(){

				ws.post({
					url: ws.v1.login,
					data: $("#login_form").serialize()
				}).done(function(json){
					// We save token in sessionStorage
					$('#login_page').addClass('not_loaded');
					setTimeout(function() {
						ws.setToken(json.token);
						ws.get({
							url: ws.init,
							async: false
						}).done(function(json) {
							storage.init(json.id, function(){
								$('body').addClass('app');
								Backbone.history.navigate("#/dashboard", {trigger: true});
							});

						});
					}, 200);
				});

				return false;
			});

		}
	});

	return LoginView;

});
