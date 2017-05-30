var constants       = require('../utils/constants');
var read_config       = require('read_config');

function define(name, value) {
    Object.defineProperty(exports, name, {
        value:      value,
        enumerable: true
    });
}


// Test if the capture is running
define("test_capture_running", function(res,template,opts) {
    child_process.exec(constants.python_path +  'simple-capture-status.sh', function(error, stdout, stderr){
        opts.capture = stdout;   
        read_config.test_cam_pwd(res,template,opts); 
    });
});