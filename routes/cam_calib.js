var PythonShell     = require('python-shell');
var express         = require('express');
var router          = express.Router();

var utils           = require('../utils/browser');
var constants       = require('../utils/constants');
var cookie          = require('../utils/cookie');

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
    
    var file = (typeof req.params.file!=='undefined' && constants.possible_parameters_files.indexOf(req.params.file)>-1)?req.params.file:'';
    
     
    if(file.trim() === "" || typeof req.cookies.config !== "undefined") {
         
        // By default we load the currently used param file (in the config cookie)
        var cookie_config = req.cookies.config;  
        
        // If absent from the config file
        if(typeof config === "undefined" || typeof cookie_config.parameters === "undefined") {
            cookie_config = {}
            cookie_config.parameters  = "Day";
        }
        
        PythonShell.run('get_parameter_from_file.py', {scriptPath: constants.python_path + "/cam", args:[cookie_config.parameters] }, function (err, ress) {
            if (err) throw err;
            // Render 
            cookie.get_config_cookie_and_render(req, res, { browser:  browser, calib: JSON.parse(ress), active_file:cookie_config.parameters, exposures:constants.EXPOSURE_TIME}, 'parameters');  
        });
          
    } else {
         
         // We delete the config cookie so parameters value will be updated
         res.clearCookie("config", {path:'/'});
         
         // Or we load the file passed in arg
         opts['args']  = [file];
         PythonShell.run('get_parameter_from_file.py', opts, function (err, ress) {
           if (err) throw err;
           // Render 
           cookie.get_config_cookie_and_render(req, res,{ browser:  browser, calib: JSON.parse(ress), active_file:opts['args'], exposures:constants.EXPOSURE_TIME}, 'parameters');  
          
         }); 
    }
  
 
};


/******************************************************************************************************************************************
* Update Cam calibration (JSON CALL)
***********************************************/
exports.post = function(req, res) {
         
    var opts = { args: [JSON.stringify(req.body)],
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
    
    // We delete the config cookie so parameters value will be updated
    res.clearCookie("config", {path:'/'});
      
    PythonShell.run('auto_set_parameters.py', opts, function (err, ress) {
        if (err) throw err;
        res.redirect('/');
    });
};

