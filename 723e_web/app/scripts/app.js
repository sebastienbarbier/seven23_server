define("app", [
			"jquery",
			"bootstrap",
			"moment",
			"fittext",
			"router",
			"ws",
			"userModel",
			"storage",
			"validator"],
		function(
			$,
			bt,
			moment,
			fittext,
			Router,
			ws,
			UserModel,
			storage) {
	// Put here the plugin code.
	// No need to return anything as we are augmenting the jQuery object
	var initialize = function() {

		// Initialise french moment interface
		var fr = require(['../../bower_components/moment/locale/fr']);
		moment.locale('fr');

		// First we check if user is logged to charge the correct page.
		ws.get({
			url: ws.init,
			async: false
		}).done(function(json) {
			if (json.is_authenticated === false) {
				// User is invited to login
				// GET[’next'] is the page to load
				var hash = window.location.hash
				if (hash == undefined) {
					hash = "/transactions";
				} else {
					hash = window.location.hash.split("?")[0];
					if (hash == "#/login") {
						hash = "/transactions";
					}
				}
				window.location.hash = "/login?next=" + hash;
				Router.initialize();
			}else{
				storage.init(json.id, function(){
					$('body').addClass('app');
					Router.initialize();
				});
			}
		}).fail(function() {
			window.location.hash = "/error";
			Router.initialize();
		});

	};

	return {
		initialize: initialize
	};

});
