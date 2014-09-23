define(["jquery", "backbone", "ws", "currencyModel"], function($, Backbone, WebServices, CurrencyModel) {

	var currencies = Backbone.Collection.extend({
		model: CurrencyModel,
		url: WebServices.v1.currencies
	});

	return currencies;
});
