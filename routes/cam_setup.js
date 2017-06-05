var PythonShell     = require('python-shell');
var express         = require('express');
var router          = express.Router();

var read_config     = require('../utils/read_config');
var utils           = require('../utils/browser');
var constants       = require('../utils/constants');

/******************************************************************************************************************************************
* Cam Setup
***********************************************/
exports.load = function(req, res) {
    
    // Test Browser
    browser = utils.get_browser(req)
    
    var opts         = {scriptPath: constants.python_path + "/cam" };
    var render_opts  = {browser:  browser };
    
    /*
        NON-rotation: http://192.168.0.11/webs/btnSettingEx?flag=1000&paramchannel=0&paramcmd=1062&paramctrl=0&paramstep=0&paramreserved=0&UserID=87048223
        90 Roration: http://192.168.0.11/webs/btnSettingEx?flag=1000&paramchannel=0&paramcmd=1062&paramctrl=1&paramstep=0&paramreserved=0&UserID=42499318
        270 Roration: http://192.168.0.11/webs/btnSettingEx?flag=1000&paramchannel=0&paramcmd=1062&paramctrl=2&paramstep=0&paramreserved=0&UserID=52872181    
    */
    
    // We load the currently used param file (in the config)
    read_config.read_config(
            function(config) {
                 PythonShell.run('get_parameter_from_file.py', {scriptPath: constants.python_path + "/cam", args:[config.parameters] }, function (err, ress) {
                   if (err) throw err;
                   // Render 
                   read_config.load_page_with_conf_test_cam_pwd(res,'setup',{ browser:  browser, calib: JSON.parse(ress), active_file:config.parameters});
                 });
            }
    );
  
};