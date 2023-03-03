
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

kdTree.kdTree.prototype.treeHeight = function(){
    return treeHeight(this);
}

/*
* Custom range function.
* @param {array} lo - Array of values [BX, BY, BC, BP] where [BX, BY] represents the lower left corner of the window. [BC] and [BP] represent the lower limit of the range for the associated attributes.
* @param {array} hi - Array of values [EX, EY, EC, EP] where [EX, EY] represents the upper right corner of the window. [EC] and [EP] represent the upper limit of the range for the associated attributes.
* @param {function} visit - function for checking whether or not a point is with the range.
*/
kdTree.kdTree.prototype.range = function(lo, hi, visit){
    console.log('ranged');
    //console.log(this.root);
}

module.exports = kdTree;