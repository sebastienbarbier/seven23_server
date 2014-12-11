define([
        "jquery",
        "backbone",
        "ws",
        "mustache",
        "text!templates/transactions/timeline/debitsCreditsTemplate.mustache",
        "storage"
    ],
    function(
        $,
        Backbone,
        WebServices,
        Mustache,
        debitsCreditsTemplate,
        storage) {

        var debitscredits = Backbone.Model.extend({
            urlRoot: WebServices.v1.debitscredits,
            defaults: {
                isCredit: function() {
                    return this.get('amount') >= 0;
                },
                isDebit: function() {
                    return this.get('amount') < 0;
                },
                isFavoriteCurrency: function() {
                    return this.debitsCredits.currency_id === storage.user.currency();
                },
                defaultCurrency: function() {
                    return storage.currencies.get(this.debitsCredits.currency_id).toString(this.debitsCredits.amount);
                },
                favoriteCurrency: function() {
                    return storage.currencies.get(storage.user.currency()).toString(this.debitsCredits.reference_amount);
                }
            },
            html: {
                list: function() {
                    return Mustache.render(debitsCreditsTemplate, {
                        debitsCredits: this.toJSON()
                    });
                }
            }
        });

        return debitscredits;
    });
