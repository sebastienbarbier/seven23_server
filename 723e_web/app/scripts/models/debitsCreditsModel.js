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
                    return this.debitsCredits.amount >= 0;
                },
                isDebit: function() {
                    return this.debitsCredits.amount < 0;
                },
                isFavoriteCurrency: function() {
                    return !this.debitsCredits.isForeignCurrency;
                },
                defaultCurrency: function() {
                    return storage.currencies.get(this.debitsCredits.currency).toString(this.debitsCredits.amount);
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
            },
            validation: {
                name: {
                    required: true
                },
                amount: function(value, attr, computedState) {
                    if(value === 0) {
                      return 'Amount is required';
                    }
                },
                date: {
                  required: true
                },
                currency: {
                  required: true
                }
            }
        });

        return debitscredits;
    });
