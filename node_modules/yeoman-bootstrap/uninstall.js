// Copyright (c) 2013 Vincent Mac <vincent@vincentmac.com>
// uninstall.js

/**
 * This is a simple script to remove/unlink this generator from the yeoman global
 * generators directory upon uninstall.
 */

'use strict';

var fs = require('fs')
  , path = require('path')
  , yeomanGeneratorPath
  , yeoman;

// Relative path to yeoman generators
yeomanGeneratorPath = 'yeoman/node_modules/yeoman-generators/lib/generators';

// Full path to yeoman generators
yeoman = path.resolve(__dirname, '..', yeomanGeneratorPath);

/**
 * Remove existing symlink to bootstrap generator
 */

function unlinkPrevious() {
  fs.unlink(path.resolve(yeoman, 'bootstrap-less'), function(err) {
    if (err) return console.log('unlink error:', err);
    return console.log('yeoman-bootstrap successfully unlinked from global generators directory.',
      'Proceed with uninstall...');
  });
}

// Check if bootstrap generator is installed in global generators directory
fs.exists(path.resolve(yeoman, 'bootstrap-less'), function(bootstrapExists) {
  if (bootstrapExists) {
    console.log('yeoman-bootstrap found.  Proceed with unlink...');
    unlinkPrevious();
  }
});

