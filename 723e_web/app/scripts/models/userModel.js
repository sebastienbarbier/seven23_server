define(["jquery", "backbone", "ws"], function($, Backbone, WebServices) {

	var user = Backbone.Model.extend({
		urlRoot: WebServices.v1.users,
		defaults: {
		},
		initialize: function() {
			//alert("Welcome to this world");
		},
		currency: function(){
			var accounts = this.get('accounts');

			if(accounts.length === 0){
				return null;
			}

			return this.get('accounts')[0].currency;
		}
	});

	return user;
});
