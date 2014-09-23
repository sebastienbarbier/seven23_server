define("ws", ["jquery"], function($) {
	// Define API Server
	var server = {
		protocol: "http",
		domain: "localhost",
		port: "8000",
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
		//
		currencies: server.url() + "/api/v1/currencies",
		// List all user accounts
		categories: server.url() + "/api/v1/categories",
		// Get token key
		login: server.url() + "/api/api-token-auth/"
	}

	// Authentification Token Key
	var key = sessionStorage.getItem("key");

	var _setToken = function(_key) {
		key = _key;
		sessionStorage.setItem("key", _key);
	}


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
			if (key !== null && key != undefined) {
				jqXHR.setRequestHeader('Authorization', 'Token ' + key);
			}
		});

		return $.ajax(options);
	}

	var _get = function(_options) {
		return _ajax('GET', _options);
	}
	var _post = function(_options) {
		return _ajax('POST', _options);
	}
	var _push = function(_options) {
		return _ajax('PUSH', _options);
	}
	var _delete = function(_options) {
		return _ajax('DELETE', _options);
	}

	return {
		// This object return server access.
		init: init,
		v1: v1,
		get: _get,
		post: _post,
		push: _push,
		del: _delete,
		setToken: _setToken
	}
});
