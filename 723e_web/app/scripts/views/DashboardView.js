define([
    'jquery',
    'underscore',
    'backbone',
    'mustache',
    'initView',
    'text!templates/dashboard.mustache',
    'moment'
], function($, _, Backbone, Mustache, InitView, dashboardTemplate, moment) {

    var DashboardView = Backbone.View.extend({
        el: $("#content"),

        render: function() {
            var initView = new InitView();
            if (initView.isLoaded() === false) {
                initView.render();
            }

            initView.changeSelectedItem("nav_dashboard");

            var date = new Date();
            var link = "/#/transactions/" + date.getFullYear() + "/" +
                moment().month(date.getUTCMonth()).format("MM");

            var template = Mustache.render(dashboardTemplate, {
                'link_current_month': link
            });
            $("#content").html(template);

        }
    });

    return DashboardView;

});
