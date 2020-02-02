var express = require('express');
var router = express.Router();
var fs = require('fs');

console.log()

/* GET home page. */
router.get('/', function(req, res, next) {
    res.render('index', {})
});

router.get('/aas', function(req, res, next) {
    var date = req.originalUrl.replace('/', '');
    var logdir = fs.readFileSync(require('path').join(__dirname,'..\\location.txt'), "utf8");

    logdir = logdir.replace(/(\r\n|\n|\r|\s)/gm, "");
    console.log("\"" + logdir + "\"")
    console.log("\"" + date + "\"")
    
    contents = fs.readFileSync(logdir + date + '.json', 'utf8');
    
    contents = contents.split('\n');
    // -1 fordi der altid er et tomt \n
    for(var i = 0; i < contents.length - 1; i++) {
        console.log(contents[i]);
        contents[i] = JSON.parse(contents[i]);
    }
    // Fjern det tomme element
    contents.pop();
    
    console.log(contents);

    data = JSON.stringify(contents)

    res.render('statDate', { date: date, data: data });
});

module.exports = router;
