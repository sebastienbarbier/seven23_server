define([
	'jquery',
	'underscore',
	'backbone',
	'mustache',
	'initView',
	'text!templates/transactions/transactionsList.mustache',
	'text!templates/transactions/debitscreditsForm.mustache',
	'debitsCreditsModel',
	'debitsCreditsCollection',
	'currenciesCollection',
	'categoryCollection'
], function(
	$,
	_,
	Backbone,
	Mustache,
	InitView,
	TransactionsListTemplate,
	DebitsCreditsFormTemplate,
	DebitsCreditsModel,
	DebitsCreditsCollection,
	CurrenciesCollection,
	CategoryCollection) {

	var collection = new DebitsCreditsCollection();
	var currencies = new CurrenciesCollection();
	var categories = new CategoryCollection();

	var DashboardView = Backbone.View.extend({
		el: $("#content"),

		render: function() {
			var initView = new InitView();
			if (initView.isLoaded() === false) {
				initView.render();
			}

			initView.changeSelectedItem("nav_transactions");


			var view = this;

			currencies.fetch();

			categories.fetch();

			collection.fetch({
				success: function() {
					console.log(collection.toJSON());
					var template = Mustache.render(TransactionsListTemplate, {
						'debitscredits': collection.toJSON()
					});
					$("#content").html(template);

					$("#content button.addDebitCredit").on('click', function() {
						view.renderDebitsCreditsForm();
					});
				}
			});

		},

		renderDebitsCreditsForm: function() {

			console.log(currencies.toJSON());

			var template = Mustache.render(DebitsCreditsFormTemplate, {
				currencies: currencies.toJSON(),
				categories: categories.toJSON()
			});
			$("#content").html(template);

			var view = this;
			// User cancel form. We go back to view page.
			$("button.debitscredits_form_cancel").on("click", function() {
				view.render();
			});

			$("button.debitscredits_form_submit").on("click", function() {

				var array = $("#debitcredit_form").serializeArray();
				var dict = {};

				for (var i = 0; i < array.length; i++) {
					dict[array[i]['name']] = array[i]['value']
				}
				dict['user'] = "http://localhost:8000/api/v1/users/1";

				var debitcredit = new DebitsCreditsModel(dict);

				debitcredit.save(dict, {
					wait: true,
					success: function(model, response) {
						console.log('Successfully saved!');
						view.render();
					},
					error: function(model, error) {
						console.log(model.toJSON());
						console.log('error.responseText');
					}
				});

			});

		}


	});

	return DashboardView;

});
