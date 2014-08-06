// views/view.js

define('views/view', function(require) {
  'use strict';

  var Backbone = require('backbone')
    , template = require('jade!templates/template');

  var View = Backbone.View.extend({
    
    /**
     * Using a `Jade` template in `Backbone.js`
     *
     * Since Jade lets you do some basic coding, if your template
     * has any code that needs to be evaluated against your dataset,
     * such as iterating over an array (ie `each item, i in items`) or
     * evaluating any conditional statements (ie `if (user.role == 'admin')...`)
     * you will want to include that data when setting your view's template
     * and will, thus, want to defer setting your template until you are
     * ready to render.
     *
     * If you have a template that just displays data that is passed in
     * (ie `p #{user.name}`) then you can set your template the traditional
     * backbone way:
     *    `template: _.template(template()),`
     */

    // template: _.template(template()),
    template: {},

    initialize: function() {

    },

    render: function() {
      var data = this.collection.toJSON();
      console.log(data);

      // Evaluate code in Jade template.
      this.template = _.template(template(data));

      var $el = $(this.el);
      $el.html(this.template());
      return this;
    }

  });

  return View;
});