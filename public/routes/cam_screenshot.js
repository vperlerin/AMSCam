var PythonShell     = require('python-shell');
var express         = require('express');
var router          = express.Router();

var constants       = require('../utils/constants');
var cookie          = require('../utils/cookie');


/******************************************************************************************************************************************
* Screenshot Page
***********************************************/
exports.load = function(req, res)   {
    cookie.get_config_cookie_and_render(req, res, {}, 'screenshot');   
};


/**********************************************
* Take screenshot
***********************************************/
exports.update = function(req, res) {
 
        var pyshellUpload = new PythonShell('upload_latest.py', {
            mode: 'json' ,
            scriptPath: constants.python_path+'/cam'
         });
        
        // JSON.stringify(message_success, null, '\t')
        pyshellUpload.on('message', function (message_success) { 
            if (message_success) {
                // Render
                
                return cookie.get_config_cookie_and_render(req, res, {  message_success: message_success}, 'screenshot');    
             }        
        });
};