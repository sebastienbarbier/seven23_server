define(["jquery", "backbone", "ws", "categoryModel"], function($, Backbone, WebServices, CategoryModel) {

	var collection = Backbone.Collection.extend({
		model: CategoryModel,
		url: WebServices.v1.categories,
		comparator: 'name'
	});


	return collection;
});
