define(["jquery", "backbone", "ws"], function($, Backbone, WebServices) {

	var currencies = Backbone.Model.extend({
		urlRoot: WebServices.v1.currencies,
		defaults: {

		},
		initialize: function() {
			//alert("Welcome to this world");
		},
		toString: function(amount){
			if(amount === undefined || amount === null){
				return "???";
			}

			var space = "";
			if(this.get('space')){
				space = " ";
			}

			if(this.get('after_amount')){
				return amount.toFixed(2) + space + this.get('sign');
			} else {
				return this.get('sign') + space + amount.toFixed(2);
			}
		}
	});

	return currencies;
});
