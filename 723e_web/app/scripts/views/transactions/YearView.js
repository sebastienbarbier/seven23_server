define([
    'jquery',
    'underscore',
    'backbone',
    'mustache',
    'moment',
    'initView',
    'ws',
    'storage',
    'text!templates/transactions/dateSelectPage.mustache'
], function(
    $,
    _,
    Backbone,
    Mustache,
    moment,
    InitView,
    ws,
    storage,
    DateSelectorPageTemplate) {


    var arrayAbstract = [];
    var nbSource = 0;

    var DashboardView = Backbone.View.extend({
        el: $("#content"),

        render: function(year) {

            var initView = new InitView();
            if (initView.isLoaded() === false) {
                initView.render();
            }

            initView.changeSelectedItem("nav_transactions");

            var calendar = {};
            if (year === undefined || year === null) {
                calendar.year = new Date().getFullYear();
            } else {
                calendar.year = moment().year(year).year();
            }
            calendar.before = calendar.year - 1;
            calendar.after = calendar.year + 1;
            calendar.months = [];

            ws.get({
                "url": ws.v1.resume_year,
                "data": {
                    year: calendar.year
                },
                success: function(json) {

                    for (var i = 1; i <= 12; i = i + 1) {
                        calendar.months.push({
							month   : moment().month(i - 1).format("MM"),
                            year    : year,
                            label   : moment().month(i - 1).format("MMMM"),
                            exist   : (json.months[i] ? true : false),
                            count   : (json.months[i] ? json.months[i].count : 0),
                            sum     : storage.currencies.get(storage.user.currency()).toString((json.months[i] ? json.months[i].sum : 0)),
                            credits : storage.currencies.get(storage.user.currency()).toString((json.months[i] ? json.months[i].sum_credits : 0)),
                            debits  : storage.currencies.get(storage.user.currency()).toString((json.months[i] ? json.months[i].sum_debits : 0))
                        });
                    }

                    var template = Mustache.render(DateSelectorPageTemplate, {
                        calendar: calendar
                    });
                    $("#content").html(template);
                }
            });
        }
    });

    return DashboardView;

});
