var express = require('express');
var router  = express.Router();
  
var utils   = require('../utils/browser');
var cookie  = require('../utils/cookie');

/******************************************************************************************************************************************
* Home Page
* router.get('/', isAuthenticated,  function(req, res) {
***********************************************/
router.get('/', function(req, res) {
 
    // Test Browser
    var opts = {};
    opts.browser = utils.get_browser(req)
    
    // Eventual Msg
    if(typeof req.query.msg != 'undefined') {
        opts.msg = req.query.msg 
    }
    
    return cookie.get_config_cookie_and_render(req, res, opts, 'home');
      
});

module.exports = router;