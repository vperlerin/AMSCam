/********************************
* Encrypt / Decrypt
********************************/

var crypto = require('crypto'),
    algorithm = 'aes-256-ctr',
    password = 'allonsEnfants2laPatrie!';

// Ex: 
/* 
var hw = encrypt("hello world")
console.log(decrypt(hw));
*/
module.exports = {
    
  /**********************************************
  * Encrypt
  ***********************************************/   
  encrypt: function (text) {
      var cipher = crypto.createCipher(algorithm,password)
      var crypted = cipher.update(text,'utf8','hex')
      crypted += cipher.final('hex');
      return crypted;
  },
  
  /**********************************************
  * Dencrypt
  ***********************************************/   
  decrypt: function (text) {
      var decipher = crypto.createDecipher(algorithm,password)
      var dec = decipher.update(text,'hex','utf8')
      dec += decipher.final('utf8');
      return dec;
  }  
}; 