
var kdTree = require('kd-tree-javascript');//https://www.npmjs.com/package/kd-tree-javascript

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

kdTree.kdTree.prototype.treeHeight = function () {
    return treeHeight(this);
}

const treeNodeCount = function (tree) {
    return tree != null ? (1
    + (tree.left != null ? treeNodeCount(tree.left) : 0)
    + (tree.right != null ? treeNodeCount(tree.right): 0)) : 0;
}

kdTree.kdTree.prototype.treeNodeCount = function () {
    return treeNodeCount(this.root);
}

kdTree.kdTree.prototype.treeHeightMax = function () {
    //n-1
    return treeNodeCount(this.root) - 1;
}

kdTree.kdTree.prototype.treeHeightMin = function () {
    //floor(log2n)
    return Math.log2(treeNodeCount(this.root));
}

const getDimensionVal = function(dimensions, tree){
    return tree.obj[dimensions[tree.dimension]];
}

const treeRange = function(lo, hi, tree, dimensions)
{
    let pointsInRange = [];
    let currDimVal = getDimensionVal(dimensions, tree);
    
    //Check this node.
    if(lo[tree.dimension] <= currDimVal && currDimVal <= hi[tree.dimension]){
        pointsInRange.push(tree.obj);
    }
    //Check left subtree.
    if(tree.left != null){
        let leftDimVal = getDimensionVal(dimensions, tree.left);
        if(lo[tree.left.dimension] <= leftDimVal || lo[tree.left.dimension] == null){
            treeRange(lo, hi, tree.left, dimensions).forEach(element => {
                pointsInRange.push(element);
            });
        }
    }
    //Check right subtree.
    if(tree.right != null){
        let rightDimVal = getDimensionVal(dimensions, tree.right);
        if(rightDimVal <= hi[tree.right.dimension] || hi[tree.right.dimension] == null){
            treeRange(lo, hi, tree.right, dimensions).forEach(element =>{
                pointsInRange.push(element); 
            });
        }
    }

    return pointsInRange;
}

/*
* Custom range function to return the points within the range.
* @param {array} lo - Array of values [BX, BY, BC, BP] where [BX, BY] represents the lower left corner of the window. [BC] and [BP] represent the lower limit of the range for the associated attributes.
* @param {array} hi - Array of values [EX, EY, EC, EP] where [EX, EY] represents the upper right corner of the window. [EC] and [EP] represent the upper limit of the range for the associated attributes.
*/
kdTree.kdTree.prototype.range = function (lo, hi, completedCallback) {
    let pointsInRange = [];
    if(lo.length == 4 && hi.length == 4){
        pointsInRange = treeRange(lo, hi, this.root, this.dimensions);
    }
    else{
        this.logger.info('Incorrect array length.');
    }

    if(completedCallback){
        completedCallback(lo, hi, pointsInRange);
    }
}

module.exports = kdTree;