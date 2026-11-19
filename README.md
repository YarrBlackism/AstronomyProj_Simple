Star Constellation

Draw constellations from self-taken night-sky photos.

Give the script a night-sky photo, and it saves a copy with constellation lines drawn on the stars and each constellation labeled.
Example result

How?

Every star looks like the same small dot, so you can’t recognize it by appearance alone. You can only identify it by where it sits relative to the stars around it. This script uses plate solving to do that:

1. photo is uploaded to astrometry.net.
2. astrometry.net matches the star pattern in your photo against a star catalog. It sends back a WCS, a map that converts any sky position (RA/Dec) into a pixel position in your photo.
3. The script downloads constellation line data from d3-celestial. Each constellation is a list of star positions.
4. The script converts each star position to a pixel position, draws lines between the stars, and writes the constellation names.

Requirements

* Python 3.9 or newer
* A free astrometry.net account (for the API key)
* A sharp night-sky photo with plenty of stars

Install the packages:

pip install astropy astroquery opencv-python

Setup: API key

1. Sign in at nova.astrometry.net.
2. Navigate to Go to Dashboard > My Profile and copy your API key.
   <img width="1021" height="836" alt="image" src="https://github.com/user-attachments/assets/1b129ed7-fe68-492b-a4a9-cf0a547efc69" />

4. Set it as an environment variable (don’t paste the key into the code).
<img width="1900" height="46" alt="image" src="https://github.com/user-attachments/assets/b5028c43-9f91-459b-a294-16685c9ef208" />

To make it permanent, use setx ASTROMETRY_API_KEY "your-key", then restart your terminal or VS Code.

Linux / macOS:

export ASTROMETRY_API_KEY="your-key"

Check it’s set:

echo $env:ASTROMETRY_API_KEY    # Windows
echo $ASTROMETRY_API_KEY        # Linux / macOS

Usage

python simple_constellations.py night.jpg

Example output:

Solving... (can take a few minutes)
Found: Orion, Taurus, Gemini, Canis Major
Saved result.jpg

Files it creates

Column 1	Column 2
File	What it is
result.jpg	Your photo with the constellations drawn on it
upload.jpg	The copy of your photo that gets uploaded
constellations.lines.json	Constellation line data (downloaded the first time)
constellations.json	Constellation names (downloaded the first time)


The code, step by step

Column 1	Column 2
Part	What it does
get_json(name)	Downloads a constellation data file the first time, then reuses the saved copy.
solve(image_path)	Uploads the photo to astrometry.net and returns the WCS (the sky-to-pixel map).
draw(img, wcs)	For each constellation: converts its stars to pixels, draws lines between them, and writes the name in the middle of the stars that are in the photo.
__main__	Loads the photo, saves upload.jpg, solves it, draws, and saves result.jpg.

Known limitations

* Needs an internet connection and an astrometry.net API key.
* Very large constellations that stretch right past the edge of the photo (Eridanus for instance) can be safely skipped.
* Labels can overlap when lots of constellations are close together.

Credits / resources used
* https://docs.astropy.org/projects/astroquery/en/latest/astrometry_net/astrometry_net.html - python module documentation
* astrometry.net: plate solving (Lang et al. 2010, arXiv:0910.2233)
* d3-celestial by Olaf Frohn: constellation data
* Astropy and astroquery: WCS, coordinates, and the astrometry.net client
- [OpenCV](https://opencv.org): drawing on images

