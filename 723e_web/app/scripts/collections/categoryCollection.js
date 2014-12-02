define(["jquery", "backbone", "ws", "categoryModel"], function($, Backbone, WebServices, CategoryModel) {

	var collection = Backbone.Collection.extend({
		model: CategoryModel,
		url: WebServices.v1.categories,
		comparator: 'name',

		// Filter down the list of all photos that have been viewed
		enable: function() {
			return this.filter(function(debitcredit){ return debitcredit.get('active'); });
		},
		// Filter down the list to only photos that have not yet been viewed
		disable: function() {
			return this.without.apply(this, this.enable());
		}
	});


	return collection;
});
