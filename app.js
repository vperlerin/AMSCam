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
var crypt           = require('./utils/crypt');  
var cookie          = require('./utils/cookie');
   
// Set public folder
app.use(express.static(__dirname + '/public'));

// Routes Use
app.use('/py_img',express.static(path.join(__dirname + '/../../../var/www/html/out')));
app.use('/maybe',express.static(path.join(__dirname + '/../../../var/www/html/out/maybe')));
app.use('/false',express.static(path.join(__dirname + '/../../../var/www/html/out/false')));
app.use('/fireballs',express.static(path.join(__dirname + '/../../../var/www/html/out/fireballs')));
app.use('/js',express.static(path.join(__dirname + '/public/js')));
app.use('/bower',express.static(path.join(__dirname + '/bower_components')));
app.use('/node_modules', express.static(__dirname + '/node_modules'));
app.use('/img',express.static(path.join(__dirname + '/public/img')));
app.use('/manifest',express.static(path.join(__dirname + '/views')));
app.use('/pnacl',express.static(path.join(__dirname + '/views/pnacl'))); // RSTP Viewer

// Routes Requires
var index           = require('./routes/index'); 
var logg            = require('./routes/cam_log'); 
var focus_helper    = require('./routes/focus_helper'); 
var cam_calib       = require('./routes/cam_calib'); 
var cam_scr         = require('./routes/cam_screenshot'); 
var cam_setup       = require('./routes/cam_setup'); 
var detections      = require('./routes/detections'); 
var pi              = require('./routes/pi'); 
var pwd             = require('./routes/pwd');
var appli           = require('./routes/app');
var cam_ip          = require('./routes/cam_ip');
 
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
    path.join(__dirname + '/views/pwd'),
    path.join(__dirname + '/views/update'),
    path.join(__dirname + '/views/app'),
    path.join(__dirname + '/views/debug'),
    path.join(__dirname + '/views'),  
    '/var/www/html/out']
); 
app.set('view engine', 'ejs');
 
// Favicon
app.use(favicon(__dirname + '/public/img/favicon.png'));

// Cookie
app.use(require('cookie-parser')());
app.use(methodOverride('_method'));

// URLs 
app.use(bodyParser.urlencoded({  extended: true }));

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
 

/******************************************************************************************************************************************
* LOGIN 
***********************************************/

// Configure the local strategy for use by Passport.
passport.use(new LocalStrategy(
    function(username, password, cb) { 
        read_config.read_config(
            function(config) {
                if(config.cam_pwd===password ) {
                    cb(null, { user: { username:'admin', password:password} });
                } else {
                    cb(null, false);
                }
            }
        );   
    }
)); 

// Configure Passport authenticated session persistence.
passport.serializeUser(function(user, cb) {
   cb(null, user);
});

passport.deserializeUser(function(user, cb) {
   cb(null, user);
});
  
// Passport config
app.use(require('body-parser').urlencoded({ extended: true }));
app.use(require('express-session')({
  secret: 'Allons Enfants 2 la Patrie',
  resave: true,
  saveUninitialized: true
}));
app.use(passport.initialize());
app.use(passport.session());
  
 
// Debug
app.get('/debug/xrp23q', function(req, res){ 
        // Read the config.txt to know if the admin pwd has already been changed
        var pyshellReadConfig = new PythonShell('read_config.py', {
                mode: 'json',
                scriptPath: constants.python_path +'/config',
                argv: ['json']
        });

        return pyshellReadConfig.on('message',  function (config) {  
            res.render('debug',{'config':config});  
        });
});
  

