define('app', function(require) {

  var View = require('views/view')
    , sampleCollection = require('collections/collection');

  var sampleData
    , sampleView;
  
  sampleData = [
      { name: 'HTML5 Boilerplate' }
    , { name: 'Twitter Bootstrap' }
    , { name: 'Modernizr' }
    , { name: 'RequireJS' }
    , { name: 'Backbone.js' }
    , { name: 'Underscore.js' }
    , { name: 'and require-jade' }
  ];

  sampleCollection.reset(sampleData);
  console.log('collection:', JSON.stringify(sampleCollection));
  sampleView = new View({ collection: sampleCollection });
  sampleView.render();
  $('#yeoman-bootstrap').html(sampleView.el);

  return 'Hello from Yeoman! This page content was compiled through Jade!';
});