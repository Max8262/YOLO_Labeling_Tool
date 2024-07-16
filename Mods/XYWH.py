
def Convert(coords, wid, hgt):
    coords[0] = (coords[0] + coords[2] / 2) / wid
    coords[1] = (coords[1] + coords[3] / 2) / hgt
    coords[2] = coords[2] / wid
    coords[3] = coords[3] / hgt


