define(["jquery", "backbone", "ws", "validator"], function($, Backbone, WebServices) {
    var subscription = Backbone.Model.extend({
        urlRoot: WebServices.v1.subscription,
        defaults: {},
        initialize: function() {
            //alert("Welcome to this world");
        },
        validation: {
            username: {
                required: true
            },
            email: [{
		      required: true,
		      msg: 'Please enter an email address'
		    },{
		      pattern: 'email',
		      msg: 'Please enter a valid email'
		    }],
            password: {
		      required: true
		    },
		    passwordRepeat: {
		      equalTo: 'password'
		    },
		    name: {
		      required: true
		    },
			currency: {
		      required: true
		    }
        }
    });
    return subscription;
});