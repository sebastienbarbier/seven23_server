require.config({

  paths: {
    backbone: ['../components/backbone/backbone', '../components/backbone/backbone-min']
  , bootstrap: ['../components/bootstrap/bootstrap/js/bootstrap.min', '../components/bootstrap/bootstrap/js/bootstrap']
  , jade: '../components/require-jade/jade'
  , jquery: ['../components/jquery/jquery', '../components/jquery/jquery.min']
  , underscore: ['../components/underscore/underscore-min', '../components/underscore/underscore']
  },

  shim: {
    'backbone': {
      deps: ['jquery', 'underscore'],
      exports: 'Backbone'
    },
    'underscore': {
      deps: ['jquery'],
      exports: '_'
    },
    'bootstrap': {
      deps: ['jquery'],
      exports: 'bootstrap'
    },
    'app': {
      deps: ['backbone']
    }

  }

});

require(['app'], function(app) {
  'use strict';
  console.log(app);
  // Backbone.history.start({pushState: true});
});