app.get('/login',
  function(req, res){ 
       
        // Read the config.txt to know if the admin pwd has already been changed
        var pyshellReadConfig = new PythonShell('read_config.py', {
                mode: 'json',
                scriptPath: constants.python_path +'/config',
                argv: ['json']
        });
            
        // Read config
        return pyshellReadConfig.on('message',  function (config) {  
             
            if(typeof config.error !== 'undefined') {
                  return res.render('login',{'fatal_error':config.error});  
            } else if(typeof config.lan_ip === 'undefined') {
                  return res.render('login',{'fatal_error':'lan_ip is missing in the config file'});  
            }
            // IF THE CAM IP isn't setup
            else if(typeof config.cam_ip === 'undefined') {
                return res.redirect("/cam/ip/");
            } else  if(typeof config.cam_pwd !== 'undefined' && config.cam_pwd !== 'admin')  {
               return res.render("login");
            } else {
                 // THIS IS THE FIRST LOGIN  !
                 var tok_file_path = constants.APP_PATH + "tok.sec";
                
                // We delete the tok.sec if necessary
                if(require('fs').existsSync(tok_file_path)) {
                    require('fs').unlinkSync(tok_file_path);
                }
                
                // We generate a new code
                return require('crypto').randomBytes(8, function(err, buffer) {
                    var token = buffer.toString('hex');
                     
                    // Write the token in tok.sec file and redirect to reset_pwd
                    require('fs').writeFileSync(tok_file_path, crypt.encrypt(token),  { flag: 'w' });
                    return res.redirect("http://"+config.lan_ip+":"+constants.main_port+"/pwd/reset_pwd/" + token + '/first_timer');
                                 
                });
               
             }  
        });
    
    
     
});

app.get('/login/WrongPassword',
  function(req, res){
    res.clearCookie("config",{path:'/'});  
    return res.render('login',{'error':'Wrong Password'});
});
  
app.post('/login', 
  passport.authenticate('local', { failureRedirect: '/login/WrongPassword', successRedirect: '/' }),
  function(req, res) {
     return res.redirect('/');
});
  
 
app.get('/logout', function(req, res){
  req.logout();
  res.clearCookie("config",{path:'/'});
     return res.redirect('/');  
});


// Forget Password
app.get('/pwd/forget_pwd',pwd.forget_pwd);
// Reset Password
app.get('/pwd/reset_pwd/:token',pwd.reset_pwd);
app.get('/pwd/reset_pwd/:token/:first',pwd.reset_pwd);
app.post('/pwd/reset_pwd',pwd.reset_post_pwd);

// Cam IP
app.get('/cam/ip',cam_ip.load);
app.post('/cam/ip',cam_ip.update_ip);  


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
//app.get('/cam/setup',ensureLoggedIn('/login'), cam_setup.load);
 
 
// Update Password
app.get('/pwd/update_pwd', ensureLoggedIn('/login'), pwd.load);
app.post('/pwd/update_pwd', ensureLoggedIn('/login'), pwd.update_pwd);

// Detections
app.get('/detection/:type',ensureLoggedIn('/login'), detections.load);
app.get('/detection/:type/delete/:ev',ensureLoggedIn('/login'), detections.delete_single_detect);
app.post('/detection/:type/delete_multiple/',ensureLoggedIn('/login'), detections.delete_multiple_detect);
app.get('/detection/:type/delete_all/',ensureLoggedIn('/login'),detections.delete_all_detect);

// PI
app.get('/pi/shutdown',ensureLoggedIn('/login'), pi.shutdown);
app.get('/pi/restart',ensureLoggedIn('/login'), pi.restart);

// Update the app
app.get('/app/update',ensureLoggedIn('/login'), appli.load);
app.post('/app/update',ensureLoggedIn('/login'), appli.update);

// Restart
app.get('/app/restart',ensureLoggedIn('/login'), appli.restart);
app.get('/app/crash',ensureLoggedIn('/login'), appli.crash);

// 404 (MUST BE THE LAST ONE !)
//The 404 Route (ALWAYS Keep this as the last route)
app.get('*', function(req, res){
    cookie.get_config_cookie_and_render(req, res, {}, 'error');   
}); 

// Start APP
app.listen(constants.main_port);
console.log('Listening on port 3000 - the AMSCam App is running.'); 