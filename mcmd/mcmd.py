import dbus
import uuid

from .config import GSD_BUS_NAME, FD_PRO_IFACE, GSD_SCR_NAME
from .config import GSD_OBJ_PATH, BRI_PRO_NAME
from .capture import CamCapture
from .utils import get_display_brightness

from PIL import Image, ImageStat


class MCMD:

    def __init__(self):
        '''
        Initialize class variables
        '''
        self.image_location = '/tmp/{}.jpg'.format(
            '{}'.format(uuid.uuid4())[:8])
        self.capture = CamCapture(self.image_location)

    def get_brightness(self):
        '''
        Get ambient brightness
        '''
        image = Image.open(self.image_location).convert('L')
        statistics = ImageStat.Stat(image)
        rms = statistics.rms
        image.close()
        return rms[0]

    def adjust(self):
        '''
        Adjust screen brightness based on cam input
        '''
        self.capture.capture()
        ambient_brightness = self.get_brightness()
        display_brightness = get_display_brightness(ambient_brightness)
        return display_brightness

    def set_brightness(self, brightness):
        session_bus = dbus.SessionBus()

        gsd_power = session_bus.get_object(
            GSD_BUS_NAME, GSD_OBJ_PATH)

        property_iface = dbus.Interface(
            gsd_power, dbus_interface=FD_PRO_IFACE)

        property_iface.Set(
            GSD_SCR_NAME, BRI_PRO_NAME, brightness)
