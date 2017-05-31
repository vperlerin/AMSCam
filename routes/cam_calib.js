var PythonShell     = require('python-shell');
var express         = require('express');
var router          = express.Router();

var read_config     = require('../utils/read_config');
var utils           = require('../utils/browser');
var constants       = require('../utils/constants');

/******************************************************************************************************************************************
* Restart Cam
***********************************************/
exports.restart = function(req, res) {
    
    // Test Browser
    browser = utils.get_browser(req)
    
    var opts         = {scriptPath: constants.python_path + "/cam" };
    var render_opts  = {browser:  browser };
    
        
    // Get Current Cam Parameters
    PythonShell.run('restart_cam_server.py', opts, function (err, ress) {
       if (err) throw err;
            res.redirect('../?msg='+'Camera restarting');
      });
  
    
};


/******************************************************************************************************************************************
* Cam calibration
***********************************************/
exports.load = function(req, res) {
    
    // Test Browser
    browser = utils.get_browser(req)
    
    var opts         = {scriptPath: constants.python_path + "/cam" };
    var render_opts  = {browser:  browser };
    
   
    if(typeof req.query.file == "undefined") {
        opts['args']  = ['Calibration'];
    } else {
        opts['args']  = [req.query.file];
    }
       
    // Get Current Cam Parameters
    PythonShell.run('get_parameter_from_file.py', opts, function (err, ress) {
       if (err) throw err;
       // Render
       read_config.test_cam_pwd(res,'parameters',{ browser:  browser, calib: JSON.parse(ress), active_file:opts['args']});
     });
  
    
};


/******************************************************************************************************************************************
* Update Cam calibration (JSON CALL)
***********************************************/
exports.post = function(req, res) {
         
    var opts = {    args: [JSON.stringify(req.body)],
                    scriptPath: constants.python_path + "/cam" 
    };
      
    PythonShell.run('set_parameters_to_file.py', opts, function (err, ress) {
        if (err) throw err;
        res.setHeader('Content-Type', 'application/json');
        res.send(JSON.stringify({ "RES": ress }, null, 3));
    });
};


/******************************************************************************************************************************************
* Auto load the proper set of parameters depending on the sun position
***********************************************/
exports.load_auto_param = function(req, res) {
         
    var opts = {    
        args: [JSON.stringify(req.body)],
        scriptPath: constants.python_path + "/cam" 
    };
      
    PythonShell.run('auto_set_parameters.py', opts, function (err, ress) {
        if (err) throw err;
        res.redirect('/');
    });
};