var figlet = require('figlet');
var fs = require('fs');
const csv = require('fast-csv');
var kdTree = require('./lib/myKdTree_1');

const appConfig = require('./config/config.json');
const log4Js = require('log4js');
const log4JsConfig = require('./config/log4js.json');

var path = require("path");

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
    const exists = fs.existsSync('./kd-tree/output');
    if (exists === true) {
        return;
    }
    fs.mkdirSync('./kd-tree/output')
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
    readCsvFileToObj("kd-tree/data/USA_Major_Cities_pop.csv", function (resultObj) {
        //console.log(resultObj);

        var points = resultObj;
        var dimensions = ["X", "Y", "NAME", "POPULATION"];
        var distance = function (a, b) {
            return Math.pow(a.x - b.x, 2) + Math.pow(a.y - b.y, 2);
        }

        //Init datastructure
        // Create a new tree from a list of points, a distance function, and a
        // list of dimensions.
        var tree = new kdTree.kdTree(points, distance, dimensions);

        var nearest = tree.nearest({ X: 5, Y: 5 }, 2);

        console.log(nearest);

        //console.log(tree);
        console.log(`The balance factor: ${tree.balanceFactor()}`);
        console.log(`The height: ${tree.treeHeight()}`);
        console.log(`The node count: ${tree.treeNodeCount()}`);//3886
        console.log(`The max height: ${tree.treeHeightMax()}`);
        console.log(`The min height: ${tree.treeHeightMin()}`);

        //Output the object to a json file:
        let jsonFn = 'kd-tree/output/myjsonfile.json';
        fs.writeFile(jsonFn, JSON.stringify(tree.toJSON()), 'utf8', function (err) {
            if (err != null) {
                console.log(err);
            }
            else {
                console.log(`JSON output saved to ${path.resolve(jsonFn)}`);
            }
        });

        //TODO: make a function to search for points in a range.
        tree.range([-102.7027, 27.20032, null, null], [-94.32688, 32.02732, null, null], function (idx) {
            console.log("visit:", idx)  //idx = index of point in points array
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