from gi.repository import Gst


class CamCapture:
    def __init__(self, image_location):
        '''
        Initialize local variables and attach gst-source/sink/converter
        '''
        Gst.init(None)
        self.player = Gst.Pipeline()

        source = Gst.ElementFactory.make('v4l2src', 'video-source')
        source.set_property('num-buffers', 1)

        vid_converter = Gst.ElementFactory.make('videoconvert', 'ffmpeg1')
        img_converter = Gst.ElementFactory.make('jpegenc', 'jpeg-converter')

        sink = Gst.ElementFactory.make('filesink', None)
        sink.set_property('location', image_location)

        self.player.add(source)
        self.player.add(vid_converter)
        self.player.add(img_converter)
        self.player.add(sink)
        source.link(vid_converter)
        vid_converter.link(img_converter)
        img_converter.link(sink)

    def capture(self):
        self.player.set_state(Gst.State.PLAYING)
        msg = self.player.bus.timed_pop_filtered(
            5 * Gst.SECOND,
            Gst.MessageType.EOS | Gst.MessageType.ERROR)

        if msg.type == Gst.MessageType.EOS:
            self.player.set_state(Gst.State.NULL)
        else:
            raise('Error occurred. Message type: {}'.format(msg.type))
