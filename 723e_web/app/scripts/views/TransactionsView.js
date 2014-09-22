define([
	'jquery',
	'underscore',
	'backbone',
	'mustache',
	'initView',
	'text!templates/transactions.mustache',
	'text!templates/transactions/transactionsList.mustache',
	'debitsCreditsModel',
	'debitsCreditsCollection'
], function(
	$,
	_,
	Backbone,
	Mustache,
	InitView,
	TransactionsTemplate,
	TransactionsListTemplate,
	DebitsCreditsModel,
	DebitsCreditsCollection) {

	var collection = new DebitsCreditsCollection();

	var DashboardView = Backbone.View.extend({
		el: $("#content"),

		render: function() {
			var initView = new InitView();
			if (initView.isLoaded() === false) {
				initView.render();
			}

			initView.changeSelectedItem("nav_transactions");
			var template = Mustache.render(TransactionsTemplate, {});
			$("#content").html(template);

			collection.fetch({
				success: function() {
					console.log(collection.toJSON());
					var template = Mustache.render(TransactionsListTemplate, {
						'debitscredits': collection.toJSON()
					});
					$("#content").html(template);
				}
			});

		}
	});

	return DashboardView;

});
