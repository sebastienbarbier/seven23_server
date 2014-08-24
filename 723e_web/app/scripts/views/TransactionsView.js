define([
	'jquery',
	'underscore',
	'backbone',
	'mustache',
	'initView',
	'text!templates/transactions.mustache'
], function($, _, Backbone, Mustache, InitView, transactionsTemplate) {

	var DashboardView = Backbone.View.extend({
		el: $("#content"),

		render: function() {
			var initView = new InitView();
			if (initView.isLoaded() === false) {
				initView.render();
			}

			initView.changeSelectedItem("nav_transactions");
			var template = Mustache.render(transactionsTemplate, {});
			$("#content").html(template);

		}
	});

	return DashboardView;

});
