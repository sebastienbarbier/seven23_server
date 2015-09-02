define([
	'jquery',
	'underscore',
	'backbone',
	'mustache',
	'moment',
	'initView',
	'text!templates/transactions.mustache',
	'text!templates/transactions/debitscreditsForm.mustache',
	'debitsCreditsModel',
	'debitsCreditsCollection',
	'text!templates/transactions/changesForm.mustache',
	'changesModel',
	'changesCollection',
	'currenciesCollection',
	'text!templates/transactions/list.mustache',
	'text!templates/transactions/dateSelectPage.mustache',
	'storage'
], function(
	$,
	_,
	Backbone,
	Mustache,
	moment,
	InitView,
	TransactionsTemplate,
	DebitsCreditsFormTemplate,
	DebitsCreditsModel,
	DebitsCreditsCollection,
	ChangesFormTemplate,
	ChangesModel,
	ChangesCollection,
	CurrenciesCollection,
	listTemplate,
	DateSelectorPageTemplate,
	storage) {

	var collection = new DebitsCreditsCollection();
	var changesCollection = new ChangesCollection();

	var arrayAbstract = [];
	var nbSource = 0;

	var DashboardView = Backbone.View.extend({
		el: $("#content"),

		render: function(year, month) {

			var initView = new InitView();
			if (initView.isLoaded() === false) {
				initView.render();
			}

			initView.changeSelectedItem("nav_transactions");

			var template = Mustache.render(TransactionsTemplate, {
				year: year
			});
			$("#content").html(template);

			var view = this;

			arrayAbstract = [];

			collection.fetch({
				data: {'year': year, 'month': month},
				success: function() {
					view.generateListe(year, month);
				}
			});

		},


		generateListe: function(year, month) {
			// Generate array of all models
			arrayAbstract = _.union(collection.toArray(), storage.changes.toArray());

			var d = moment(year + "-" + month, "YYYY-MM").format("MMMM YYYY");
			// Date filter stuff
			if (year !== undefined && year !== null) {
				var dateStart;

				if (month !== undefined && month !== null) {
					dateStart = year + "-" + month;
				} else {
					dateStart = "" + year;
				}

				arrayAbstract = _.filter(arrayAbstract, function(c) {
					return c.get('date').indexOf(dateStart) === 0; //
				});
			}

			var template;

			// Feed each element with category object
			for (i = 0; i < arrayAbstract.length; i++) {
				var c = storage.categories.get(arrayAbstract[i].get('category'));
				if (c !== undefined) {
					arrayAbstract[i].set('categoryJSON', c.toJSON());
				}
			}

			//
			// PREPARE LIST OF RESULT
			// arrayAbstract is a list of transaction with categorieJSON.
			//

			// console.log(arrayAbstract);

			var bilan = {};
			bilan.total = 0;
			bilan.debits = 0;
			bilan.credits = 0;
			bilan.categories = {};
			bilan.counter = arrayAbstract.length;

			for (i = 0; i < arrayAbstract.length; i++) {
				var valeur;
				// Eliminate Change Model because has no isFavoriteCurrency
				var isFavorite = arrayAbstract[i].get('isFavoriteCurrency');

				if(isFavorite !== undefined && isFavorite !== null){
					var category = arrayAbstract[i].get('category');

					if(arrayAbstract[i].get('currency') === storage.user.currency()){
						valeur = arrayAbstract[i].get('amount');
					} else {
						valeur = arrayAbstract[i].get('reference_amount');
					}
					if(valeur >= 0){
						bilan.credits = bilan.credits + valeur;
					}else{
						bilan.debits = bilan.debits + valeur;
					}
					// If has categorw and is negative
					if(category && valeur < 0){
						// Sum by categories
						if(!bilan.categories[category]){
							bilan.categories[category] = 0;
						}
						bilan.categories[category] = bilan.categories[category] + valeur;
					}
				}
			}

			bilan.total = bilan.debits + bilan.credits;
			bilan.color = ((bilan.total >= 0) ? 'green' : 'red');


			bilan.total = storage.currencies.get(storage.user.currency()).toString(bilan.total);
			bilan.debits = storage.currencies.get(storage.user.currency()).toString(bilan.debits);
			bilan.credits = storage.currencies.get(storage.user.currency()).toString(bilan.credits);

			// Optimize categories
			bilan.categories = _.pairs(bilan.categories);

			bilan.categories = _.sortBy(bilan.categories, function(obj) {
				return obj[1];
			});

			for(var i=0, l=bilan.categories.length; i < l; i=i+1){
				try{
					bilan.categories[i][0] = storage.categories.get(bilan.categories[i][0]).toJSON();
					bilan.categories[i][2] = storage.currencies.get(storage.user.currency()).toString(bilan.categories[i][1]);
				}catch(e){

				}
			}
			//
			// Prepare Timeline
			//

			// Group by date, return JSON
			arrayAbstract = _.groupBy(arrayAbstract, function(obj) {
				return obj.get("date");
			});

			// Transform JSON to Array
			arrayAbstract = _.pairs(arrayAbstract);

			// Order by date
			arrayAbstract = _.sortBy(arrayAbstract, function(obj) {
				return obj[0];
			});
			// Reverse
			arrayAbstract.reverse();

			// Change date format
			for (i = 0; i < arrayAbstract.length; i++) {
				arrayAbstract[i][0] = moment(arrayAbstract[i][0], "YYYY-MM-DD").format("dddd D MMMM YYYY");
			}

			template = Mustache.render(listTemplate, {
				liste: arrayAbstract,
				bilan: bilan,
				year: year,
				date: d
			});

			$("#debitscredits").html(template);

			var view = this;

			// BIND EVENT
			$("button.addDebitCredit").on('click', function() {
				//transactionsFormView.render(year, month);
				Backbone.history.navigate("#/transactions/"+year+"/"+month+"/debitscredits/add", {
					trigger: true
				});
			});

			$("button.addChange").on('click', function() {
				//changesFormView.render(year, month);
				Backbone.history.navigate("#/transactions/"+year+"/"+month+"/changes/add", {
					trigger: true
				});
			});

			// Event create form on button click
			$(".element .edit").on('click', function() {
				var transaction = $(this).parents(".actions").prev();
				if (transaction.hasClass('debitcredit')) {
					var debitcredit = transaction.data('id');
					Backbone.history.navigate("#/transactions/"+year+"/"+month+"/debitscredits/edit/"+debitcredit, {
						trigger: true
					});
				} else if (transaction.hasClass('change')) {
					var change = transaction.data('id');
					Backbone.history.navigate("#/transactions/"+year+"/"+month+"/changes/edit/"+change, {
						trigger: true
					});
				}
			});

			$(".element .delete").on('click', function() {
				var transaction = $(this).parents(".actions").prev();
				if (transaction.hasClass('debitcredit')) {
					var debitcredit = transaction.data('id');
					collection.get(debitcredit).destroy({
						// prints nothing!!!
						success: function() {
							view.render(year, month);
						},
						error: function() {
							view.render(year, month);
						}
					});
				} else if (transaction.hasClass('change')) {
					var change = $(this).parents(".actions").prev().data('id');
					storage.changes.get(change).destroy({
						// prints nothing!!!
						success: function() {
							view.render(year, month);
						},
						error: function() {
							view.render(year, month);
						}
					});
				}
			});

			// If there is some data, we display
			if (arrayAbstract.length) {
				// Pie categroy chart
				var ctx = document.getElementById("categorieYearPie").getContext("2d");
	            var data = [];
	            for(i = 0, l = bilan.categories.length; i < l; i=i+1){
	                data.push({
	                    value: Math.round(Math.abs(bilan.categories[i][1]) * 100) / 100,
	                    color: bilan.categories[i][0].color,
	                    highlight: bilan.categories[i][0].color,
	                    label: bilan.categories[i][0].name
	                });
	            }

	            var myNewChart = new Chart(ctx).Pie(data, {
	                responsive: true,
	                animation : false
	            });
			}



		}
	});

	return DashboardView;

});
