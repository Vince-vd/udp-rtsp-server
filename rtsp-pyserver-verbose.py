import gi
gi.require_version('Gst', '1.0')
gi.require_version('GstRtspServer', '1.0')
from gi.repository import Gst, GstRtspServer, GLib

def on_client_connected(server, client):
    connection = client.get_connection()
    print("Client connected: {0}".format(connection.get_ip()))

def on_media_configure(factory, media):
    print("Media configured: {0}".format(media.get_element().get_name()))

    def on_message(bus, message):
        t = message.type
        if t == Gst.MessageType.STATE_CHANGED:
            if message.src == media.get_element():
                old_state, new_state, pending_state = message.parse_state_changed()
                print("Pipeline state changed from {0} to {1}".format(
                    Gst.Element.state_get_name(old_state), Gst.Element.state_get_name(new_state)))
        elif t == Gst.MessageType.ERROR:
            err, debug = message.parse_error()
            print("Error: {0}".format(err, debug))
        elif t == Gst.MessageType.EOS:
            print("End-Of-Stream reached")

    bus = media.get_element().get_bus()
    bus.add_signal_watch()
    bus.connect("message", on_message)

Gst.init(None)

mainloop = GLib.MainLoop()

# create a server
server = GstRtspServer.RTSPServer.new()
server.set_address("10.29.17.108")

# connect to the client-connected signal
server.connect("client-connected", on_client_connected)

# get the mount points for this server
mounts = server.get_mount_points()

# make a media factory for a test stream
factory = GstRtspServer.RTSPMediaFactory.new()
#factory.set_launch("( udpsrc port=5600 ! application/x-rtp, payload=96 ! rtpjitterbuffer ! rtph264pay name=pay0 pt=96 )")
factory.set_launch("( udpsrc port=5600 ! application/x-rtp, payload=96 ! rtpjitterbuffer ! rtph264depay ! h264parse ! rtph264pay name=pay0 pt=96 )")

# connect to the media-configure signal
factory.connect("media-configure", on_media_configure)

# attach the test stream to the /test url
mounts.add_factory("/test", factory)

# attach the server to the default maincontext
server.attach(None)

print("stream ready at rtsp://10.29.17.108/test")
mainloop.run()
