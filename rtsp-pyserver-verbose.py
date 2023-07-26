import gi
import logging
import sys, getopt

gi.require_version('Gst', '1.0')
gi.require_version('GstRtspServer', '1.0')
from gi.repository import Gst, GstRtspServer, GLib

logging.basicConfig(level=logging.DEBUG)

def on_client_connected(server, client):
    connection = client.get_connection()
    logging.info("Client connected: {0}".format(connection.get_ip()))

def on_media_configure(factory, media):
    logging.info("Media configured: {0}".format(media.get_element().get_name()))

    def on_message(bus, message):
        t = message.type
        if t == Gst.MessageType.STATE_CHANGED:
            if message.src == media.get_element():
                old_state, new_state, pending_state = message.parse_state_changed()
                logging.debug("Pipeline state changed from {0} to {1}".format(
                    Gst.Element.state_get_name(old_state), Gst.Element.state_get_name(new_state)))
        elif t == Gst.MessageType.ERROR:
            err, debug = message.parse_error()
            logging.error("Error: {0}".format(err, debug))
        elif t == Gst.MessageType.EOS:
            logging.info("End-Of-Stream reached")

    bus = media.get_element().get_bus()
    bus.add_signal_watch()
    bus.connect("message", on_message)

def on_teardown_request(client, session):
    logging.info("Client disconnected: {0}".format(client.get_host()))

def on_idle(loop):
    session_pool = server.get_session_pool()
    if session_pool.get_n_sessions() == 0:
        logging.info("No active sessions")
        #loop.quit()
    else:
        logging.info("There are {0} active sessions".format(session_pool.get_n_sessions()))


if __name__ == '__main__':
    
    ip_address = None
    opts, args = getopt.getopt(sys.argv[1:], "i:",)
    for opt, arg in opts:
        if opt == '-i':
            ip_address = arg
            print(f"running server on {ip_address}")
    
    if ip_address is None:
        sys.exit("no ip address provided, please run the script with -i <ip>")

    Gst.init(None)

    mainloop = GLib.MainLoop()

    # create a server
    server = GstRtspServer.RTSPServer.new()
    # G14
    #server.set_address("10.29.17.108")
    # RPi
    server.set_address(ip_address)
    # RPi USB
    #server.set_address("169.254.74.240")

    # connect to the client-connected signal
    server.connect("client-connected", on_client_connected)

    # get the mount points for this server
    mounts = server.get_mount_points()

    # make a media factory for a test stream
    factory = GstRtspServer.RTSPMediaFactory.new()
    # With jitterbuffer
    #factory.set_launch("( udpsrc port=5600 ! application/x-rtp, payload=96 ! rtpjitterbuffer ! rtph264depay ! h264parse ! rtph264pay name=pay0 pt=96 )")
    # No jiterbuffer, no reencoding
    factory.set_launch("( udpsrc port=5600 ! application/x-rtp, payload=96 ! rtph264depay ! rtph264pay name=pay0 pt=96 )")

    # connect to the media-configure signal
    factory.connect("media-configure", on_media_configure)

    # attach the test stream to the /test url
    mounts.add_factory("/rovcam", factory)

    # attach the server to the default maincontext
    server.attach(None)

    logging.info(f"stream ready at rtsp://{ip_address}/rovcam")
    try:
        mainloop.run()
    except Exception as e:
        logging.error("Error in main loop: {0}".format(e))
        raise
