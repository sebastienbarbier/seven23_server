define([
	'jquery',
	'underscore',
	'backbone',
	'mustache',
	'initView',
	'text!templates/transactions.mustache',
	'text!templates/transactions/debitscreditsForm.mustache',
	'debitsCreditsModel',
	'debitsCreditsCollection',
	'currenciesCollection',
	'text!templates/transactions/list.mustache',
	'categoryCollection',
	'text!templates/transactions/dateSelectPage.mustache'
], function(
	$,
	_,
	Backbone,
	Mustache,
	InitView,
	TransactionsTemplate,
	DebitsCreditsFormTemplate,
	DebitsCreditsModel,
	DebitsCreditsCollection,
	CurrenciesCollection,
	listTemplate,
	CategoryCollection,
	DateSelectorPageTemplate) {

	var currencies = new CurrenciesCollection();
	var categories = new CategoryCollection();

	var arrayAbstract = [];
	var nbSource = 0;

	var DashboardView = Backbone.View.extend({
		el: $("#content"),

		displayForm: function(year, month, debitcredit){

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
				Backbone.history.navigate("#/transactions/"+year+"/"+month, {
					trigger: true
				});
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
						Backbone.history.navigate("#/transactions/"+year+"/"+month, {
							trigger: true
						});

					},
					error: function(model, error) {
						console.log(model.toJSON());
						console.log('error.responseText');
					}
				});

			});
		},

		render: function(year, month, debitcredit_id) {

			var initView = new InitView();
			if (initView.isLoaded() === false) {
				initView.render();
			}

			initView.changeSelectedItem("nav_transactions");

			var view = this;

			currencies.fetch({
				success: function() {
					categories.fetch({
						success: function() {
							if(debitcredit_id){
								var debitcredit = new DebitsCreditsModel({id: debitcredit_id});
								debitcredit.fetch({
							        success: function (c) {
							            view.displayForm(year, month, debitcredit.toJSON());
							        }
							    });
							}else{
								view.displayForm(year, month);
							}
						}
					});
				}
			});
		}

	});

	return DashboardView;

});
