define(["jquery",
		"backbone",
		"underscore",
		"ws",
		"debitsCreditsModel",
		"storage"],
	function(
		$,
		Backbone,
		_,
		WebServices,
		DebitsCreditsModel,
		storage) {

	function recursiveCurrency(ratio){
		return null
	}

	var debitscredits = Backbone.Collection.extend({
		model: DebitsCreditsModel,
		url: WebServices.v1.debitscredits,
		comparator: 'date',
	});

	return debitscredits;
});
