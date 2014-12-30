define([
	'jquery',
	'underscore',
	'backbone',
	'mustache',
	'initView',
	'text!templates/settings.mustache',
	'storage'
], function($, _, Backbone, Mustache, InitView, settingsTemplate, storage) {

	var SettingsView = Backbone.View.extend({
		el: $("#content"),

		render: function() {
			var initView = new InitView();
			if (initView.isLoaded() === false) {
				initView.render();
			}

			initView.changeSelectedItem("nav_settings");

			var user = storage.user.toJSON();

			for(var i = 0; i < user.accounts.length; i=i+1){
				user.accounts[i].currency_json = storage.currencies.get(user.accounts[i].currency).toJSON()
			}

			// Generate and push template.
			var template = Mustache.render(settingsTemplate, {
				'user': user
			});
			$("#content").html(template);

		}
	});

	return SettingsView;

});
