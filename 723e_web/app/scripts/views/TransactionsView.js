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
	'categoryCollection',
	'text!templates/transactions/dateSelectPage.mustache'
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
	CategoryCollection,
	DateSelectorPageTemplate) {

	var collection = new DebitsCreditsCollection();
	var changesCollection = new ChangesCollection();
	var currencies = new CurrenciesCollection();
	var categories = new CategoryCollection();

	var arrayAbstract = [];
	var nbSource = 0;

	var DashboardView = Backbone.View.extend({
		el: $("#content"),

		render: function(year, month) {

			var initView = new InitView();
			if (initView.isLoaded() === false) {
				initView.render();
			}

			initView.changeSelectedItem("nav_transactions");



			if (year === undefined || year === null) {
				$("#content").html(DateSelectorPageTemplate);
			} else {

				var d = moment(year + "-" + month, "YYYY-MM").format("MMMM YYYY");

				var template = Mustache.render(TransactionsTemplate, {
					date: d
				});
				$("#content").html(template);

				var view = this;


				// BIND EVENT
				$("#content button.addDebitCredit").on('click', function() {
					view.renderDebitsCreditsForm(year, month);
				});

				$("#content button.addChange").on('click', function() {
					view.renderChangesForm(year, month);
				});

				arrayAbstract = [];
				nbSource = 0;

				currencies.fetch();

				categories.fetch();

				collection.fetch({
					success: function() {
						nbSource++;
						if (nbSource === 2) {
							view.generateListe(year, month);
						}
					}
				});

				changesCollection.fetch({
					success: function() {
						nbSource++;
						if (nbSource === 2) {
							view.generateListe(year, month);
						}
					}
				});
			}

		},

		renderDebitsCreditsForm: function(year, month, debitcredit) {

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
				view.render(year, month);
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
						view.render(year, month);
					},
					error: function(model, error) {
						console.log(model.toJSON());
						console.log('error.responseText');
					}
				});

			});

		},

		renderChangesForm: function(year, month, change) {


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
				view.render(year, month);
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
						view.render(year, month);
					},
					error: function(model, error) {
						console.log(model.toJSON());
						console.log('error.responseText');
					}
				});

			});

		},
		generateListe: function(year, month) {
			// Generate array of all models
			arrayAbstract = _.union(collection.toArray(), changesCollection.toArray());

			// Date filter stuff
			if (year !== undefined && year !== null) {
				var dateStart;

				if (month !== undefined && month !== null) {
					dateStart = year + "-" + month;
				} else {
					dateStart = "" + year;
				}

				arrayAbstract = _.filter(arrayAbstract, function(c) {
					return c.get('date').indexOf(dateStart) === 0; //
				});
			}

			// Feed each element with category object
			for (i = 0; i < arrayAbstract.length; i++) {
				var c = categories.get(arrayAbstract[i].get('category_id'))
				if (c !== undefined) {
					arrayAbstract[i].set('categoryJSON', c.toJSON());
				}
			}

			// Group by date, return JSON
			arrayAbstract = _.groupBy(arrayAbstract, function(obj) {
				return obj.get("date");
			});

			// Transofrm JSON to Array
			arrayAbstract = _.pairs(arrayAbstract);

			// Order by date
			arrayAbstract = _.sortBy(arrayAbstract, function(obj) {
				return obj[0]
			});
			// Reverse
			arrayAbstract.reverse();
			// Change date format
			for (i = 0; i < arrayAbstract.length; i++) {
				arrayAbstract[i][0] = moment(arrayAbstract[i][0], "YYYY-MM-DD").format("dddd D MMMM YYYY");
			}

			var template = Mustache.render(listTemplate, {
				liste: arrayAbstract
			});

			$("#debitscredits").html(template);

			var view = this;

			$(".actions").on('click', function() {
				var action = $(this);
				if (action.hasClass('open')) {
					action.removeClass('open');
					action.prev().animate({
						"marginRight": 20
					});
					action.animate({
						"width": 20
					});
				} else {
					action.addClass("open");
					action.prev().animate({
						"marginRight": 180
					});
					action.animate({
						"width": 180
					});
				}
			});

			// Event create form on button click
			$(".element .edit").on('click', function() {
				var transaction = $(this).parents(".actions").prev();
				if (transaction.hasClass('debitcredit')) {
					var debitcredit = transaction.data('id');
					view.renderDebitsCreditsForm(year, month, collection.get(debitcredit).toJSON());
				} else if (transaction.hasClass('change')) {
					var change = transaction.data('id');
					view.renderChangesForm(year, month, changesCollection.get(change).toJSON());
				}
			});

			$(".element .delete").on('click', function() {
				var transaction = $(this).parents(".actions").prev();
				if (transaction.hasClass('debitcredit')) {
					var debitcredit = $(this).prev().data('id');
					collection.get(debitcredit).destroy({
						// prints nothing!!!
						success: function() {
							view.render(year, month);
						},
						error: function() {
							view.render(year, month);
						}
					});
				} else if (transaction.hasClass('change')) {
					var change = $(this).parents(".change").data('id');
					changesCollection.get(change).destroy({
						// prints nothing!!!
						success: function() {
							view.render(year, month);
						},
						error: function() {
							view.render(year, month);
						}
					});
				}


			});

		}


	});

	return DashboardView;

});
