var express     = require('express'),
    app         = express(),
    path        = require('path'),
    request     = require('request'),
    PythonShell = require('python-shell'),
    UAParser    = require('ua-parser-js'),
    constants   = require('./utils/constants'),
    utils       = require('./utils/browser'),
    bodyParser  = require('body-parser'),
    fs          = require('fs'),
    async       = require('async'),
    repeat      = require('repeat'); 

// Set default folder
app.use(express.static(__dirname + '/public'));

// Img & Videos folders
app.use('/py_img',express.static(path.join(__dirname + '/../../../var/www/html/out')));
app.use('/maybe',express.static(path.join(__dirname + '/../../../var/www/html/out/maybe')));
app.use('/false',express.static(path.join(__dirname + '/../../../var/www/html/out/false')));
app.use('/fireballs',express.static(path.join(__dirname + '/../../../var/www/html/out/fireballs')));
 
// Views
app.set('views', [
    path.join(__dirname + '/public/detections'),
    path.join(__dirname + '/public/home'),
    path.join(__dirname + '/public/cam'),
    path.join(__dirname + '/public'),
    '/var/www/html/out']
); 
app.set('view engine', 'ejs');


// Bower
app.use('/bower_components', express.static(__dirname + '/bower_components'));

// URLs 
app.use(bodyParser.urlencoded({
    extended: true
}));



/******************************************************************************************************************************************
* FUNCTIONS
***********************************************/

    // Test if the cam password has been setup (read the config_file)
    // if not, redirect to /cam/update_cam_pwd
    function test_cam_pwd(res,template,template_args) {
        
        var pyshellUpload = new PythonShell('read_config.py', {
            mode: 'json',
            scriptPath: constants.python_path +'/config'
        });
       
       return async.parallel([
           function() {
                pyshellUpload.on('message',  function (config) { 
                    if(typeof config.cam_pwd  == "undefined") {
                        res.redirect('/cam/update_cam_pwd');    
                        return true;
                    } else {
                        // Add the config to the template
                        template_args.config = config;
                        res.render(template,template_args);
                        return false;   
                    }
                })
           }
        ]);
           
        
    }
    
    // Test if the cam password has been setup (config passwed in arg)
    // if not, redirect to /cam/update_cam_pwd
    function test_cam_pwd_from_config(config,res,template,template_args) {
        if(typeof config.cam_pwd  == "undefined") {
            res.redirect('/cam/update_cam_pwd');    
            return false;
        } else {
            res.render(template,template_args);
            return true;   
        }
     }


/******************************************************************************************************************************************
* Home Page
***********************************************/
app.get('/', function(req, res) {
    
    // Test Browser
    browser = utils.get_browser(req)
    
    // Render
    test_cam_pwd(res,'home',{ browser:  browser});
     
});
   

/******************************************************************************************************************************************
* Read Log
***********************************************/
app.get('/cam/log', function(req, res) {
  
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

        var readConfig = new PythonShell('read_log.py', {
                mode: 'text' ,
                scriptPath: constants.python_path + "/log",
                args:[constants.cam_log_file]
        });
        
        readConfig.on('message', function (log_cont) {  
            test_cam_pwd(res,'log',{log_content:JSON.parse(log_cont)});
        });
    }
         
});


/*********************************************** 
* Add Log entry (from form)
***********************************************/
app.post('/cam/log', function(req, res) {
       
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
 });
 
 
/*********************************************** 
* Clean cam log
***********************************************/
app.get('/cam/log/clean', function(req, res) {
       
        var delLog = new PythonShell('del_log.py', {
            mode: 'text' ,
            scriptPath: constants.python_path + "/log",
            args:[constants.cam_log_file]
        });
        
        delLog.on('message', function () {  
              res.redirect('/cam/log');
        }); 
 });



/******************************************************************************************************************************************
* FOCUS HELPER
***********************************************/
app.get('/cam/focus_helper', function(req, res) {
    
     test_cam_pwd(res,'focus_helper',{});
    
});


/*********************************************** 
* START FOCUS HELPER
***********************************************/
app.post('/cam/focus_helper', function(req, res) {
  
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
        test_cam_pwd(res,'focus_helper',{'success':'Focus helper stopped on ' +   dt.toUTCString()});
    });
   
    
});



/******************************************************************************************************************************************
* Screenshot Page
***********************************************/
app.get('/cam/screenshot', function(req, res) {
    
    // If the cam password has already been updated:
    test_cam_pwd(res,'screenshot',{});
    
});


