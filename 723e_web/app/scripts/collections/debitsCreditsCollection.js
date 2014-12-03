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
        convert: function(){
        	var favoriteCurrency = storage.user.currency();
        	var change;
        	// For each transactions in this collection
        	for(var i = 0; i < this.models.length; i = i + 1){
        		var debitcredit = this.models[i];
        		// If current currency is different from favorite currency
        		if(debitcredit.get('currency_id') !== favoriteCurrency){
        			change = storage.changes.filter(function(c){
        				return (c.get('new_currency') === debitcredit.get('currency_id'))
        						&& (c.get('date') <= debitcredit.get('date'));
        			});

        			// Si aucun change ne correspond.
        			if(change === undefined || change === null || change.length === 0){
        				debitcredit.set('new_amount', null);
        			} else {

	        			// Ratio à appliquer.
	        			var ratio = 1;

	        			if(change[change.length-1]){
	        				ratio = change[change.length-1].get('exchange_rate')
	        			}

        				debitcredit.set('new_amount', debitcredit.get('amount') / ratio);
        			}

        			console.log(change);
        		}
        		console.log(debitcredit);
        	}
        }
	});

	return debitscredits;
});
