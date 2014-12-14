define([
		'jquery',
		'underscore',
		'backbone',
		'mustache',
		'initView',
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
		CategoriesItemTemplate,
		CategoriesFormTemplate,
		Category,
		CategoryCollection,
		storage) {

		var CategoryFormView = Backbone.View.extend({
			el: $("#content"),

			displayForm: function(categorie){

				var categories_actives = storage.categories.enable();

				var template = Mustache.render(CategoriesFormTemplate, {
					'categorie': categorie,
					'categories': new CategoryCollection(categories_actives).toJSON()
				});
				$("#content").html(template);

				var defaultIcon = "fa-circle-o";
				// Put select markup as selected
				if (categorie) {
					$("#cat_form select[name='parent']").find('option[value="' + categorie.parent_id + '"]').attr('selected', true);
					defaultIcon = categorie.icon;
				}

				$('#cat_form .iconpicker').iconpicker({
					arrowClass: 'btn-primary',
					arrowPrevIconClass: 'glyphicon glyphicon-chevron-left',
					arrowNextIconClass: 'glyphicon glyphicon-chevron-right',
					cols: 5,
					icon: defaultIcon,
					iconset: 'fontawesome',
					labelHeader: '{0} of {1} pages',
					labelFooter: '{0} - {1} of {2} icons',
					placement: 'bottom',
					rows: 5,
					search: true,
					searchText: 'Search',
					selectedClass: 'btn-primary',
					unselectedClass: ''
				});

				$('#cat_form .colorpicker').colorpicker();

				// User validate form
				$("button.cat_form_submit").on("click", function() {

					var array = $("#cat_form").serializeArray();
					var dict = {};

					for (var i = 0; i < array.length; i++) {
						dict[array[i]['name']] = array[i]['value']
					}
					dict['user'] = "http://localhost:8000/api/v1/users/1";

					if (dict.parent && dict.parent !== "") {
						dict.parent = storage.categories.get(dict.parent).url();
					}

					var category = new Category(dict);

					category.save(dict, {
						wait: true,
						success: function(model, response) {
							storage.categories.fetch({
								success: function(){
									Backbone.history.navigate("#/categories", {
										trigger: true
									});
								}
							});
						},
						error: function(model, error) {
							console.log(model.toJSON());
							console.log('error.responseText');
						}
					});

				});
			},

			render: function(categorie_id) {
				var initView = new InitView();
				if (initView.isLoaded() === false) {
					initView.render();
				}

				initView.changeSelectedItem("nav_categories");

				var view = this;

				require(['bootstrap-iconpicker', 'bootstrap-colorpicker'], function() {

					if(categorie_id){
						var categorie = new Category({id: categorie_id});
						categorie.fetch({
					        success: function (c) {
					            view.displayForm(categorie.toJSON());
					        }
					    });
					}else{
						view.displayForm();
					}


				});
			}
		});

		return CategoryFormView;

	});
