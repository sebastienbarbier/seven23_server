define(["jquery", "backbone", "ws"], function($, Backbone, WebServices) {

	var debitscredits = Backbone.Model.extend({
		urlRoot: WebServices.v1.debitscredits,
		defaults: {

		},
		initialize: function() {
			//alert("Welcome to this world");
		}
	});

	return debitscredits;
});
