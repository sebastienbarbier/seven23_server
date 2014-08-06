define("userModel", ["jquery", "backbone"], function($, Backbone) {

	var user = Backbone.Model.extend({
		initialize: function() {
			//alert("Welcome to this world");
		}
	});

	return user;
});
