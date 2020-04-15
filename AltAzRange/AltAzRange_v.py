# Based on javascript solution by https://github.com/cosinekitty/geocalc
# calculated distance is in meters and THIS IS NOT distance around the curvature of Earth
# (it's like straight line between points)
# latitude : -90 to 90 [deg]
# longitude : -180 to 180 [deg]
# height : is meters above sea level (can be lower than zero) [m]
import math


class AltAzimuthRange(object):
    default_lat = None
    default_long = None
    default_elv = None

    def __init__(self):
        if AltAzimuthRange.default_lat and AltAzimuthRange.default_long and AltAzimuthRange.default_elv:
            self.a = {'lat': AltAzimuthRange.default_lat, 'lon': AltAzimuthRange.default_long,
                      'elv': AltAzimuthRange.default_elv}
        else:
            self.a = None
        self.b = None
        pass

    def observer(self, lat: float, long: float, altitude: float):
        # latitude, longitude, meters above sea level (can be lower than zero)
        self.a = {'lat': lat, 'lon': long, 'elv': altitude}

    def target(self, lat: float, long: float, altitude: float):
        # latitude, longitude, meters above sea level (can be lower than zero)
        self.b = {'lat': lat, 'lon': long, 'elv': altitude}

    def calculate(self) -> dict:
        if not self.a:
            raise Exception(
                "Observer is not defined. Fix this by using instance_name.observer(lat,long,altitude) method")
        if not self.b:
            raise Exception(
                "Target location is not defined. Fix this by using instance_name.target(lat,long,altitude) method")
        ap, bp = AltAzimuthRange.LocationToPoint(self.a), AltAzimuthRange.LocationToPoint(self.b)
        br = AltAzimuthRange.RotateGlobe(self.b, self.a, bp['radius'])
        dist = round(AltAzimuthRange.Distance(ap, bp), 2)
        if br['z'] * br['z'] + br['y'] * br['y'] > 1.0e-6:
            theta = math.atan2(br['z'], br['y']) * 180.0 / math.pi
            azimuth = 90.0 - theta
            if azimuth < 0.0:
                azimuth += 360.0
            if azimuth > 360.0:
                azimuth -= 360.0
            azimuth = round(azimuth, 2)
            bma = AltAzimuthRange.NormalizeVectorDiff(bp, ap)
            if bma:
                elevation = 90.0 - (180.0 / math.pi) * math.acos(
                    bma['x'] * ap['nx'] + bma['y'] * ap['ny'] + bma['z'] * ap['nz'])
                elevation = round(elevation, 2)
            else:
                elevation = None
        else:
            azimuth = None
            elevation = None
        return {"azimuth": azimuth, "elevation": elevation, "distance": dist}

    @staticmethod
    def default_observer(lat: float, long: float, altitude: float):
        AltAzimuthRange.default_lat = lat
        AltAzimuthRange.default_long = long
        AltAzimuthRange.default_elv = altitude

    @staticmethod
    def Distance(ap, bp):
        dx = ap['x'] - bp['x']
        dy = ap['y'] - bp['y']
        dz = ap['z'] - bp['z']
        return math.sqrt(dx * dx + dy * dy + dz * dz)

    @staticmethod
    def GeocentricLatitude(lat):
        e2 = 0.00669437999014
        clat = math.atan((1.0 - e2) * math.tan(lat))
        return clat

    @staticmethod
    def EarthRadiusInMeters(latituderadians):
        a = 6378137.0
        b = 6356752.3
        cos = math.cos(latituderadians)
        sin = math.sin(latituderadians)
        t1 = a * a * cos
        t2 = b * b * sin
        t3 = a * cos
        t4 = b * sin
        return math.sqrt((t1 * t1 + t2 * t2) / (t3 * t3 + t4 * t4))

    @staticmethod
    def LocationToPoint(c):
        lat = c['lat'] * math.pi / 180.0
        lon = c['lon'] * math.pi / 180.0
        radius = AltAzimuthRange.EarthRadiusInMeters(lat)
        clat = AltAzimuthRange.GeocentricLatitude(lat)

        cos_lon = math.cos(lon)
        sin_lon = math.sin(lon)
        cos_lat = math.cos(clat)
        sin_lat = math.sin(clat)
        x = radius * cos_lon * cos_lat
        y = radius * sin_lon * cos_lat
        z = radius * sin_lat

        cos_glat = math.cos(lat)
        sin_glat = math.sin(lat)

        nx = cos_glat * cos_lon
        ny = cos_glat * sin_lon
        nz = sin_glat

        x += c['elv'] * nx
        y += c['elv'] * ny
        z += c['elv'] * nz

        return {'x': x, 'y': y, 'z': z, 'radius': radius, 'nx': nx, 'ny': ny, 'nz': nz}

    @staticmethod
    def NormalizeVectorDiff(b, a):
        dx = b['x'] - a['x']
        dy = b['y'] - a['y']
        dz = b['z'] - a['z']
        dist2 = dx * dx + dy * dy + dz * dz
        if dist2 == 0:
            return None
        dist = math.sqrt(dist2)
        return {'x': (dx / dist), 'y': (dy / dist), 'z': (dz / dist), 'radius': 1.0}

    @staticmethod
    def RotateGlobe(b, a, b_radius):
        br = {'lat': b['lat'], 'lon': (b['lon'] - a['lon']), 'elv': b['elv']}
        brp = AltAzimuthRange.LocationToPoint(br)

        alat = AltAzimuthRange.GeocentricLatitude(-a['lat'] * math.pi / 180.0)
        acos = math.cos(alat)
        asin = math.sin(alat)

        bx = (brp['x'] * acos) - (brp['z'] * asin)
        by = brp['y']
        bz = (brp['x'] * asin) + (brp['z'] * acos)

        return {'x': bx, 'y': by, 'z': bz, 'radius': b_radius}


if __name__ == "__main__":
    # if you plan to track multiple objects set default observer
    # localisation of instance (height above sea level in meters)
    AltAzimuthRange.default_observer(51.773931, 18.061959, 50)

    # create instance of class
    satellite_1 = AltAzimuthRange()
    high_alt_balloon = AltAzimuthRange()

    # use if no default observer is specified, also use to can override it
    # satellite_1.observer(51.773931, 18.061959, 50)

    # set target localisation of instance (height above sea level in meters)
    satellite_1.target(51.681562, 17.778988, 430000)
    high_alt_balloon.target(52.307790, 21.37, 190000)

    # call calculate method that returns dictionary
    # calculate and returns azimuth [deg], elevation angle [deg], distance [m]
    print(satellite_1.calculate())

    result = high_alt_balloon.calculate()
    # print(result['elevation'])

    # remember to delete unused instance of class
    del satellite_1, high_alt_balloon
