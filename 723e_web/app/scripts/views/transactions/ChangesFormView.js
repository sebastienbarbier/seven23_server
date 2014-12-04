define([
	'jquery',
	'underscore',
	'backbone',
	'mustache',
	'initView',
	'text!templates/transactions/changesForm.mustache',
	'changesModel',
	'storage',
	'bootstrap-datepicker'
], function(
	$,
	_,
	Backbone,
	Mustache,
	InitView,
	ChangesFormTemplate,
	ChangesModel,
	storage) {

	var arrayAbstract = [];
	var nbSource = 0;

	var DashboardView = Backbone.View.extend({
		el: $("#content"),

		displayForm: function(year, month, change){


			var template = Mustache.render(ChangesFormTemplate, {
				change: change,
				currencies: storage.currencies.toJSON()
			});
			$("#content").html(template);

			$('#content input.datepicker').datepicker({
				format: 'yyyy-mm-dd',
				autoclose: true
			});

			// Put select markup as selected
			if (change) {
				$("#changes_form select[name='currency']").find('option[value="' + change.currency + '"]').attr('selected', true);
				$("#changes_form select[name='new_currency']").find('option[value="' + change.new_currency + '"]').attr('selected', true);
				$("#changes_form select[name='category']").find('option[value="' + change.category + '"]').attr('selected', true);
			}

			var view = this;
			// User cancel form. We go back to view page.
			$("button.changes_form_cancel").on("click", function() {
				Backbone.history.navigate("#/transactions/"+year+"/"+month, {
					trigger: true
				});
			});

			$("button.changes_form_submit").on("click", function() {

				var array = $("#changes_form").serializeArray();
				var dict = {};

				for (var i = 0; i < array.length; i++) {
					dict[array[i]['name']] = array[i]['value']
				}
				dict['user'] = "http://localhost:8000/api/v1/users/1";

				var change;
				if(dict['id'] !== undefined){
					change = storage.changes.get(dict['id']).set(dict);
				}else{
					change = new ChangesModel(dict);
				}

				change.save(dict, {
					wait: true,
					success: function(model, response) {
						storage.changes.add(model);
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
			});
		},

		render: function(year, month, change_id) {
			var initView = new InitView();
			if (initView.isLoaded() === false) {
				initView.render();
			}

			initView.changeSelectedItem("nav_transactions");

			var view = this;

			if(change_id){
			    view.displayForm(year, month, storage.changes.get(change_id).toJSON());
			}else{
				view.displayForm(year, month);
			}
		}
	});

	return DashboardView;

});
