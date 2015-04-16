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

			// BIND EVENT ON MENU
			$('.menu-button-smartphone a').on('click', function() {
				$("#navbar nav").toggleClass('open');
				return false;
			});
			$("#navbar li a").on('click', function () {
				if($("#navbar nav").hasClass('open')) {
					$("#navbar nav").removeClass('open')
				}
			});

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
