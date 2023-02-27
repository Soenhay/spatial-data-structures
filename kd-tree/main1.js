var figlet = require('figlet');
var fs = require('fs');
const csv = require('fast-csv');
var kdTree = require('kd-tree-javascript');//https://www.npmjs.com/package/kd-tree-javascript

const appConfig = require('./config/config.json');
const log4Js = require('log4js');
const log4JsConfig = require('./config/log4js.json');

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

/*
https://stackoverflow.com/questions/70477163/calculate-height-depth-of-binary-tree-javascript
https://stackabuse.com/javascript-check-if-variable-is-a-undefined-or-null/
*/
const treeHeight = function (tree) {
    return 1 + Math.max(
        tree.root != null ? treeHeight(tree.root) : -1,
        tree.left != null ? treeHeight(tree.left) : -1,
        tree.right != null ? treeHeight(tree.right) : -1
    );
}

const main = function () {
    // print process.argv
    process.argv.forEach(function (val, index, array) {
        console.log(index + ': ' + val);
    });

    //Init logging
    log4Js.configure(log4JsConfig);
    this.logger = log4Js.getLogger();

    //Display title
    this.logger.info('\r\n' + figlet.textSync(appConfig.appName));


    //Load data
    //X,Y,NAME,ST,POPULATION
    readCsvFileToObj("data/USA_Major_Cities_pop.csv", function (resultObj) {
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

        console.log(tree);
        console.log(`The balance factor: ${tree.balanceFactor()}`);
        console.log(`The height: ${treeHeight(tree)}`);
        console.log(`The min height:`);
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