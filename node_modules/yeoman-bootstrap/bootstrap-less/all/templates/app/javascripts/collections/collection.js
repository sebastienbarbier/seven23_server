// collections/collections.js

define('collections/collection', function(require) {
  'use strict';

  var Backbone = require('backbone');
  var Model = require('models/model');

  var Collection = Backbone.Collection.extend({
    model: Model,

    initialize: function(){

    }

  });

  return new Collection();
});