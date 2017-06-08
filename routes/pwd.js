var PythonShell     = require('python-shell');
var express         = require('express');
var router          = express.Router();

var read_config     = require('../utils/read_config');
var utils           = require('../utils/browser');
var constants       = require('../utils/constants');
var cookie          = require('../utils/cookie');
var crypt           = require('../utils/crypt');


/******************************************************************************************************************************************
* RESET PWD (GET)
***********************************************/
exports.reset_pwd =  function(req, res) {
    
     var tok_file_path = constants.APP_PATH + "tok.sec";
    
     // If no token or tok.sec doesnt exist: exit!
     // TODO: test if it's a token
     if(typeof req.params.token==='undefined' || !require('fs').existsSync(tok_file_path)) {
         res.redirect('/');
     }
       
     // Test token against the one in tok.sec
     require('fs').readFile(tok_file_path, "utf8", function (err,data) {
         if (err) {  return console.log(err);  }
         
         // We delete the tok.sec
         require('fs').unlinkSync(tok_file_path);
         
         if(data === crypt.encrypt(req.params.token.toString("utf8"))) {
            // THIS IS OK
            cookie.get_config_cookie_and_render(req, res,{}, 'reset_pwd');  

         } else {
            // THIS IS NOT OK
            cookie.get_config_cookie_and_render(req, res,{'fatal_error':'This link has expired. Please try again.'}, 'reset_pwd');  
         }
     });
    
}


/******************************************************************************************************************************************
* RESET PWD (POST)
***********************************************/
exports.reset_post_pwd =  function(req, res) {
    
     var tok_file_path = constants.APP_PATH + "tok.sec";
     var new_pwd     = req.body.newPwd;
     var new_pwd2    = req.body.newPwd2;
     var _error      = [];
     
     // We delete the tok.sec if necessary
     if(require('fs').existsSync(tok_file_path)) {
         require('fs').unlinkSync(tok_file_path);
     }
       
     // Test password
     if(new_pwd.trim() == '') {
            _error.push('Please, enter a valid password.');
     }
       
     // Test if new passwords match
     if(new_pwd !== new_pwd2) {
            _error.push('The 2 new passwords don\'t match.');
     }
        
     // Test if new passwords != admin
     if(new_pwd === 'admin') {
            _error.push('For security reasons, "admin" is forbidden as the camera password. ');
     }  
     
   
     if(_error.length !== 0 ) {
        // Error
        cookie.get_config_cookie_and_render(req, res,{errors : _error}, 'reset_pwd');       
     } else {
         
        // We get the cookie values
        var cookie_config = req.cookies.config;  
        
        // Send warning new password
        cookie_config.new_cam_pwd = new_pwd; 
         
        // We update the password    
        var updateConfig = new PythonShell('update_config.py', {
            mode: 'json',
            scriptPath: constants.python_path+'/config',
            args:[JSON.stringify(cookie_config)]
        });
                      
        updateConfig.on('message',  function (config_write_res) { 
            // We clear the config cookie so it re-read from config.txt
            res.clearCookie("config",{path:'/'});  
                   
            // THIS IS OK
            cookie.get_config_cookie_and_render(req, res,{ success : "Password updated."}, 'reset_pwd');         
           
        }); 
     }
    
}



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
 exports.update_pwd =  function(req, res) {
    
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
                    
                    // We clear the config cookie so it re-read from config.txt
                    res.clearCookie("config",{path:'/'});  
                 
                    var updateConfig = new PythonShell('update_config.py', {
                        mode: 'json',
                        scriptPath: constants.python_path+'/config',
                        args:[JSON.stringify(config)]
                    });
                      
                    redirected = true;
                      
                    updateConfig.on('message',  function (config_write_res) { 
                         return res.redirect('/?success=Thank you for updating your camera password. Enjoy!');    
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
                              // We clear the config cookie so it re-read from config.txt
                              res.clearCookie("config",{path:'/'});  
                              
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
* FORGET PWD (send email)
***********************************************/
exports.forget_pwd =  function(req, res) {
       
    // Generate a random code
    require('crypto').randomBytes(8, function(err, buffer) {
      var token = buffer.toString('hex');
      
      // Write the token in tok.sec file
      require('fs').writeFile(constants.APP_PATH +"tok.sec", crypt.encrypt(token),  { flag: 'w' }, function(err) {
            if(err) { return console.log(err); }
            
            console.log('TOK.SEC CREATED');
            
            var pyshellReadConfig = new PythonShell('read_config.py', {
                mode: 'json',
                scriptPath: constants.python_path +'/config',
                argv: ['json']
            });
        
            // Send an email with the code
            // Read config
            pyshellReadConfig.on('message',  function (config) { 
                if(typeof config.cam_pwd === 'undefined') {
                     config.cam_pwd = 'admin'; // Default (in the case the user ask to send the password before he modified it)
                }  
                
                var pyshellSendEmail = new PythonShell('send_email.py', {
                    mode: 'text',
                    scriptPath: constants.python_path +'/mail',
                    args: [config.email,"Reset Password","Dear " + config.first_name + " "  + config.last_name + ",<br/><br/>Please, click the following link to reset your password:<br/><a href='http://"+config.lan_ip+":"+constants.main_port+"/pwd/reset_pwd/" + token + "'><b>Reset your password</b></a><br/><br/>Or copy and past the following link on your browser:<br/> http://"+config.lan_ip+":"+constants.main_port+"/pwd/reset_pwd/" + token + "<br/><br/><br/>Thank you,<br/>The AMS Team"]
                });
                    
                backURL=req.header('Referer') || '/';    
                    
                pyshellSendEmail.on('message', function (config) { 
                     cookie.get_config_cookie_and_render(req, res, {backURL:backURL}, 'email_sent_pwd');  
                });
                
            }); 
      }); 
      
    }); 
    
};
