var PythonShell     = require('python-shell');
var express         = require('express');
var router          = express.Router();
var repeat          = require('repeat');
 
var read_config     = require('../utils/read_config');
var utils           = require('../utils/browser');
var constants       = require('../utils/constants');


/******************************************************************************************************************************************
* FOCUS HELPER
***********************************************/
// app.get('/cam/focus_helper', 

exports.load = function(req, res) {
      read_config.load_page_with_conf_test_cam_pwd(res,'focus_helper',{});
};


/*********************************************** 
* START FOCUS HELPER
***********************************************/
// ('/cam/focus_helper'
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
        read_config.load_page_with_conf_test_cam_pwd(res,'focus_helper',{'success':'Focus helper stopped on ' +   dt.toUTCString()});
    });
   
    
};