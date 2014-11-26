define(["jquery", "backbone", "ws", "debitsCreditsModel"], function($, Backbone, WebServices, DebitsCreditsModel) {

	var debitscredits = Backbone.Collection.extend({
		model: DebitsCreditsModel,
		url: WebServices.v1.debitscredits,
		comparator: 'date'
	});

	return debitscredits;
});
