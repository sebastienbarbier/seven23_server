define([
	'jquery',
	'underscore',
	'backbone',
	'mustache',
	'initView',
	'text!templates/categories.mustache'
], function($, _, Backbone, Mustache, InitView, CaegoriesTemplate) {

	var DashboardView = Backbone.View.extend({
		el: $("#content"),

		render: function() {
			var initView = new InitView();
			if (initView.isLoaded() === false) {
				initView.render();
			}

			initView.changeSelectedItem("nav_categories");
			var template = Mustache.render(CaegoriesTemplate, {});
			$("#content").html(template);

		}
	});

	return DashboardView;

});
