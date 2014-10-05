define([
		"jquery",
		"backbone",
		"ws",
		"mustache",
		"text!templates/transactions/timeline/debitsCreditsTemplate.mustache"
	],
	function(
		$,
		Backbone,
		WebServices,
		Mustache,
		debitsCreditsTemplate) {

		var debitscredits = Backbone.Model.extend({
			urlRoot: WebServices.v1.debitscredits,
			defaults: {

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
