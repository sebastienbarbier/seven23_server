define([
	'jquery',
	'underscore',
	'backbone',
	'mustache',
	'ws',
	'text!templates/dashboard.mustache'
], function($, _, Backbone, Mustache, Ws, dashboardTemplate) {

	var DashboardView = Backbone.View.extend({
		el: $("#page"),

		render: function() {

			var template = Mustache.render(dashboardTemplate, {});
			this.$el.html(template);

		}
	});

	return DashboardView;

});
