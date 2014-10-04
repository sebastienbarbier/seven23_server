define(["jquery", "backbone", "ws"], function($, Backbone, WebServices) {

	var changes = Backbone.Model.extend({
		urlRoot: WebServices.v1.changes,
		defaults: {

		},
		initialize: function() {
			//alert("Welcome to this world");
		},
		html: {
			list: function() {
				return "Changes : " + this.get("name");
			}
		}
	});

	return changes;
});
