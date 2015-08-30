define("ws", ["jquery"], function($) {
	// Define API Server
	var server = {
		protocol: (APP_CONFIG.apiProtocol ? APP_CONFIG.apiProtocol : "https"),
		domain: (APP_CONFIG.apiUrl ? APP_CONFIG.apiUrl : "api.723e.com"),
		port: (APP_CONFIG.apiPort ? APP_CONFIG.apiPort : "80"),
		url: function() {
			return this.protocol + "://" + this.domain + ":" + this.port;
		}
	};

	// This service describe remote API
	var init = server.url() + "/api/v1/init/";

	var v1 = {
		// List all user accounts
		accounts: server.url() + "/api/v1/accounts",
		// List all user accounts
		users: server.url() + "/api/v1/users",
		// List all user debitscredits
		debitscredits: server.url() + "/api/v1/debitscredits",
		// List all user debitscredits
		changes: server.url() + "/api/v1/changes",
		//
		currencies: server.url() + "/api/v1/currencies",
		//
		resume_year: server.url() + "/api/v1/resume_year/", // "/api/v1/resume_year/2014/"
		// List all user accounts
		categories: server.url() + "/api/v1/categories",
		// Get token key
		login: server.url() + "/api/api-token-auth/",
		// Create an account
		subscription: server.url() + "/api/v1/subscription/"
	};

	// Authentification Token Key
	var key = sessionStorage.getItem("key");

	var _setToken = function(_key) {
		key = _key;
		sessionStorage.setItem("key", _key);
	};


	var _ajax = function(type, _options) {

		// list configuration
		options = $.extend({
			type: type
		}, _options);

		// Hook into jquery
		// Use withCredentials to send the server cookies
		// The server must allow this through response headers
		$.ajaxPrefilter(function(options, originalOptions, jqXHR) {
			// If we have a csrf token send it through with the next request
			if (key) {
				jqXHR.setRequestHeader('Authorization', 'Token ' + key);
			}
		});

		return $.ajax(options);
	};

	var _get = function(_options) {
		return _ajax('GET', _options);
	};
	var _post = function(_options) {
		return _ajax('POST', _options);
	};
	var _push = function(_options) {
		return _ajax('PUSH', _options);
	};
	var _delete = function(_options) {
		return _ajax('DELETE', _options);
	};

	return {
		// This object return server access.
		init: init,
		v1: v1,
		get: _get,
		post: _post,
		push: _push,
		del: _delete,
		setToken: _setToken
	};
});
