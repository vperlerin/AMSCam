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
var methodOverride  = require('method-override');

// Security
var passport = require('passport');
var LocalStrategy = require('passport-local').Strategy;
var ensureLoggedIn = require('connect-ensure-login').ensureLoggedIn;
 
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
app.use('/img',express.static(path.join(__dirname + '/public/img')));
app.use('/manifest',express.static(path.join(__dirname + '/views')));
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
var cam_pwd         = require('./routes/cam_pwd'); 
var detections      = require('./routes/detections'); 
var pi              = require('./routes/pi'); 


/******************************************************************************************************************************************
* LOGIN 
***********************************************/

// Configure the local strategy for use by Passport.
passport.use(new LocalStrategy(
  
    function(username, password, cb) {
      
        read_config.read_config(
            function(config) {
                if(config.cam_pwd==password) {
                    console.log('PWD OK');
                    cb(null, { user: { username:'admin', password:password} });
                } else {
                    console.log('PWD NOT OK');
                    cb(null, false);
                }
            }
        );   
})); 

// Configure Passport authenticated session persistence.
passport.serializeUser(function(user, cb) {
   cb(null, user);
});

passport.deserializeUser(function(user, cb) {
  cb(null, user);
});


// Passport config
app.use(require('cookie-parser')());
app.use(require('body-parser').urlencoded({ extended: true }));
app.use(require('express-session')({
  secret: 'Allons Enfants 2 la Patrie',
  resave: true,
  saveUninitialized: true
}));
app.use(passport.initialize());
app.use(passport.session());
 
 
app.get('/login',
  function(req, res){
    res.render('login');
  });
  
app.post('/login', 
  passport.authenticate('local', { failureRedirect: '/login', successRedirect: '/' }),
  function(req, res) {
     res.redirect('/');
});
 
app.get('/logout', function(req, res){
  req.logout();
  res.redirect('/');  
});


/******************************************************************************************************************************************
* ROUTES
***********************************************/

// Home
app.use('/',ensureLoggedIn('/login'), index);

// Cam Log
app.get('/cam/log',ensureLoggedIn('/login'), logg.load);
app.post('/cam/log',ensureLoggedIn('/login'), logg.add);
app.get('/cam/log/clean',ensureLoggedIn('/login'), logg.clean);

// Focus Helper
app.get('/cam/focus_helper',ensureLoggedIn('/login'), focus_helper.load);
app.post('/cam/focus_helper',ensureLoggedIn('/login'), focus_helper.start);

// Cam Restart & Parameters
app.get('/cam/restart',ensureLoggedIn('/login'), cam_calib.restart);
app.get('/cam/parameters/:file',ensureLoggedIn('/login'), cam_calib.load);
app.get('/cam/parameters',ensureLoggedIn('/login'), cam_calib.load);
app.post('/cam/parameters',ensureLoggedIn('/login'), cam_calib.post); // Ajax Call
app.get('/cam/load_parameters',ensureLoggedIn('/login'), cam_calib.load_auto_param); // Ajax Call

// Cam Screenshot
app.get('/cam/screenshot',ensureLoggedIn('/login'), cam_scr.load);
app.post('/cam/screenshot',ensureLoggedIn('/login'), cam_scr.update);  

// Cam Setup
app.get('/cam/setup',ensureLoggedIn('/login'), cam_setup.load);

// Cam Password
app.get('/cam/forget_cam_pwd',ensureLoggedIn('/login'), cam_pwd.forget_cam_pwd);
app.get('/cam/update_cam_pwd',ensureLoggedIn('/login'), cam_pwd.load);
app.post('/cam/update_cam_pwd',ensureLoggedIn('/login'), cam_pwd.update_cam_pwd);

// Detections
app.get('/detection/:type',ensureLoggedIn('/login'), detections.load);
app.get('/detection/:type/delete/:ev',ensureLoggedIn('/login'), detections.delete_single_detect);
app.post('/detection/:type/delete_multiple/',ensureLoggedIn('/login'), detections.delete_multiple_detect);
app.get('/detection/:type/delete_all/',ensureLoggedIn('/login'),detections.delete_all_detect);

// PI
app.get('/pi/shutdown',ensureLoggedIn('/login'), pi.shutdown);
app.get('/pi/restart',ensureLoggedIn('/login'), pi.restart);



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








 
app.listen(constants.main_port);
console.log('Listening on port 3000 - the AMSCam App is running.'); 