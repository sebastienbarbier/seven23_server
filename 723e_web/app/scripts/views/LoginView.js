define([
	'jquery',
	'underscore',
	'backbone',
	'mustache',
	'ws',
	'text!templates/login.mustache',
	'storage',
	'subscriptionModel',
	'currenciesCollection'
], function($, _, Backbone, Mustache, ws, loginTemplate, storage, Subscription, CurrenciesCollection) {

	// Currencies for subscription form
	var currencies = new CurrenciesCollection();

	function initLoading(token) {
		// We save token in sessionStorage
		$('#login_page').addClass('not_loaded');
		setTimeout(function() {
			ws.setToken(token);
			ws.get({
				url: ws.init,
				async: false
			}).done(function(json) {
				storage.init(json.id, function(){
					$('body').addClass('app');
					Backbone.history.navigate("#/transactions", {trigger: true});
				});
			});
		}, 200);
	}

	var LoginView = Backbone.View.extend({
		el: $("#page"),

		render: function() {

			var template = Mustache.render(loginTemplate, {
				'server': ws.server.url(),
				'allowSubscription': APP_CONFIG.allowSubscription
			});

			this.$el.html(template);
			//alert('TEST');

			setTimeout(function() {
				$('#login_page').removeClass('not_loaded');
			}, 200);

			// Submit form
			$("#login_form").submit(function(){
				ws.post({
					url: ws.v1.login,
					data: $("#login_form").serialize()
				}).done(function(json){
					initLoading(json.token);
				}).fail(function(error) {
					$('#login_page .error').addClass('show');
				});

				return false;
			});


			// When click on subscribe
			$("#subscribe_form").submit(function(){
				var array = $("#subscribe_form").serializeArray();
				var dict = {};
				for (var i = 0; i < array.length; i++) {
					if (array[i]['value'] && array[i]['value'] != "") {
						dict[array[i]['name']] = array[i]['value']
					}
				}

				// Check if email is email synthax
				var sub = new Subscription(dict);

			    Backbone.Validation.bind(this, {
			      model: sub,
			      valid: function(view, attr) {

					// Check if all are required
				    $(view).find('input[name=' + attr + '], select[name=' + attr + ']')
				    	.parent()
				    	.removeClass('has-error')
				    	.addClass('has-success')
				    	.prev().html('');

			      },
			      invalid: function(view, attr, error) {

				    $(view).find('input[name=' + attr + '], select[name=' + attr + ']')
				    	.parent()
				    	.addClass('has-error')
				    	.removeClass('has-success')
				    	.prev().html(error);

			      }
			    });

				sub.validate();

				if (sub.isValid()) {
					sub.save(null, {
						wait: true,
						success: function(model, response) {
							console.log('Successfully saved!');
							initLoading(response.token);
						},
						error: function(model, error) {
							console.log(model);
							console.log(error);
							if (error.status === 400) {
								$("#subscribe_form").find('input[name=' + error.responseJSON.field + '], select[name=' + error.responseJSON.field + ']')
							    	.parent()
							    	.addClass('has-error')
							    	.removeClass('has-success')
							    	.prev().html(error.responseJSON.errorMsg);
							}
						}
					});
				}

				return false;
			});

			//
			$('footer .subscribe').on('click', function() {
				// Get list of all currencies
				$('#login').hide();
				$('#about').hide();
				$('.hide_if_about').show();

				currencies.fetch({
					success: function() {

						var options = $("#subscribe_form select[name=currency]").html('');
						options.append($("<option selected disabled />").val('').text('Devise du compte'));
						$.each(currencies.toJSON(), function() {
						    options.append($("<option />").val(this.id).text(this.name));
						});

						$('#subscription_form').show();
					}
				});

				return false;
			});

			$('footer .about').on('click', function() {
				$('#about').show();
				$('.hide_if_about').hide();
				return false;
			});

			// Subscibe form
			$('#subscription_form input.back').on('click', function() {
				$('#subscription_form').hide();
				$('#login').show();
				return false;
			});

			// About
			$('#about a.back').on('click', function() {
				$('#about').hide();
				$('.hide_if_about').show();
				return false;
			});
		}
	});

	return LoginView;

});
