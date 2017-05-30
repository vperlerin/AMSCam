var PythonShell     = require('python-shell');
var express         = require('express');
var router          = express.Router();

var read_config     = require('../utils/read_config');
var constants       = require('../utils/constants');


/******************************************************************************************************************************************
* Screenshot Page
***********************************************/
exports.load = function(req, res)   {
    
    // If the cam password has already been updated:
    read_config.test_cam_pwd(res,'screenshot',{});
    
};


/**********************************************
* Take screenshot
***********************************************/
exports.update = function(req, resp) {
 
        var pyshellUpload = new PythonShell('upload_latest.py', {
            mode: 'json' ,
            scriptPath: constants.python_path+'/cam'
         });
        
        // JSON.stringify(message_success, null, '\t')
        pyshellUpload.on('message', function (message_success) { 
            if (message_success) {
                // Render
                return read_config.test_cam_pwd(resp,'screenshot',{  message_success: message_success});
             }        
        });
};