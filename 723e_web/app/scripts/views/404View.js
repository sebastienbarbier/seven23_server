define([
    'jquery',
    'underscore',
    'backbone',
    'mustache',
    'initView',
    'text!templates/404.mustache'
], function($, _, Backbone, Mustache, InitView, settingsTemplate) {

    var SettingsView = Backbone.View.extend({
        el: $("#content"),

        render: function() {
            var initView = new InitView();
            if (initView.isLoaded() === false) {
                initView.render();
            }

            initView.changeSelectedItem("nav_settings");
            var template = Mustache.render(settingsTemplate, {});
            $("#content").html(template);

        }
    });

    return SettingsView;

});
