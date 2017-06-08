/********************************
* Define the App Contants
********************************/
var path = require('path');

function define(name, value) {
    Object.defineProperty(exports, name, {
        value:      value,
        enumerable: true
    });
}

define("python_path", path.join('/'+__dirname + './../../fireball_camera/'));
define("python_pi_path", path.join('/'+__dirname + '/../../fireball_camera/pi/'));
define("config_file", path.join('/'+__dirname + '/../../fireball_camera/config.txt'));
define("cam_log_file", "cam_log");
define("main_port",3000);
define("DETECTION_PER_PAGE",30);
define("possible_parameters_files",['Night','Day','Calibration']);
// Cookie as a 15 min period of life because it's the period for the cron job to eventually update the parameters of the cam (switch between Night and Day)
// define("config_cookie_maxAge",15 * 60 * 1000);  
// Well... it's a pain so...
define("config_cookie_maxAge",365 * 24 * 60 * 1000); 
define("APP_PATH","/home/pi/AMSCam/");