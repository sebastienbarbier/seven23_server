define([
	"jquery",
	"backbone",
	"ws",
	"mustache",
	"text!templates/transactions/timeline/changesTemplate.mustache"
], function(
	$,
	Backbone,
	WebServices,
	Mustache,
	changeTemplate) {

	var changes = Backbone.Model.extend({
		urlRoot: WebServices.v1.changes,
		defaults: {

		},
		initialize: function() {
			//alert("Welcome to this world");
		},
		html: {
			list: function() {
				return Mustache.render(changeTemplate, {
					change: this.toJSON()
				});
			}
		}
	});

	return changes;
});
