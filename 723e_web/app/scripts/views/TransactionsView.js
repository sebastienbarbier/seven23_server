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

					var template = Mustache.render(TransactionsListTemplate, {
						'debitscredits': collection.toJSON()
					});
					$("#content").html(template);

					$("#content button.addDebitCredit").on('click', function() {
						view.renderDebitsCreditsForm();
					});

					// Event create form on button click
					$("#debitscredits_list button.edit").on('click', function() {
						var debitcredit = $(this).parents(".debitcredit").data('id');
						view.renderDebitsCreditsForm(collection.get(debitcredit).toJSON());
					});

					$("#debitscredits_list button.delete").on('click', function() {
						var debitcredit = $(this).parents(".debitcredit").data('id');
						collection.get(debitcredit).destroy({
							// prints nothing!!!
							success: function() {
								view.render();
							},
							error: function() {
								view.render();
							}
						});

					});
				}
			});

		},

		renderDebitsCreditsForm: function(debitcredit) {

			console.log(currencies.toJSON());

			var template = Mustache.render(DebitsCreditsFormTemplate, {
				debitcredit: debitcredit,
				currencies: currencies.toJSON(),
				categories: categories.toJSON()
			});
			$("#content").html(template);

			// Put select markup as selected
			if (debitcredit) {
				$("#debitcredit_form select[name='currency']").find('option[value="' + debitcredit.currency + '"]').attr('selected', true);
				$("#debitcredit_form select[name='category']").find('option[value="' + debitcredit.category + '"]').attr('selected', true);
			}

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
