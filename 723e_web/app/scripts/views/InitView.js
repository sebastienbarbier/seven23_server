define([
	'jquery',
	'underscore',
	'backbone',
	'mustache',
	'text!templates/init.mustache'
], function($, _, Backbone, Mustache, initTemplate) {

	var InitView = Backbone.View.extend({
		el: $("#page"),

		render: function() {
			var template = Mustache.render(initTemplate, {});
			this.$el.html(template);
		},

		isLoaded: function() {
			return $("#navbar").is(':visible');
		},

		changeSelectedItem: function(item) {
			$("#navbar .selected").removeClass('selected');
			$("#navbar ." + item).addClass('selected');
		}
	});

	return InitView;

});
