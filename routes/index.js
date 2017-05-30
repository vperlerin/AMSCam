var express = require('express');
var router  = express.Router();
 
var utils = require('../utils/browser');
var cam_capture = require('../utils/capture_test');

/******************************************************************************************************************************************
* Home Page
***********************************************/
router.get('/', function(req, res) {
     
    // Test Browser
    var opts = {};
    opts.browser = utils.get_browser(req)
    
    if(typeof req.query.msg != 'undefined') {
        opts.msg =   req.query.msg 
    }
     // Render
    cam_capture.test_capture_running(res,'home',opts);
     
});

module.exports = router;