/**********************************************
* Take screenshot
***********************************************/
app.post('/cam/screenshot', function(req, resp) {
 
        var pyshellUpload = new PythonShell('upload_latest.py', {
            mode: 'json' ,
            scriptPath: constants.python_path+'/cam'
         });
        
        // JSON.stringify(message_success, null, '\t')
        pyshellUpload.on('message', function (message_success) { 
            if (message_success) {
                // Render
                return test_cam_pwd(resp,'screenshot',{  message_success: message_success});
             }        
        });
       
          
});




/******************************************************************************************************************************************
* PI RESTART 
***********************************************/
app.get('/pi/restart', function(req, res) {
     
    var opts = {  scriptPath: constants.python_pi_path  };
  
    browser = utils.get_browser(req)
      
    PythonShell.run('restart_pi.py', opts, function (err, ress) {
      if (err) throw err;
       res.redirect('/');
    });
     
});

/******************************************************************************************************************************************
* PI SHUTDOWN
***********************************************/
app.get('/pi/shutdown', function(req, res) {
     
    var opts = {  scriptPath: constants.python_pi_path  };
  
    browser = utils.get_browser(req)
      
    PythonShell.run('shutdown_pi.py', opts, function (err, ress) {
      if (err) throw err;
       res.redirect('/');
    });
     
});





/******************************************************************************************************************************************
* FORGET CAM PWD
***********************************************/
app.get('/cam/forget_cam_pwd', function(req, res) {
    
    var pyshellReadConfig = new PythonShell('read_config.py', {
            mode: 'json',
            scriptPath: constants.python_path +'/config'
    });
     
    // Read config
    pyshellReadConfig.on('message',  function (config) { 
        if(typeof config.cam_pwd == 'undefined') {
             config.cam_pwd = 'admin'; // Default (in the case the user ask to send the password before he modified it)
        }  
        
        var pyshellSendEmail = new PythonShell('send_email.py', {
            mode: 'text',
            scriptPath: constants.python_path +'/mail',
            args: [config.email,"Password Recovery","Dear " + config.first_name + " "  + config.last_name + ",<br/><br/>Your current Camera password is:<br/><pre>" + config.cam_pwd + "</pre><br/><a href='http://"+config.lan_ip+":"+constants.main_port+"/cam/update_cam_pwd'>Update your Camera password</a> now!<br/><br/>Thank you,<br/>The AMS Team"]
        });
            
        pyshellSendEmail.on('message', function (config) { 
             // Redirect to /cam/update_cam_pwd with success message
             test_cam_pwd(res,'update_cam_pwd',{
                success: 'Email sent',
                config: config
             });
        });
        
    });
    
});


/******************************************************************************************************************************************
* UPDATE CAM PWD
***********************************************/
app.get('/cam/update_cam_pwd', function(req, res) {
    
    var pyshellUpload = new PythonShell('read_config.py', {
            mode: 'json',
            scriptPath: constants.python_path +'/config'
    });
       
    // Read config
    pyshellUpload.on('message',  function (config) { 
          res.render('update_cam_pwd', {
             config: config
        })
    });
    
});


