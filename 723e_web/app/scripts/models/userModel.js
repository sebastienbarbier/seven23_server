define(["jquery", "backbone", "ws"], function($, Backbone, WebServices) {

	var user = Backbone.Model.extend({
		urlRoot: WebServices.v1.users,
		initialize: function() {
			//alert("Welcome to this world");
		}
	});

	return user;
});
