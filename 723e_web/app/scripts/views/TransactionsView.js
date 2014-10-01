define([
	'jquery',
	'underscore',
	'backbone',
	'mustache',
	'initView',
	'text!templates/transactions.mustache',
	'text!templates/transactions/transactionsList.mustache',
	'text!templates/transactions/debitscreditsForm.mustache',
	'debitsCreditsModel',
	'debitsCreditsCollection',
	'text!templates/transactions/changesList.mustache',
	'text!templates/transactions/changesForm.mustache',
	'changesModel',
	'changesCollection',
	'currenciesCollection',
	'categoryCollection'
], function(
	$,
	_,
	Backbone,
	Mustache,
	InitView,
	TransactionsTemplate,
	TransactionsListTemplate,
	DebitsCreditsFormTemplate,
	DebitsCreditsModel,
	DebitsCreditsCollection,
	ChangesListTemplate,
	ChangesFormTemplate,
	ChangesModel,
	ChangesCollection,
	CurrenciesCollection,
	CategoryCollection) {

	var collection = new DebitsCreditsCollection();
	var changesCollection = new ChangesCollection();
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

			$("#content").html(TransactionsTemplate);

			var view = this;

			currencies.fetch();

			categories.fetch();

			collection.fetch({
				success: function() {

					var template = Mustache.render(TransactionsListTemplate, {
						'debitscredits': collection.toJSON()
					});
					$("#transactions").html(template);

					$("#content button.addDebitCredit").on('click', function() {
						view.renderDebitsCreditsForm();
					});

					$("#content button.addChange").on('click', function() {
						view.renderChangesForm();
					});

					// Event create form on button click
					$("#transactions button.edit").on('click', function() {
						var debitcredit = $(this).parents(".debitcredit").data('id');
						view.renderDebitsCreditsForm(collection.get(debitcredit).toJSON());
					});

					$("#transactions button.delete").on('click', function() {
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

			changesCollection.fetch({
				success: function() {

					var template = Mustache.render(ChangesListTemplate, {
						'changes': changesCollection.toJSON()
					});
					$("#changes").html(template);

					$("#content button.addChange").on('click', function() {
						view.renderChangesForm();
					});

					$("#content button.addChange").on('click', function() {
						view.renderChangesForm();
					});

					// Event create form on button click
					$("#changes button.edit").on('click', function() {
						var change = $(this).parents(".change").data('id');
						view.renderChangesForm(changesCollection.get(change).toJSON());
					});

					$("#changes button.delete").on('click', function() {
						var change = $(this).parents(".change").data('id');
						changesCollection.get(change).destroy({
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

		},

		renderChangesForm: function(change) {


			var template = Mustache.render(ChangesFormTemplate, {
				change: change,
				currencies: currencies.toJSON(),
				categories: categories.toJSON()
			});
			$("#content").html(template);

			// Put select markup as selected
			if (change) {
				$("#changes_form select[name='currency']").find('option[value="' + change.currency + '"]').attr('selected', true);
				$("#changes_form select[name='new_currency']").find('option[value="' + change.new_currency + '"]').attr('selected', true);
				$("#changes_form select[name='category']").find('option[value="' + change.category + '"]').attr('selected', true);
			}

			var view = this;
			// User cancel form. We go back to view page.
			$("button.changes_form_cancel").on("click", function() {
				view.render();
			});

			$("button.changes_form_submit").on("click", function() {

				var array = $("#changes_form").serializeArray();
				var dict = {};

				for (var i = 0; i < array.length; i++) {
					dict[array[i]['name']] = array[i]['value']
				}
				dict['user'] = "http://localhost:8000/api/v1/users/1";

				var change = new ChangesModel(dict);

				change.save(dict, {
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
