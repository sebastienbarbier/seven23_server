define([
	'jquery',
	'underscore',
	'backbone',
	'mustache',
	'ws',
	'text!templates/login.mustache',
	'storage',
	'invitationModel'
], function($, _, Backbone, Mustache, ws, loginTemplate, storage, Invitation) {

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
				}).fail(function(error) {
					$('#login_page .error').addClass('show');
				});

				return false;
			});

			$("#send-request").submit(function () {
				var alertSuccess = $(".request .alert-success");
				var alertDanger = $(".request .alert-danger");
				var form = $("#send-request");

				var dict = { 
					email: $('#request-mail').val() 
				};

				var invite = new Invitation(dict);
				invite.save(dict, {
					success: function(model, response) {
						alertDanger.removeClass('show');
						alertSuccess.toggleClass('show');
						form.toggleClass('hide');
					},
					error: function(model, error) {
						alertDanger.addClass('show');
					}
				});
				return false;
			});

		}
	});

	return LoginView;

});
