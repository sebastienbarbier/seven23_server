define(["jquery", "backbone", "ws"], function($, Backbone, WebServices) {

	var invitation = Backbone.Model.extend({
		urlRoot: WebServices.v1.invitations,
		defaults: {
		},
		initialize: function() {
			//alert("Welcome to this world");
		}
	});

	return invitation;
});
