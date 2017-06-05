// Modules
var express         = require('express');
var app             = express();
var path            = require('path');
var request         = require('request');
var PythonShell     = require('python-shell');
var bodyParser      = require('body-parser');
var fs              = require('fs');

var minifyHTML      = require('express-minify-html');
var favicon         = require('serve-favicon');
var logger          = require('morgan'); 
var methodOverride = require('method-override');

// Custom Scripts
var read_config     = require('./utils/read_config');
var utils           = require('./utils/browser');
var constants       = require('./utils/constants');
var cam_capture     = require('./utils/capture_test');


// Set public folder
app.use(express.static(__dirname + '/public'));

// Routes
app.use('/py_img',express.static(path.join(__dirname + '/../../../var/www/html/out')));
app.use('/maybe',express.static(path.join(__dirname + '/../../../var/www/html/out/maybe')));
app.use('/false',express.static(path.join(__dirname + '/../../../var/www/html/out/false')));
app.use('/fireballs',express.static(path.join(__dirname + '/../../../var/www/html/out/fireballs')));
app.use('/js',express.static(path.join(__dirname + '/public/js')));
app.use('/pnacl',express.static(path.join(__dirname + '/views/pnacl'))); // RSTP Viewer

// Logger
app.use(logger('dev'));  


 
// Compress HTML
app.use(minifyHTML({
    override:      true,
    exception_url: false,
    htmlMinifier: {
        removeComments:            true,
        collapseWhitespace:        true,
        collapseBooleanAttributes: true,
        removeAttributeQuotes:     true,
        removeEmptyAttributes:     true,
        minifyJS:                  true
    }
}));

// Views
app.set('views', [
    path.join(__dirname + '/views/detections'),
    path.join(__dirname + '/views/home'),
    path.join(__dirname + '/views/cam'),
    path.join(__dirname + '/views'),  
    '/var/www/html/out']
); 
app.set('view engine', 'ejs');
 
// Favicon
app.use(favicon(__dirname + '/public/img/favicon.png'));

// Bower & Nodes
app.use('/bower_components', express.static(__dirname + '/bower_components')); 
app.use('/node_modules', express.static(__dirname + '/node_modules'));

// URLs 
app.use(bodyParser.urlencoded({
    extended: true
}));

app.use(methodOverride('_method'));

// development error handler
// will print stacktrace
if (app.get('env') === 'development') {
    app.use(function(err, req, res, next) {
        res.status(err.status || 500);
        res.render('error', {
            message: err.message,
            error: err
        });
    });
}

// production error handler
// no stacktraces leaked to user
app.use(function(err, req, res, next) {
    res.status(err.status || 500);
    res.render('error', {
        message: err.message,
        error: {}
    });
});

module.exports = app;

// Routes
var index           = require('./routes/index'); 
var logg            = require('./routes/cam_log'); 
var focus_helper    = require('./routes/focus_helper'); 
var cam_calib       = require('./routes/cam_calib'); 
var cam_scr         = require('./routes/cam_screenshot'); 
var cam_setup       = require('./routes/cam_setup'); 
var detections      = require('./routes/detections'); 


// Home
app.use('/', index);

// Cam Log
app.get('/cam/log', logg.load);
app.post('/cam/log', logg.add);
app.get('/cam/log/clean', logg.clean);

// Focus Helper
app.get('/cam/focus_helper', focus_helper.load);
app.post('/cam/focus_helper', focus_helper.start);

// Cam Restart & Parameters
app.get('/cam/restart', cam_calib.restart);
app.get('/cam/parameters', cam_calib.load);
app.post('/cam/parameters', cam_calib.post); // Ajax Call
app.get('/cam/load_parameters', cam_calib.load_auto_param); // Ajax Call

// Cam Screenshot
app.get('/cam/screenshot', cam_scr.load);
app.post('/cam/screenshot', cam_scr.update);  

// Cam Setup
app.get('/cam/setup', cam_setup.load);

// Detections
app.get('/detection/:type', detections.load);
app.get('/detection/:type/delete/:ev', detections.delete_single_detect);
app.post('/detection/:type/delete_multiple/', detections.delete_multiple_detect);

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
            scriptPath: constants.python_path +'/config',
            argv: ['json']
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
             read_config.load_page_with_conf_test_cam_pwd(res,'update_cam_pwd',{
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
        scriptPath: constants.python_path +'/config',
        argv: ['json']
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
        
        // Test if new passwords != admin
        if(new_pwd === 'admin') {
            _error.push('For security reasons, "admin" is forbidden as the camera password. Please, enter a new password.');
        }
         
        // Error
        if(_error.length !== 0 ) {
                     
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

    });
    
    
});




 
app.listen(constants.main_port);
console.log('Listening on port 3000 - the AMSCam App is running.'); 