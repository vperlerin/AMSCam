var PythonShell     = require('python-shell');
var constants       = require('../utils/constants');
var async           = require('async');
 
function define(name, value) {
    Object.defineProperty(exports, name, {
        value:      value,
        enumerable: true
    });
}


define("read_config", function read_config(callback) {
    var pyshellUpload = new PythonShell('read_config.py', {
        mode: 'json',
        scriptPath: constants.python_path +'/config',
        argv: ['json']
    });
    
    return async.parallel([
           function() {
            pyshellUpload.on('message',  function (config) {  
                callback(config);
            });
       }
    ]);
});


  
// Test if the cam password has been setup (read the config_file)
// if not, redirect to /cam/update_cam_pwd
define("load_page_with_conf_test_cam_pwd", function load_page_with_conf_test_cam_pwd(res,template,template_args) {
    
    var pyshellUpload = new PythonShell('read_config.py', {
        mode: 'json',
        scriptPath: constants.python_path +'/config',
        argv: ['json']
    });
   
   return async.parallel([
       function() {
            pyshellUpload.on('message',  function (config) { 
              
                if(typeof config.cam_pwd  === "undefined" || config.cam_pwd === "admin") {
                    res.redirect('/cam/update_cam_pwd');    
                    return true;
                } else {
                    // Add the config to the template
                    template_args.config = config;
                    res.render(template,template_args);
                    return false;   
                }
            })
       }
    ]);
});
 