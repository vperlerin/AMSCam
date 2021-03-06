var PythonShell     = require('python-shell');
var express         = require('express');
var router          = express.Router();
 
var read_config     = require('../utils/read_config');
var utils           = require('../utils/browser');
var constants       = require('../utils/constants');

/******************************************************************************************************************************************
* Read Log
***********************************************/
exports.load =  function(req, res) {
      
        if(typeof req.query.ot != "undefined") {
            
            // Pass something in argument (API Style)
            var dt = new Date();
            var tt   = (typeof req.query.time == "undefined")?dt.toUTCString():req.query.time;
            var val1 = req.query.ot;
            var val2 = req.query.it;
            var val3 = req.query.ih; 
            var to_update = {'log':tt+'$'+val1+'$'+val2+'$'+val3}; 
         
            var writeLog = new PythonShell('write_log.py', {
                    mode: 'text' ,
                    scriptPath: constants.python_path + "/log",
                    args:[constants.cam_log_file,JSON.stringify(to_update)]
            });
            
            writeLog.on('message', function () {  
                  res.redirect('/cam/log');
            }); 
            
        }  else {
            
             // Pass nothing
    
            var readLog = new PythonShell('read_log.py', {
                    mode: 'text' ,
                    scriptPath: constants.python_path + "/log",
                    args:[constants.cam_log_file]
            });
            
            readLog.on('message', function (log_cont) {  
                cookie.get_config_cookie_and_render(req, res, {log_content:JSON.parse(log_cont)}, 'log'); 
            });
        }
};

/*********************************************** 
* Add Log entry (from form)
***********************************************/
exports.add =  function(req, res) {
       
        var tt   = req.body.timeV;
        var val1 = req.body.val1;
        var val2 = req.body.val2;
        var val3 = req.body.val3; 
        var to_update = {'log':tt+'$'+val1+'$'+val2+'$'+val3}; 
       
        var writeLog = new PythonShell('write_log.py', {
                mode: 'text' ,
                scriptPath: constants.python_path + "/log",
                args:[constants.cam_log_file,JSON.stringify(to_update)]
        });
        
        writeLog.on('message', function () {  
              res.redirect('/cam/log');
        }); 
 };


/*********************************************** 
* Clean log
***********************************************/
exports.clean =  function(req, res) {
       
        var delLog = new PythonShell('del_log.py', {
            mode: 'text' ,
            scriptPath: constants.python_path + "/log",
            args:[constants.cam_log_file]
        });
        
        delLog.on('message', function () {  
              res.redirect('/cam/log');
        }); 
 };
