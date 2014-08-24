define([
	'jquery',
	'underscore',
	'backbone',
	'mustache',
	'initView',
	'text!templates/categories/categories.mustache',
	'text!templates/categories/categoriesForm.mustache'
], function($, _, Backbone, Mustache, InitView, CategoriesTemplate, CategoriesForm) {

	var DashboardView = Backbone.View.extend({
		el: $("#content"),

		render: function() {
			var initView = new InitView();
			if (initView.isLoaded() === false) {
				initView.render();
			}

			initView.changeSelectedItem("nav_categories");
			var template = Mustache.render(CategoriesTemplate, {});
			$("#content").html(template);

			var view = this;
			// Event create form on button click
			$("#content button.addCategorie").on('click', function() {
				view.renderForm();
			});
		},

		renderForm: function(categorie) {
			var template = Mustache.render(CategoriesForm, {});
			$("#content").html(template);

			var view = this;
			$("button.cat_form_cancel").on("click", function() {
				view.render();
			});
		}
	});

	return DashboardView;

});
