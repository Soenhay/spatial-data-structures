var figlet = require('figlet');
var fs = require('fs');
const csv = require('fast-csv');
var kdTree = require('static-kdtree');//https://www.npmjs.com/package/static-kdtree

const appConfig = require('./config/config.json');
const log4Js = require('log4js');
const log4JsConfig = require('./config/log4js.json');

const readCsvFileToObj = function (fn, getDataRow, callbackEnd) {
    //https://stackoverflow.com/questions/59299172/how-to-read-a-csv-file-and-store-it-in-and-array-of-objects
    let results = [];
    fs.createReadStream(fn)
        .pipe(csv.parse({ headers: true }))
        .on('error', error => console.error(error))
        .on('data', (data) => {
            results.push(getDataRow(data));
        })
        .on('end', (rowCount) => {
            console.log(`Parsed ${rowCount} rows from ${fn}`);
            callbackEnd(results);
        });
}

/*
https://stackoverflow.com/questions/70477163/calculate-height-depth-of-binary-tree-javascript
https://stackabuse.com/javascript-check-if-variable-is-a-undefined-or-null/
*/
const treeHeight = function (tree) {
    //Doesn't work for this library.
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
    var dimensions = ["X", "Y", "NAME", "POPULATION"];
    readCsvFileToObj("data/USA_Major_Cities_pop.csv", 
    function(data){
        return [data[dimensions[0]],data[dimensions[1]],data[dimensions[2]],data[dimensions[3]]];
    },
    function (resultObj) {
        //console.log(resultObj);

        var points = resultObj;
        var distance = function (a, b) {
            return Math.pow(a.x - b.x, 2) + Math.pow(a.y - b.y, 2);
        }

        //Init datastructure
        var tree = new kdTree(points);//Doesn't seem work with string values.

        console.log(tree);
        //console.log(`The height: ${treeHeight(tree)}`);//Doesn't work.
        //console.log(`The min height:`);

        tree.range([-102.7027,27.20032,null,null], [-94.32688,32.02732,null,null], function(idx) {
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