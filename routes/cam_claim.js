var PythonShell     = require('python-shell');
var express         = require('express');
var router          = express.Router();

var read_config     = require('../utils/read_config');
var utils           = require('../utils/browser');
var constants       = require('../utils/constants');
var cookie          = require('../utils/cookie');
 

// Default (first claim)
exports.load =  function(req, res) { 

        // Update the config file from the API and update the cookie accordlingly
        read_config.read_config_from_api(function(config) {
             
            res.cookie('config', config, {path:'/', maxAge: constants.config_cookie_maxAge});
   
            // The guy shouldn't be here if the cam has already been claimed
            if(typeof config.user_id!=="undefined" && typeof config.api_key!=="undefined") {
                res.redirect('/');
            } else {
                var url        = req.headers.host;
                res.clearCookie("config",{path:'/'});
                cookie.get_config_cookie_and_render(req, res, {url:url}, 'claim');  
            }
                   
        }); 
  
   
}