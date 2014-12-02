define([
		"jquery",
		"backbone",
		"ws",
		"mustache",
		"text!templates/transactions/timeline/debitsCreditsTemplate.mustache",
		"storage"
	],
	function(
		$,
		Backbone,
		WebServices,
		Mustache,
		debitsCreditsTemplate,
		storage) {

		var debitscredits = Backbone.Model.extend({
			urlRoot: WebServices.v1.debitscredits,
			defaults: {
				isCredit: function(){
					return this.get('amount') >= 0;
				},
				isDebit: function(){
					return this.get('amount') < 0;
				},
				isFavoriteCurrency: function(){
					return true;
				},
				defaultCurrency: function(){
					console.log(this.debitsCredits.currency_id);
					return storage.currencies.get(this.debitsCredits.currency_id).toString(this.debitsCredits.amount);
				},
				favoriteCurrency: function(){

				}
			},
			initialize: function() {
				//alert("Welcome to this world");
			},
			html: {
				list: function() {
					return Mustache.render(debitsCreditsTemplate, {
						debitsCredits: this.toJSON()
					});
				}
			}
		});

		return debitscredits;
	});
