define("storage",
	   ["jquery",
		"categoryCollection",
		"currenciesCollection",
		"userModel"],
	function(
		$,
		CategoriesCollection,
		CurrenciesCollection,
		UserModel) {

	// Properties
	var user;
	var categories = new CategoriesCollection();
	var currencies = new CurrenciesCollection();

	// This function intialise storage object.
	var init = function(userid, callback){

		// Number of collection to fetch asynchronously
		var fetchNb = 3;
		// Number of collection already fetched
		var fetchCounter = 0;

		// Get User model
		user = new UserModel({id: userid});
		user.fetch({
	        success: function (user) {
	        	fetchCounter++;
	        	if(fetchCounter === fetchNb){
	        		callback();
	        	}
	        }
	    });

		// Get list of all categories
		categories.fetch({
			success: function() {
	        	fetchCounter++;
	        	if(fetchCounter === fetchNb){
	        		callback();
	        	}
			}
		});

		// Get list of all currencies
		currencies.fetch({
			success: function() {
	        	fetchCounter++;
	        	if(fetchCounter === fetchNb){
	        		callback();
	        	}
			}
		});


	};

	return {
		init       : init,
		user       : user,
		categories : categories,
		currencies : currencies
	}
});
