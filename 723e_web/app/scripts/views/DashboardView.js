define([
	'jquery',
	'underscore',
	'backbone',
	'mustache',
	'initView',
	'text!templates/dashboard.mustache'
], function($, _, Backbone, Mustache, InitView, dashboardTemplate) {

	var DashboardView = Backbone.View.extend({
		el: $("#content"),

		render: function() {
			var initView = new InitView();
			if (initView.isLoaded() === false) {
				initView.render();
			}

			initView.changeSelectedItem("nav_dashboard");
			var template = Mustache.render(dashboardTemplate, {});
			$("#content").html(template);

		}
	});

	return DashboardView;

});