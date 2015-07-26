define([
	'jquery',
	'underscore',
	'backbone',
	'mustache',
	'initView',
	'text!templates/transactions/debitscreditsForm.mustache',
	'debitsCreditsModel',
	'debitsCreditsCollection',
	'storage',
	'bootstrap-datepicker'
], function(
	$,
	_,
	Backbone,
	Mustache,
	InitView,
	DebitsCreditsFormTemplate,
	DebitsCreditsModel,
	DebitsCreditsCollection,
	storage) {

	var arrayAbstract = [];
	var nbSource = 0;

	var DashboardView = Backbone.View.extend({
		el: $("#content"),

		displayForm: function(year, month, debitcredit){

			if (debitcredit && debitcredit.amount > 0) {
				debitcredit.credit = debitcredit.amount;
			}
			if (debitcredit && debitcredit.amount < 0) {
				debitcredit.debit = debitcredit.amount * -1;
			}

			var template = Mustache.render(DebitsCreditsFormTemplate, {
				debitcredit: debitcredit,
				currencies: storage.currencies.toJSON(),
				categories: storage.categories.toJSON()
			});

			$("#content").html(template);

			$('#content input.datepicker').datepicker({
				format: 'yyyy-mm-dd',
				autoclose: true
			});

			// Put select markup as selected
			if (debitcredit) {
				$("#debitcredit_form select[name='currency']").find('option[value="' + debitcredit.currency + '"]').attr('selected', true);
				$("#debitcredit_form select[name='category']").find('option[value="' + debitcredit.category + '"]').attr('selected', true);
			} else {
				$("#debitcredit_form select[name='currency']").find('option[value="' + storage.user.currency() + '"]').attr('selected', true);
			}

			var view = this;
			// User cancel form. We go back to view page.
			$("button.debitscredits_form_cancel").on("click", function() {
				Backbone.history.navigate("#/transactions/"+year+"/"+month, {
					trigger: true
				});
			});

			$("#debitcredit_form").on("submit", function() {

				var array = $("#debitcredit_form").serializeArray();
				var dict = {};

				for (var i = 0; i < array.length; i++) {
					dict[array[i]['name']] = array[i]['value'];
				}
				
				if (!dict['debit']) {
					dict['debit'] = 0;
				} else {
					dict['debit'] = dict['debit'].replace(',', '.');
				}
				if (!dict['credit']) {
					dict['credit'] = 0;
				} else {
					dict['credit'] = dict['credit'].replace(',', '.');
				}

				if (dict['category'] == "") {
					delete dict['category'];
				}

				dict['account'] = storage.user.get('accounts')[0].id;
				dict['amount'] = dict['credit'] - dict['debit'];

				var debitcredit = new DebitsCreditsModel(dict);

				Backbone.Validation.bind(this, {
			      model: debitcredit,
			      valid: function(view, attr) {

					// Check if all are required
				    $(view).find('input[name=' + attr + '], select[name=' + attr + ']')
				    	.parent()
				    	.removeClass('has-error')
				    	.addClass('has-success')
				    	.prev().html('');
					
			      },
			      invalid: function(view, attr, error) {

				    $(view).find('input[name=' + attr + '], select[name=' + attr + ']')
				    	.parent()
				    	.addClass('has-error')
				    	.removeClass('has-success')
				    	.prev().html(error);

			      }
			    });

				debitcredit.validate();

				if (debitcredit.isValid()) {
					debitcredit.save(dict, {
						wait: true,
						success: function(model, response) {
							console.log('Successfully saved!');
							Backbone.history.navigate("#/transactions/"+year+"/"+month, {
								trigger: true
							});

						},
						error: function(model, error) {
							console.log(model.toJSON());
							console.log('error.responseText');
						}
					});
				}
				// prevent default behaviour
				return false;
			});
		},

		render: function(year, month, debitcredit_id) {

			var initView = new InitView();
			if (initView.isLoaded() === false) {
				initView.render();
			}

			initView.changeSelectedItem("nav_transactions");

			var view = this;

			if(debitcredit_id){
				var debitcredit = new DebitsCreditsModel({id: debitcredit_id});
				debitcredit.fetch({
			        success: function (c) {
			            view.displayForm(year, month, debitcredit.toJSON());
			        }
			    });
			}else{
				view.displayForm(year, month);
			}
		}

	});

	return DashboardView;

});
