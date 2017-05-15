var path = require('path');

function define(name, value) {
    Object.defineProperty(exports, name, {
        value:      value,
        enumerable: true
    });
}

define("python_path", path.join('/'+__dirname + '/../fireball_camera/'));
define("python_pi_path", path.join('/'+__dirname + '/../fireball_camera/pi/'));