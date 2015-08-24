define([
	'jquery',
	'underscore',
	'backbone',
	'mustache',
	'initView',
	'text!templates/settings.mustache',
	'text!templates/user/deleteUser.mustache',
	'storage'
], function($, _, Backbone, Mustache, InitView, settingsTemplate, deleteTemplate, storage) {

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
				user.accounts[i].currency_json = storage.currencies.get(user.accounts[i].currency).toJSON();
			}

			// Generate and push template.
			var template = Mustache.render(settingsTemplate, {
				'user': user
			});
			$("#content").html(template);

			// When properly closing modal, we delete user.
			$("button.deleteUserButton").on("click", function() {
				$('#deleteModal').one('hidden.bs.modal', function(e) {
			        deleteUser('user');
			    }).modal('hide');
			});
		}
	});

	function deleteUser () {
		storage.user.destroy({success: function(model, response) {
			// Generate and push template.
			sessionStorage.removeItem("key");
			var template = Mustache.render(deleteTemplate);
			$("#page").html(template);
		}});
	}

	return SettingsView;

});
