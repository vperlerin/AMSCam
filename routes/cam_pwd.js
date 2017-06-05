var PythonShell     = require('python-shell');
var express         = require('express');
var router          = express.Router();

var read_config     = require('../utils/read_config');
var utils           = require('../utils/browser');
var constants       = require('../utils/constants');


/******************************************************************************************************************************************
* UPDATE CAM PWD (GET)
***********************************************/
 exports.load = function(req, res) {
     
    var pyshellReadConfig = new PythonShell('read_config.py', {
            mode: 'json',
            scriptPath: constants.python_path +'/config',
            argv: ['json']
    });
        
    // Read config
    pyshellReadConfig.on('message',  function (config) { 
          
          // Test if config.cam_pwd has been updated 
          // to properly display the warning message
          
          if(typeof config.cam_pwd === "undefined" || config.cam_pwd === "admin") {
             delete config.cam_pwd; 
          }
      
          res.render('update_cam_pwd', {
             config: config
          });
    });
    
};


/******************************************************************************************************************************************
* UPDATE CAM PWD (POST)
***********************************************/
 exports.update_cam_pwd =  function(req, res) {
    
    var old_pwd     = req.body.oldPwd;
    var new_pwd     = req.body.newPwd;
    var new_pwd2    = req.body.newPwd2;
    var _error      = [];
    var first_time  = false;
    var redirected  = false;
    
    var pyshellReadConfig = new PythonShell('read_config.py', {
        mode: 'json',
        scriptPath: constants.python_path +'/config',
        argv: ['json']
    });
    
    // Read config
    pyshellReadConfig.on('message',  function (config) { 
     
        // Test if new passwords match
        if(new_pwd !== new_pwd2) {
            _error.push('The 2 new passwords don\'t match. Please, try again.');
        }
        
        // Test if new passwords != admin
        if(new_pwd === 'admin') {
            _error.push('For security reasons, "admin" is forbidden as the camera password. Please, enter a new password.');
        }
        
        // Test the old pwd 
        if(typeof config.cam_pwd !== 'undefined') {
            
            if(config.cam_pwd !== old_pwd) {
                _error.push('The old password is wrong. Please, try again.');
            }
            
            if(config.cam_pwd == 'admin' && _error.length == 0) {
                 
                    // First time we update the password: we redirect to the home
                    config.new_cam_pwd = new_pwd;
                 
                    var updateConfig = new PythonShell('update_config.py', {
                        mode: 'json',
                        scriptPath: constants.python_path+'/config',
                        args:[JSON.stringify(config)]
                    });
                      
                    redirected = true;
                      
                    updateConfig.on('message',  function (config_write_res) { 
                         return res.redirect('/');    
                    });
             }
            
            
            
        } else {
            if(old_pwd !== 'admin') {
                _error.push('The old password has never been updated. Please, try "admin".');
            }  
        }
          
        if(!redirected) {
          
            // Error
            if(_error.length !== 0 ) {
                
                if(typeof config.cam_pwd === "undefined" || config.cam_pwd === "admin") {
                    delete config.cam_pwd; 
                }
                         
                // We have an error: we redirect with the error message
                res.render('update_cam_pwd', {
                    config : config,
                    errors : _error
                });
               
             } else {
                  
                    // Add PWD to the config file
                    config.new_cam_pwd = new_pwd;
                     
                    var updateConfig = new PythonShell('update_config.py', {
                        mode: 'json',
                        scriptPath: constants.python_path+'/config',
                        args:[JSON.stringify(config)]
                    });
                      
                    updateConfig.on('message',  function (config_write_res) { 
                              res.render('update_cam_pwd', {
                                config : config_write_res,
                                success : "Password updated"
                            });
                    });
              
             }
        }
    });
    
};
    
    


/******************************************************************************************************************************************
* FORGET CAM PWD (send email)
***********************************************/
 exports.forget_cam_pwd =  function(req, res) {
    
    var pyshellReadConfig = new PythonShell('read_config.py', {
            mode: 'json',
            scriptPath: constants.python_path +'/config',
            argv: ['json']
    });
     
    // Read config
    pyshellReadConfig.on('message',  function (config) { 
        if(typeof config.cam_pwd === 'undefined') {
             config.cam_pwd = 'admin'; // Default (in the case the user ask to send the password before he modified it)
        }  
        
        var pyshellSendEmail = new PythonShell('send_email.py', {
            mode: 'text',
            scriptPath: constants.python_path +'/mail',
            args: [config.email,"Password Recovery","Dear " + config.first_name + " "  + config.last_name + ",<br/><br/>Your current Camera password is:<br/><pre>" + config.cam_pwd + "</pre><br/><a href='http://"+config.lan_ip+":"+constants.main_port+"/cam/update_cam_pwd'>Update your Camera password</a> now!<br/><br/>Thank you,<br/>The AMS Team"]
        });
            
        pyshellSendEmail.on('message', function (config) { 
             // Redirect to /cam/update_cam_pwd with success message
             read_config.load_page_with_conf_test_cam_pwd(res,'update_cam_pwd',{
                success: 'Email sent',
                config: config
             });
        });
        
    });
    
};



