var request = require('request'), 
    UAParser = require('ua-parser-js');


module.exports = {
    
  /**********************************************
  * Chrome or Firefox - detect browser
  ***********************************************/   
  get_browser: function (req) {
     var ua = req.headers['user-agent'];
     var parser = new UAParser();
     return parser.setUA(ua).getBrowser().name; 
  } 
}; 