/**********************************************
* Update cam password
***********************************************/
app.post('/cam/update_cam_pwd', function(req, res) {
    
    var old_pwd     = req.body.oldPwd;
    var new_pwd     = req.body.newPwd;
    var new_pwd2    = req.body.newPwd2;
    var _error      = [];
    
    var pyshellReadConfig = new PythonShell('read_config.py', {
        mode: 'json',
        scriptPath: constants.python_path +'/config'
    });
    
    // Read config
    pyshellReadConfig.on('message',  function (config) { 
     
        // Test the old pwd 
        if(typeof config.cam_pwd !== 'undefined') {
            if(config.cam_pwd !== old_pwd) {
                _error.push('The old password is wrong. Please, try again.');
            }
        } else {
            if(old_pwd !== 'admin') {
                _error.push('The old password has never been updated. Please, try "admin".');
            }
        }
        
        // Test if new passwords match
        if(new_pwd !== new_pwd2) {
            _error.push('The 2 new passwords don\'t match. Please, try again.');
        }
         
        // Error
        if(_error.length !== 0 ) {
                     
            // We have an error: we redirect with the error message
            res.render('update_cam_pwd', {
                config : config,
                errors      : _error
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

    });
    
    
});



/******************************************************************************************************************************************
* Detection maybe
***********************************************/
app.get('/detection/maybe', function(req, res) {
    
    // Get all maybe detections
    var opts = {
        mode: 'json',
        args: ['/var/www/html/out/maybe/'],
        scriptPath: constants.python_path
    };
    
    // Test Browser
    browser = utils.get_browser(req)
      
    PythonShell.run('list_files.py', opts, function (err, ress) {
      if (err) throw err;
      
      // Render options
      opts_render = {
            results: ress,
            folder: '/maybe',
            browser: browser
      };
        
      if(typeof req.query.success !== "undefined") {
        opts_render.success = req.query.success.split("$");
      }
      
      test_cam_pwd(res,'maybe',opts_render);
    
    });
     
});


/**********************************************
* Detection maybe deletion (single)
***********************************************/
app.get('/detection/maybe/delete', function(req, res) {
    
    // Get select detection 
    var opts = { 
        mode: 'text',
        args: ['/var/www/html/out/maybe/',req.query.ev],
        scriptPath: constants.python_path+'/file_management'
    }; 
    
    PythonShell.run('delete_file.py', opts, function (err, ress) {
        if (err) throw err;
        res.redirect('/detection/maybe?success='+ress[0]);
    });
      
});


/**********************************************
* Detection maybe deletion (multiple)
***********************************************/
app.post('/detection/maybe/delete_multiple', function(req, res) {
   
    var opts = { 
        mode: 'text',
        args: ['/var/www/html/out/maybe/',req.body.events],
        scriptPath: constants.python_path+'/file_management'
    }; 
     
    PythonShell.run('delete_file.py', opts, function (err, ress) {
        if (err) throw err;
        res.redirect('/detection/maybe?success='+ress[0]);
    });
     
});



/******************************************************************************************************************************************
* Detection false
***********************************************/
app.get('/detection/false', function(req, res) {
    
    // Get all maybe detections
    var opts = {
        mode: 'json',
        args: ['/var/www/html/out/false/'],
        scriptPath: constants.python_path
    };
    
    // Test Browser
    browser = utils.get_browser(req)
      
    PythonShell.run('list_files.py', opts, function (err, ress) {
      if (err) throw err;
      
      // Render options
      opts_render = {
            results: ress,
            folder: '/false',
            browser: false
      };
        
      if(typeof req.query.success !== "undefined") {
        opts_render.success = req.query.success.split("$");
      }
           
      test_cam_pwd(res,'false',opts_render);    
       
    });
     
});


/**********************************************
* Detection false deletion (single)
***********************************************/
app.get('/detection/false/delete', function(req, res) {
    
    // Get select detection 
    var opts = { 
        mode: 'text',
        args: ['/var/www/html/out/false/',req.query.ev],
        scriptPath: constants.python_path+'/file_management'
    };
    
    PythonShell.run('delete_file.py', opts, function (err, ress) {
        if (err) throw err;
        res.redirect('/detection/false?success='+ress[0]);
    });
      
});


/**********************************************
* Detection false deletion (multiple)
***********************************************/
app.post('/detection/false/delete_multiple', function(req, res) {
   
    var opts = { 
        mode: 'text',
        args: ['/var/www/html/out/false/',req.body.events],
        scriptPath: constants.python_path+'/file_management'
    }; 
     
    PythonShell.run('delete_file.py', opts, function (err, ress) {
        if (err) throw err;
        res.redirect('/detection/false?success='+ress[0]);
    });
     
});

  
/******************************************************************************************************************************************
* Detection fireball
***********************************************/
app.get('/detection/fireballs', function(req, res) {
    
    // Get all maybe detections
    var opts = {
        mode: 'json',
        args: ['/var/www/html/out/fireballs/'] ,
        scriptPath: constants.python_path 

    };
    
    // Test Browser
    browser = utils.get_browser(req)
      
    PythonShell.run('list_files.py', opts, function (err, ress) {
      if (err) throw err;
      
      // Render options
      opts_render = {
            results: ress,
            folder: '/fireballs',
            browser: false
      };
        
      if(typeof req.query.success !== "undefined") {
        opts_render.success = req.query.success.split("$");
      }
       
      test_cam_pwd(res,'fireballs',opts_render);   
            
    });
     
});


/**********************************************
* Detection false deletion (single)
***********************************************/
app.get('/detection/fireballs/delete', function(req, res) {
    
    // Get select detection 
    var opts = { 
        mode: 'text',
        args: ['/var/www/html/out/fireballs/',req.query.ev],
        scriptPath: constants.python_path +'/file_management'
    }; 
    
    PythonShell.run('delete_file.py', opts, function (err, ress) {
        if (err) throw err;
        res.redirect('/detection/fireballs?success='+ress[0]);
    });
      
});


/**********************************************
* Detection false deletion (multiple)
***********************************************/
app.post('/detection/fireballs/delete_multiple', function(req, res) {
   
    var opts = { 
        mode: 'text',
        args: ['/var/www/html/out/fireballs/',req.body.events],
        scriptPath: constants.python_path +'/file_management'
    }; 
     
    PythonShell.run('delete_file.py', opts, function (err, ress) {
        if (err) throw err;
        res.redirect('/detection/fireballs?success='+ress[0]);
    });
     
});

 
app.listen(constants.main_port);