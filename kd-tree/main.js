var figlet = require('figlet');

const appConfig = require('./config/config.json');
const log4Js = require('log4js');
const log4JsConfig = require('./config/log4js.json');


const main = function(){
    // print process.argv
    process.argv.forEach(function (val, index, array) {
        console.log(index + ': ' + val);
    });

    //Init logging
    log4Js.configure(log4JsConfig);
    this.logger = log4Js.getLogger();

    //Display title
    this.logger.info('\r\n' + figlet.textSync(appConfig.appName));



};

main();
