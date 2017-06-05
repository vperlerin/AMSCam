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