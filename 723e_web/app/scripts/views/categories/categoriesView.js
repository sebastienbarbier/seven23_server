define([
		'jquery',
		'underscore',
		'backbone',
		'mustache',
		'initView',
		'text!templates/categories/categories.mustache',
		'text!templates/categories/categoriesItem.mustache',
		'text!templates/categories/categoriesForm.mustache',
		'categoryModel',
		'categoryCollection',
		'storage'
	],
	function(
		$,
		_,
		Backbone,
		Mustache,
		InitView,
		CategoriesTemplate,
		CategoriesItemTemplate,
		CategoriesFormTemplate,
		Category,
		CategoryCollection,
		storage) {

		var DashboardView = Backbone.View.extend({
			el: $("#content"),

			getTreeHTML: function(catCollection) {
				var c = catCollection;

				function getItemHTML(cat) {
					var rootItems = c.where({
						'parent_id': cat,
						'active': true
					});

					var result = "";

					for (var i = 0, len = rootItems.length; i < len; i = i + 1) {
						result += Mustache.render(CategoriesItemTemplate, {
							'categorie': rootItems[i].toJSON(),
							'tree': getItemHTML(rootItems[i].get('id')),
							'i': i%3
						});
					}

					return result;
				};

				return getItemHTML(null);
			},

			getListDisableHTML: function(catCollection) {
				var result = "";
				var collectionDisabled = catCollection;

				for (var i = 0, len = collectionDisabled.length; i < len; i = i + 1) {
					result += Mustache.render(CategoriesItemTemplate, {
						'categorie': collectionDisabled[i].toJSON()
					});
				}

				return result;
			},

			render: function() {
				var initView = new InitView();
				if (initView.isLoaded() === false) {
					initView.render();
				}

				initView.changeSelectedItem("nav_categories");

				var view = this;

				var tree_enable = view.getTreeHTML(storage.categories);
				var tree_disable = view.getListDisableHTML(storage.categories.disable());

				var template = Mustache.render(CategoriesTemplate, {
					'tree_enable': tree_enable,
					'tree_disable': tree_disable
				});
				$("#content").html(template);


				// Event create form on button click
				$("#categories button.edit").on('click', function() {
					var cat = $(this).parents("li").data('id');

					Backbone.history.navigate("#/categories/edit/"+cat, {
						trigger: true
					});
				});

				$("#categories button.delete").on('click', function() {
					var cat = $(this).parents("li").data('id');
					storage.categories.get(cat).destroy( // prints nothing!!!
						{
							success: function() {
								view.render();
							},
							error: function() {
								view.render();
							}
						});
				});
				$("#categories_disable button.delete").on('click', function() {
					var cat = $(this).parents("li").data('id');
					storage.categories.get(cat).destroy( // prints nothing!!!
						{
							success: function() {
								view.render();
							},
							error: function() {
								view.render();
							}
						});
				});

				$("#categories_view h6").on('click', function() {
					$("#categories_disable").toggle()
				});

			}
		});

		return DashboardView;

	});
