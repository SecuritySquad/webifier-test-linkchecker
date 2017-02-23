"use strict";
var page = require('webpage').create(),
    system = require('system'),
    address;

if (system.args.length === 1) {
    console.log('Usage: open.js <some URL>');
    phantom.exit(1);
} else {
    address = system.args[1];

    page.onResourceRequested = function (req) {
        console.log('requested: ' + req.url);
    };

    page.open(address, function (status) {
        if (status !== 'success') {
            console.log('FAIL to load the address');
        } else {
            var parent = page.evaluate(function () {
                var test = document.querySelectorAll('a');
                return Array.prototype.map.call(test, function (elem) {
                    return elem.href;
                });
            });
            for (var i = 0; i < parent.length; i++) {
                //Print parent link
                console.log("Link: " + parent[i]);
            }
        }
        phantom.exit();
    });
}
