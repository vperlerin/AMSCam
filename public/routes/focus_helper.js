var PythonShell     = require('python-shell');
var express         = require('express');
var router          = express.Router();
var repeat          = require('repeat');
 
var read_config     = require('../utils/read_config');
var utils           = require('../utils/browser');
var constants       = require('../utils/constants');
var cookie          = require('../utils/cookie');


/******************************************************************************************************************************************
* FOCUS HELPER
***********************************************/ 
exports.load = function(req, res) {
      cookie.get_config_cookie_and_render(req, res, {}, 'focus_helper');   
};


/*********************************************** 
* START FOCUS HELPER
***********************************************/
exports.start = function(req, res) {
   
    // Setup the repeat
    var _interval  = req.body._interval;
    var _period    = req.body._period;
    var _delay     = req.body._delay; 
  
   
    repeat(function(done) {
        
       PythonShell.run('upload_latest.py', {
            mode: 'text' ,
            scriptPath: constants.python_path+'/cam'
       }, function (err, results) {
            done();
       });
          
    }).every(_interval, 'sec').for(_period, 'sec').start.in(_delay, 'sec').then(function() {
        var dt = new Date(); 
        cookie.get_config_cookie_and_render(req, res, {'success':'Focus helper stopped on ' +   dt.toUTCString()}, 'focus_helper');    
    });
   
    
};