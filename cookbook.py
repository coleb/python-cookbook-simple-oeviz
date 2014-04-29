"""
 Flask server for OEViz
 Copyright (C) 2014 OpenEye Scientific Software, Inc.
"""
from urllib import unquote

from flask import Flask, render_template, Response
from openeye.oechem import OETransparentColor, OEGraphMol, OEParseSmiles, OERed
from openeye.oedepict import (OEImage, OE2DMolDisplayOptions,
                              OEScale_AutoScale, OE2DMolDisplay,
                              OERenderMolecule, OEWriteImageToString,
                              OEPrepareDepiction, OE2DPoint, OEFont,
                              OEFontFamily_Helvetica)

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
    image = OEImage(400, 400, OETransparentColor)

    # Process SMILES
    mol = OEGraphMol()
    parsed = OEParseSmiles(mol, str(unquote(smiles)))
    OEPrepareDepiction(mol)

    if parsed:
        # Create image of molecule
        opts = OE2DMolDisplayOptions(image.GetWidth(),
                                     image.GetHeight(), OEScale_AutoScale)
        disp = OE2DMolDisplay(mol, opts)
        OERenderMolecule(image, disp)
    else:
        # Create error image
        font = OEFont()
        font.SetFamily(OEFontFamily_Helvetica)
        font.SetSize(20)
        font.SetColor(OERed)
        image.DrawText(OE2DPoint(image.GetWidth()/2.0, image.GetHeight()/2.0),
                       'Your SMILES is not valid', font)

    img_content = OEWriteImageToString('png', image)

    return Response(img_content, mimetype='image/png')


if __name__ == "__main__":
    app.run()
