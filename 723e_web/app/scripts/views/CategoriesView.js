define([
		'jquery',
		'underscore',
		'backbone',
		'mustache',
		'initView',
		'text!templates/categories/categories.mustache',
		'text!templates/categories/categoriesForm.mustache',
		'categoryModel',
		'categoryCollection'
	],
	function(
		$,
		_,
		Backbone,
		Mustache,
		InitView,
		CategoriesTemplate,
		CategoriesFormTemplate,
		Category,
		CategoryCollection) {

		var collection = new CategoryCollection();

		var DashboardView = Backbone.View.extend({
			el: $("#content"),

			render: function() {
				var initView = new InitView();
				if (initView.isLoaded() === false) {
					initView.render();
				}

				initView.changeSelectedItem("nav_categories");

				var view = this;

				collection.fetch({
					success: function() {

						var template = Mustache.render(CategoriesTemplate, {
							'categories': collection.toJSON()
						});
						$("#content").html(template);


						// Event create form on button click
						$("#categories_list button.edit").on('click', function() {
							var cat = $(this).parents(".categorie").data('id');
							view.renderForm(collection.get(cat).toJSON());
						});

						$("#categories_list button.delete").on('click', function() {
							var cat = $(this).parents(".categorie").data('id');
							collection.get(cat).destroy({
								// prints nothing!!!
								success: function() {
									view.render();
								},
								error: function() {
									view.render();
								}
							});

						});

						$("#content button.addCategorie").on('click', function() {
							view.renderForm();
						});
					}
				});
			},

			renderForm: function(categorie) {
				var template = Mustache.render(CategoriesFormTemplate, {
					'categorie': categorie
				});
				$("#content").html(template);

				var view = this;
				// User validate form
				$("button.cat_form_submit").on("click", function() {

					var array = $("#cat_form").serializeArray();
					var dict = {};

					for (var i = 0; i < array.length; i++) {
						dict[array[i]['name']] = array[i]['value']
					}
					dict['user'] = "http://localhost:8000/api/v1/users/1";

					var category = new Category(dict);

					category.save(dict, {
						wait: true,
						success: function(model, response) {
							console.log('Successfully saved!');
							view.render();
						},
						error: function(model, error) {
							console.log(model.toJSON());
							console.log('error.responseText');
						}
					});

				});
				// User cancel form. We go back to view page.
				$("button.cat_form_cancel").on("click", function() {
					view.render();
				});
			}
		});

		return DashboardView;

	});
