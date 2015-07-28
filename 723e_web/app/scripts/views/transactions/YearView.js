define([
    'jquery',
    'underscore',
    'backbone',
    'mustache',
    'moment',
    'initView',
    'ws',
    'storage',
    'chartjs',
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
    Chart,
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

            var currentDate = new Date();

            var calendar = {};
            if (year === undefined || year === null) {
                calendar.year = currentDate.getFullYear();
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

                    var account_currency = storage.currencies.get(storage.user.currency());
                    var i, l;
                    // Generate statistiques
                    var stats = {
                        'global' : {
                            'counter': 0,
                            'sum': 0,
                            'credits': 0,
                            'debits': 0
                        },
                        'average' : {
                            'sum': 0,
                            'credits': 0,
                            'debits': 0
                        },
                        'changes': json.stats.changes,
                        'categories': json.categories.list
                    };

                    for (i = 1; i <= 12; i = i + 1) {
                        var sum     = (json.months[i] ? json.months[i].sum : 0),
                            credits = (json.months[i] ? json.months[i].sum_credits : 0),
                            debits  = (json.months[i] ? json.months[i].sum_debits : 0),
                            count   = (json.months[i] ? json.months[i].count : 0);

                        calendar.months.push({
							month   : moment().month(i - 1).format("MM"),
                            year    : year,
                            label   : moment().month(i - 1).format("MMMM"),
                            exist   : (json.months[i] ? true : false),
                            count   : count,
                            sum     : account_currency.toString(sum),
                            credits : account_currency.toString(credits),
                            debits  : account_currency.toString(debits),
                            c       : credits,
                            d       : Math.abs(debits),
                            color : (sum >= 0) ? 'green' : 'red'
                        });

                        if(i <= currentDate.getMonth() && count !== 0){
                            stats.global.counter += 1;
                            stats.global.sum += sum;
                            stats.global.credits += credits;
                            stats.global.debits += debits;
                        }
                    }

                    stats.average.sum = stats.global.sum / stats.global.counter;
                    stats.average.credits = stats.global.credits / stats.global.counter;
                    stats.average.debits = stats.global.debits / stats.global.counter;

                    for(i = 0, l = stats.average.length; i < l; i=i+1){
                        var new_currency = storage.currencies.get(stats.average[i].currency);
                        stats.average[i].old = account_currency.toString(stats.average[i].old);
                        stats.average[i].new = new_currency.toString(stats.average[i].new);
                        stats.average[i].average = account_currency.toString(stats.average[i].average);
                    }


                    for(i = 0, l = stats.categories.length; i < l; i=i+1){
                        stats.categories[i].category = storage.categories.get(stats.categories[i].category).toJSON();
                    }

                    var template = Mustache.render(DateSelectorPageTemplate, {
                        calendar: calendar,
                        stats: stats
                    });
                    $("#content").html(template);

                    $("#content .fitText").fitText();

                    // Init graph
                    var ctx = document.getElementById("expenseYearLine").getContext("2d");
                    var data = {
                        labels: _.pluck(calendar.months, 'label'),
                        datasets: [
                            {
                                label: "Crédits",
                                fillColor: "rgba(0,150,0,0.2)",
                                strokeColor: "rgba(0,150,0,1)",
                                pointColor: "rgba(0,150,0,1)",
                                pointStrokeColor: "#fff",
                                pointHighlightFill: "#fff",
                                pointHighlightStroke: "rgba(0,150,0,1)",
                                data: _.pluck(calendar.months, 'c')
                            },
                            {
                                label: "Débits",
                                fillColor: "rgba(151,0,0,0.2)",
                                strokeColor: "rgba(151,0,0,1)",
                                pointColor: "rgba(151,0,0,1)",
                                pointStrokeColor: "#fff",
                                pointHighlightFill: "#fff",
                                pointHighlightStroke: "rgba(151,0,0,1)",
                                data: _.pluck(calendar.months, 'd')
                            }
                        ]
                    };
                    var myNewChart = new Chart(ctx).Line(data, {
                        responsive: true
                    });


                    var ctx = document.getElementById("categorieYearPie").getContext("2d");
                    var data = [];
                    for(i = 0, l = stats.categories.length; i < l; i=i+1){
                        data.push({
                            value: Math.round(Math.abs(stats.categories[i].sum) * 100) / 100,
                            color: stats.categories[i].category.color,
                            highlight: stats.categories[i].category.color,
                            label: stats.categories[i].category.name
                        });

                    }

                        // {
                        //     value: 300,
                        //     color:"#F7464A",
                        //     highlight: "#FF5A5E",
                        //     label: "Red"
                        // },
                        // {
                        //     value: 50,
                        //     color: "#46BFBD",
                        //     highlight: "#5AD3D1",
                        //     label: "Green"
                        // },
                        // {
                        //     value: 100,
                        //     color: "#FDB45C",
                        //     highlight: "#FFC870",
                        //     label: "Yellow"
                        // }
                    
                    var myNewChart = new Chart(ctx).Pie(data, {
                        responsive: true
                    });
                }
            });
        }
    });

    return DashboardView;

});
