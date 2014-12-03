define(["jquery", "backbone", "ws"], function($, Backbone, WebServices) {

	var currencies = Backbone.Model.extend({
		urlRoot: WebServices.v1.currencies,
		defaults: {

		},
		initialize: function() {
			//alert("Welcome to this world");
		},
		toString: function(amount){
			var space = "";
			if(this.get('space')){
				space = " ";
			}

			if(this.get('after_amount')){
				return amount + space + this.get('sign');
			} else {
				return this.get('sign') + space + amount;
			}
		}
	});

	return currencies;
});
