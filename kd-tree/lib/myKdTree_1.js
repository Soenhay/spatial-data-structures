
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

//Add our custom range function to the module.
kdTree.kdTree.prototype.range = function(lo, hi, visit){
    console.log('ranged');
    //console.log(this.root);
}

module.exports = kdTree;