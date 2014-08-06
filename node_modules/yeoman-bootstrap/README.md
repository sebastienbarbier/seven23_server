yeoman-bootstrap
=================

This is a [yeoman](http://yeoman.io) generator that scaffolds out a project using [Twitter Bootstrap](http://getbootstrap.com) by default, expanding on yeoman's `quickstart` generator.  This generator will install *Twitter Bootstrap*, *jQuery*, *Backbone.js*, *Underscore.js*, *Modernizr*, *Require.js*, and *require-jade*.

## Installation

You can install this generator globally via npm:

`[sudo] npm install -g yeoman-bootstrap`

I have only tested this on Mac OS X, but it should work in Windows and other *nix environments. During a global npm install, the generator will get installed in your global `node_modules` directory, while a symlink to the foundation generator will be created in your global yeoman generators directory:

`/usr/local/lib/node_modules/yeoman/node_modules/yeoman-generators/lib/generators/bootstrap-less/`

## Usage

After copying to your global generator location, use:

`yeoman init bootstrap-less` 

to generate the basic scaffolding for a bootstrap based project.

This generator provides a scaffold that uses require.js to load javascript modules. After generating the project scaffolding a [node child_process](http://nodejs.org/api/child_process.html#child_process_child_process_spawn_command_args_options) will run to install jQuery, Backbone, and Require.js along with any dependencies.  This child process is running 
`yeoman install jquery backbone modernizr bootstrap requirejs require-jade --save`
so you don't have to after.

Note: There is a bug in Yeoman 0.9.6 that is preventing the `--save` argument from adding files to `component.json`.  If you would like your components saved in there, run: 
`bower install jquery backbone modernizr bootstrap requirejs require-jade --save`
to add them.

## Uninstall

You can uninstall this generator via npm:

`[sudo] npm uninstall -g yeoman-bootstrap`

This will remove the symlink in your global yeoman generators directory and then proceed to delete the package.