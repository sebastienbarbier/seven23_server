define("app", ["jquery", "router", "ws", "userModel"], function($, Router, ws, UserModel) {
	// Put here the plugin code.
	// No need to return anything as we are augmenting the jQuery object
	var initialize = function() {

		var user = new UserModel();

		// First we check if user is logged to charge the correct page.
		ws.get({
			url: ws.init,
			async: false
		}).done(function(json) {

			console.log(json);
			if (json.is_authenticated === false) {
				// User is invited to login
				// GET[’next'] is the page to load
				var hash = window.location.hash
				if (hash == undefined) {
					hash = "/dashboard";
				} else {
					hash = window.location.hash.split("?")[0];
					if (hash == "#/login") {
						hash = "/dashboard";
					}
				}
				window.location.hash = "/login?next=" + hash;
			} else {

				// window.location.hash = "#/dashboard";
			}
		}).fail(function() {
			window.location.hash = "/error";
		});

		// Pass in our Router module and call it's initialize function
		Router.initialize();
	};

	return {
		initialize: initialize
	};

});
