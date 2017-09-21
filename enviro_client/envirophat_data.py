# pylint: disable=broad-except,invalid-name,wrong-import-position
"""
    EnviroPhat Data model
"""
# import simplejson as json
from envirophat import light, weather, motion


class EnviroPhatData(object):
    """ encapsulate EnviroPhat data in a class """

    _precision = 2

    def __init__(self):
        """ instantiate the class """

    @staticmethod
    def get_light():
        """ return light.light() """
        return light.light()

    @staticmethod
    def get_rgb_light():
        """ return [r, g, b] values """
        return list(light.rgb())

    @staticmethod
    def get_weather_temperature(precision=None):
        """ return weather.temperature() """
        precision = int(precision)
        return round(weather.temperature(), precision)

    @staticmethod
    def get_weather_pressure(precision=None):
        """ return weather.preasure() """
        precision = int(precision)
        return round(weather.pressure(), precision)

    @staticmethod
    def get_weather_altitude(precision=None, qnh=None):
        """ return weather.altitude() """
        precision = int(precision)
        if not qnh:
            qnh = 1020
        qnh = int(qnh)
        return round(weather.altitude(qnh), precision)

    @staticmethod
    def get_mothion_accelerometer():
        """ return motion.accelerometer() """
        return list(motion.accelerometer())

    @staticmethod
    def get_mothion_magnetometer():
        """ return motion.magnetometer() """
        return list(motion.magnetometer())

    @classmethod
    def get_sample(cls, precision=None):
        """ get the sample data format """
        if not precision:
            precision = cls._precision
        precision = int(precision)
        data = {
            'light': {
                'brightness': cls.get_light(),
                'rbg': cls.get_rgb_light()
            },
            'weather': {
                'temperature': cls.get_weather_temperature(precision),
                'pressure': cls.get_weather_pressure(precision),
                'altitude': cls.get_weather_altitude(precision)
            },
            'motion': {
                'accelerometer': cls.get_mothion_accelerometer(),
                'magnetometer': cls.get_mothion_magnetometer()
            }
        }
        return data
