import json
import os
import sys
import urllib.request

import cv2
from astropy import units as u
from astropy.coordinates import SkyCoord
from astropy.wcs import WCS
from astroquery.astrometry_net import AstrometryNet

DATA = "https://raw.githubusercontent.com/ofrohn/d3-celestial/master/data/"


def get_json(name):
    if not os.path.exists(name):
        urllib.request.urlretrieve(DATA + name, name)
    with open(name, encoding="utf-8") as f:
        return json.load(f)


def solve(image_path):
    """Ask astrometry.net where in the sky this photo points."""
    ast = AstrometryNet()
    ast.api_key = os.environ["ASTROMETRY_API_KEY"]
    print("Solving... (can take a few minutes)")
    header = ast.solve_from_image(image_path, force_image_upload=True,
                                  solve_timeout=600, publicly_visible="n")
    if not header:
        sys.exit("Could not solve this photo.")
    return WCS(header)


def draw(img, wcs):
    h, w = img.shape[:2]
    center = wcs.pixel_to_world(w / 2, h / 2)
    radius = center.separation(wcs.pixel_to_world(0, 0)).deg

    lines = get_json("constellations.lines.json")
    names = {c["id"]: c["properties"]["name"] for c in get_json("constellations.json")["features"]}
    found = []

    for con in lines["features"]:
        points_inside = []
        for line in con["geometry"]["coordinates"]:
            stars = SkyCoord([ra % 360 for ra, dec in line] * u.deg,
                             [dec for ra, dec in line] * u.deg)
            if stars.separation(center).deg.max() > min(radius * 2, 80):
                continue 
            xs, ys = wcs.world_to_pixel(stars)
            pts = [(int(x), int(y)) for x, y in zip(xs, ys)]
            for a, b in zip(pts, pts[1:]):
                cv2.line(img, a, b, (255, 200, 80), 3, cv2.LINE_AA)
            points_inside += [p for p in pts if 0 <= p[0] < w and 0 <= p[1] < h]

        if len(points_inside) >= 2:
            name = names[con["id"]]
            found.append(name)
            x = sum(p[0] for p in points_inside) // len(points_inside)
            y = sum(p[1] for p in points_inside) // len(points_inside)
            cv2.putText(img, name, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 3, cv2.LINE_AA)
    return found


if __name__ == "__main__":
    img = cv2.imread(sys.argv[1])
    cv2.imwrite("upload.jpg", img) 
    wcs = solve("upload.jpg")
    found = draw(img, wcs)
    cv2.imwrite("result.jpg", img)
    print("Found:", ", ".join(found) or "nothing")
    print("Saved result.jpg")
