define([
	'jquery',
	'underscore',
	'backbone',
	'mustache',
	'moment',
	'initView',
	'text!templates/transactions.mustache',
	'text!templates/transactions/debitscreditsForm.mustache',
	'debitsCreditsModel',
	'debitsCreditsCollection',
	'text!templates/transactions/changesForm.mustache',
	'changesModel',
	'changesCollection',
	'currenciesCollection',
	'text!templates/transactions/list.mustache',
	'categoryCollection'
], function(
	$,
	_,
	Backbone,
	Mustache,
	moment,
	InitView,
	TransactionsTemplate,
	DebitsCreditsFormTemplate,
	DebitsCreditsModel,
	DebitsCreditsCollection,
	ChangesFormTemplate,
	ChangesModel,
	ChangesCollection,
	CurrenciesCollection,
	listTemplate,
	CategoryCollection) {

	var collection = new DebitsCreditsCollection();
	var changesCollection = new ChangesCollection();
	var currencies = new CurrenciesCollection();
	var categories = new CategoryCollection();

	var arrayAbstract = [];
	var nbSource = 0;

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

			// BIND EVENT
			$("#content button.addDebitCredit").on('click', function() {
				view.renderDebitsCreditsForm();
			});

			$("#content button.addChange").on('click', function() {
				view.renderChangesForm();
			});

			arrayAbstract = [];
			nbSource = 0;

			currencies.fetch();

			categories.fetch();

			collection.fetch({
				success: function() {
					nbSource++;
					if (nbSource === 2) {
						view.generateListe();
					}
				}
			});

			changesCollection.fetch({
				success: function() {
					nbSource++;
					if (nbSource === 2) {
						view.generateListe();
					}
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

		},
		generateListe: function() {
			// Generate array of all models
			arrayAbstract = _.union(collection.toArray(), changesCollection.toArray());

			console.log(arrayAbstract);
			// Group by date, return JSON
			arrayAbstract = _.groupBy(arrayAbstract, function(obj) {
				return obj.get("date");
			});

			console.log(arrayAbstract);
			// Transofrm JSON to Array
			arrayAbstract = _.pairs(arrayAbstract);

			console.log(arrayAbstract);
			// Order by date
			arrayAbstract = _.sortBy(arrayAbstract, function(obj) {
				return obj[0]
			});
			// Change date format
			console.log(arrayAbstract);
			for (i = 0; i < arrayAbstract.length; i++) {
				arrayAbstract[i][0] = moment(arrayAbstract[i][0], "YYYY-MM-DD").format("dddd D MMMM YYYY");
			}


			var template = Mustache.render(listTemplate, {
				liste: arrayAbstract
			});

			$("#listes").html(template);

			var view = this;

			// Event create form on button click
			$(".debitscredits button.edit").on('click', function() {
				var debitcredit = $(this).parents(".debitscredits").data('id');
				view.renderDebitsCreditsForm(collection.get(debitcredit).toJSON());
			});

			$(".debitscredits button.delete").on('click', function() {
				var debitcredit = $(this).parents(".debitscredits").data('id');
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

			$(".changes button.edit").on('click', function() {
				var change = $(this).parents(".changes").data('id');
				view.renderChangesForm(changesCollection.get(change).toJSON());
			});

			$(".changes button.delete").on('click', function() {
				var change = $(this).parents(".changes").data('id');
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

	return DashboardView;

});
