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


			if (month === undefined || month === null) {

				var calendar = {};
				if (year === undefined || year === null) {
					calendar.year = new Date().getFullYear();
				} else {
					calendar.year = moment().year(year).year();
				}
				calendar.before = calendar.year - 1;
				calendar.after = calendar.year + 1;
				calendar.months = [];
				for (var i = 1; i <= 12; i = i + 1) {
					calendar.months.push({
						month: moment().month(i - 1).format("MM"),
						year: year,
						label: moment().month(i - 1).format("MMMM")
					});
				}

				var template = Mustache.render(DateSelectorPageTemplate, {
					calendar: calendar
				});
				$("#content").html(template);
			} else {

				var d = moment(year + "-" + month, "YYYY-MM").format("MMMM YYYY");

				var template = Mustache.render(TransactionsTemplate, {
					date: d,
					year: year
				});
				$("#content").html(template);

				var view = this;


				// BIND EVENT
				$("#content button.addDebitCredit").on('click', function() {
					//transactionsFormView.render(year, month);
					Backbone.history.navigate("#/transactions/"+year+"/"+month+"/debitscredits/add", {
						trigger: true
					});
				});

				$("#content button.addChange").on('click', function() {
					//changesFormView.render(year, month);
					Backbone.history.navigate("#/transactions/"+year+"/"+month+"/changes/add", {
						trigger: true
					});
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
					Backbone.history.navigate("#/transactions/"+year+"/"+month+"/debitscredits/edit/"+debitcredit, {
						trigger: true
					});
				} else if (transaction.hasClass('change')) {
					var change = transaction.data('id');
					Backbone.history.navigate("#/transactions/"+year+"/"+month+"/changes/edit/"+change, {
						trigger: true
					});
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
