"""
 Flask server for OEViz
 Copyright (C) 2014, 2015 OpenEye Scientific Software, Inc.
"""

try:
    from urllib.parse import unquote
except ImportError:
    from urllib import unquote

from flask import Flask, render_template, Response
from openeye.oechem import OEGraphMol, OESmilesToMol, OERed
from openeye.oedepict import (OEImage, OERenderMolecule, OEWriteImageToString,
                              OEPrepareDepiction, OE2DPoint, OEFont,
                              OEFontFamily_Helvetica, OEAlignment_Center,
                              OEFontStyle_Default, OE2DMolDisplay)

from emoji.unicode_codes import EMOJI_UNICODE

from random import choice

ALL_EMOJI = EMOJI_UNICODE.values()

app = Flask(__name__)
app.debug = True


@app.route('/')
def depict():
    """ Return a simple HTML file """
    return render_template('oeviz.html')


@app.route('/smiles/<smiles>/')
def depict_smiles(smiles):
    """ OEChem and OEDepict image generation """
    # Image to draw on
    image = OEImage(400, 400)

    # Process SMILES
    mol = OEGraphMol()
    parsed = OESmilesToMol(mol, str(unquote(smiles)))
    
    if parsed:
        # Create image of molecule
        newtitle = []
        for c in mol.GetTitle():
            newtitle.append(choice(ALL_EMOJI))
        mol.SetTitle(("".join(newtitle)).encode("UTF-8"))
        
        OEPrepareDepiction(mol)

        disp = OE2DMolDisplay(mol)
        for adisp in disp.GetAtomDisplays():
            adisp.SetLabel(choice(ALL_EMOJI).encode("UTF-8"))
        
        OERenderMolecule(image, disp)
    else:
        # Create error image
        font = OEFont(OEFontFamily_Helvetica, OEFontStyle_Default, 20,
                      OEAlignment_Center, OERed)
        image.DrawText(OE2DPoint(image.GetWidth()/2.0, image.GetHeight()/2.0),
                       'Your SMILES is not valid', font)

    img_content = OEWriteImageToString('svg', image)

    return Response(img_content, mimetype='image/svg+xml')


if __name__ == "__main__":
    app.run(host="0.0.0.0")
