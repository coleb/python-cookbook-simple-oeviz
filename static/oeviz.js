/*!
 * Copyright 2014 OpenEye Scientific Software, Inc.
 */

function updateImage() {
    'use strict';
    var input = document.getElementById("oeinput").value;

    if (input === "") {
        input = "X";
    }

    document.getElementById("oeimage").src = "/smiles/" + encodeURIComponent(input) + "/";
}