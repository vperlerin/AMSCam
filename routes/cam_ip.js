var PythonShell     = require('python-shell');
var express         = require('express');
var router          = express.Router();

var read_config     = require('../utils/read_config');
var utils           = require('../utils/browser');
var constants       = require('../utils/constants');
var cookie          = require('../utils/cookie');
 

exports.load =  function(req, res) {
    cookie.get_config_cookie_and_render(req, res, {}, 'ip');  
};

exports.update_ip =  function(req, res) {
     
    var new_cam_ip   = req.body.cam_ip;
    var _error      = [];
    
    // Test IPv4
    if (/(([0-1]?[0-9]{1,2}\.)|(2[0-4][0-9]\.)|(25[0-5]\.)){3}(([0-1]?[0-9]{1,2})|(2[0-4][0-9])|(25[0-5]))/.test(new_cam_ip)==false) {
           _error.push('IP Non Valid. Please enter an IPv4 IP.');
    }  
    
    if(_error.length !== 0 ) {
        // Error
        cookie.get_config_cookie_and_render(req, res,{errors : _error}, 'ip');       
     }  else {
         
        // We get the cookie values
        var cookie_config = req.cookies.config;  
        var first_time = false;
    
        // It is the first time?
        if (typeof cookie_config.cam_ip === 'undefined') {
            first_time = true;
        }
         
        // Send the new CAM IP
        cookie_config.cam_ip = new_cam_ip; 
         
        // We update the IP    
        var updateConfig = new PythonShell('update_config.py', {
            mode: 'json',
            scriptPath: constants.python_path+'/config',
            args:[JSON.stringify(cookie_config)]
        });
                      
        updateConfig.on('message',  function (config_write_res) { 
            // We clear the config cookie so it re-read from config.txt
            res.clearCookie("config",{path:'/'});  
                   
            // THIS IS OK
            if(first_time) {
                res.redirect('/');      
            } else {
                cookie.get_config_cookie_and_render(req, res,{ success : "IP updated."}, 'ip');         
            }
        }); 
     }
    

    
};


