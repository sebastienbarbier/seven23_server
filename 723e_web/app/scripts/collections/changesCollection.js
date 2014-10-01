define(["jquery", "backbone", "ws", "changesModel"], function($, Backbone, WebServices, ChangesModel) {

	var changes = Backbone.Collection.extend({
		model: ChangesModel,
		url: WebServices.v1.changes
	});

	return changes;
});
