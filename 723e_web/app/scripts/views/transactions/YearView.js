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

		render: function(year) {

			var initView = new InitView();
			if (initView.isLoaded() === false) {
				initView.render();
			}

			initView.changeSelectedItem("nav_transactions");

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


		}

	});

	return DashboardView;

});
