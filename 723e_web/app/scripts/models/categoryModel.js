define(["jquery", "backbone", "ws"], function($, Backbone, WebServices) {

	var category = Backbone.Model.extend({
		urlRoot: WebServices.v1.categories,
		defaults: {
			name: 'Nom',
			description: 'Description',
			color: '#ffffff',
			icon: 'fa-circle'
		},
		initialize: function() {
			//alert("Welcome to this world");
		},
		validate: function(attrs, options) {
			if (attrs.description === "") {
				return "NAAAANNNNN";
			}
			if (attrs.name === "") {
				return "BISSS";
			}
		}
	});

	return category;
});
