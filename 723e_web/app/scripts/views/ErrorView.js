define([
	'jquery',
	'underscore',
	'backbone',
	'mustache',
	'text!templates/error.mustache'
], function($, _, Backbone, Mustache, initTemplate) {

	var InitView = Backbone.View.extend({
		el: $("#page"),

		render: function() {
			var template = Mustache.render(initTemplate, {});
			this.$el.html(template);
		}
	});

	return InitView;

});
