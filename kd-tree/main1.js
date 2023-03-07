var figlet = require('figlet');
var fs = require('fs');
const csv = require('fast-csv');
var kdTree = require('./lib/myKdTree_1');

const appConfig = require('./config/config.json');
const log4Js = require('log4js');
const log4JsConfig = require('./config/log4js.json');

var path = require("path");

var inputPathAndFn = path.resolve("data/USA_Major_Cities_pop.csv");
var outputPath = path.resolve("output");


// console.log(inputPathAndFn)
// console.log(outputPath)

const readCsvFileToObj = function (fn, callback) {
    //https://stackoverflow.com/questions/59299172/how-to-read-a-csv-file-and-store-it-in-and-array-of-objects
    let results = [];
    fs.createReadStream(fn)
        .pipe(csv.parse({ headers: true }))
        .on('error', error => console.error(error))
        .on('data', (data) => {
            results.push(data);
        })
        .on('end', (rowCount) => {
            console.log(`Parsed ${rowCount} rows from ${fn}`);
            callback(results);
        });
}

function initializeOutputDirectory() {
    const exists = fs.existsSync(outputPath);
    if (exists === true) {
        return;
    }
    fs.mkdirSync(outputPath);
}

function outputJsonFile(fn, jsonObj) {
    let jsonFn = path.resolve(outputPath, fn);
    fs.writeFile(jsonFn, JSON.stringify(jsonObj), 'utf8', function (err) {
        if (err != null) {
            this.logger.info(err);
        }
        else {
            this.logger.info(`JSON output saved to ${jsonFn}`);
        }
    });
}

const main = function () {
    // print process.argv
    process.argv.forEach(function (val, index, array) {
        console.log(index + ': ' + val);
    });

    //Init logging
    log4Js.configure(log4JsConfig);
    this.logger = log4Js.getLogger();

    //Init output dir
    initializeOutputDirectory();

    //Display title
    this.logger.info('\r\n' + figlet.textSync(appConfig.appName));


    //Load data
    //X,Y,NAME,ST,POPULATION
    readCsvFileToObj(inputPathAndFn, function (resultObj) {
        //this.logger.info(resultObj);

        var points = resultObj;
        var dimensions = ["X", "Y", "NAME", "POPULATION"];
        var distance = function (a, b) {
            return Math.pow(a.x - b.x, 2) + Math.pow(a.y - b.y, 2);
        }

        //Init datastructure
        // Create a new tree from a list of points, a distance function, and a
        // list of dimensions.
        var tree = new kdTree.kdTree(points, distance, dimensions);
        tree.logger = this.logger;
        tree.dimensions = dimensions;

        // var nearest = tree.nearest({ X: 5, Y: 5 }, 2);
        // this.logger.info(nearest);

        //this.logger.info(tree);
        this.logger.info(`The balance factor: ${tree.balanceFactor()}`);
        this.logger.info(`The height: ${tree.treeHeight()}`);
        this.logger.info(`The node count: ${tree.treeNodeCount()}`);//3886
        this.logger.info(`The max height: ${tree.treeHeightMax()}`);
        this.logger.info(`The min height: ${tree.treeHeightMin()}`);

        //Output the object to a json file:
        outputJsonFile("myJsonOutput.json", tree.toJSON());


        tree.range([-102.7027, 27.20032, null, null], [-94.32688, 32.02732, null, null], function (lo, hi, pointsInRange) {
            this.logger.info(`The range lo:${lo}, hi:${hi} has (${pointsInRange.length}) points.`);
            outputJsonFile("data1.json", pointsInRange);
        });

        tree.range([-102.7027, 27.20032, 'C', null], [-94.32688, 32.02732, 'H', null], function (lo, hi, pointsInRange) {
            this.logger.info(`The range lo:${lo}, hi:${hi} has (${pointsInRange.length}) points.`);
            outputJsonFile("data2.json", pointsInRange);
        });

        tree.range([-102.7027, 27.20032, 'C', 50000], [-94.32688, 32.02732, 'H', 500000], function (lo, hi, pointsInRange) {
            this.logger.info(`The range lo:${lo}, hi:${hi} has (${pointsInRange.length}) points.`);
            outputJsonFile("data3.json", pointsInRange);
        });
    });
};

main();


/*
    // Query the nearest *count* neighbours to a point, with an optional
    // maximal search distance.
    // Result is an array with *count* elements.
    // Each element is an array with two components: the searched point and
    // the distance to it.
    tree.nearest(point, count, [maxDistance]);
 
    // Insert a new point into the tree. Must be consistent with previous
    // contents.
    tree.insert(point);
 
    // Remove a point from the tree by reference.
    tree.remove(point);
 
    // Get an approximation of how unbalanced the tree is.
    // The higher this number, the worse query performance will be.
    // It indicates how many times worse it is than the optimal tree.
    // Minimum is 1. Unreliable for small trees.
    tree.balanceFactor();


    MISC notes:
    https://www.geeksforgeeks.org/find-minimum-in-k-dimensional-tree/

    */