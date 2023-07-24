#include <gst/gst.h>
#include <gst/rtsp-server/rtsp-server.h>



static void
client_connected (GstRTSPServer * server, GstRTSPClient * client, gpointer user_data)
{
  GstRTSPConnection *connection = gst_rtsp_client_get_connection(client);
  const gchar *ip = gst_rtsp_connection_get_ip(connection);
  g_print ("Client connected: %s\n", ip);
}


/* static void
media_configure (GstRTSPMediaFactory * factory, GstRTSPMedia * media, gpointer user_data)
{
  g_print ("Media configured: %s\n", GST_OBJECT_NAME (media));
} */

static void
media_configure (GstRTSPMediaFactory * factory, GstRTSPMedia * media, gpointer user_data)
{
  const gchar *launch = gst_rtsp_media_factory_get_launch (factory);
  g_print ("Media configured with launch: %s\n", launch);
}


int
main (int argc, char *argv[])
{
  GMainLoop *loop;
  GstRTSPServer *server;
  GstRTSPMountPoints *mounts;
  GstRTSPMediaFactory *factory;

  gst_init (&argc, &argv);

  if (argc != 2) {
    g_print ("Usage: %s <ip-address>\n", argv[0]);
    return -1;
  }

  server = gst_rtsp_server_new ();
  g_object_set(server, "address", argv[1], NULL);

  g_signal_connect (server, "client-connected", (GCallback) client_connected, NULL);

  mounts = gst_rtsp_server_get_mount_points (server);

  factory = gst_rtsp_media_factory_new ();
  gst_rtsp_media_factory_set_launch (factory, "( udpsrc port=5600 ! application/x-rtp, payload=96 ! rtpjitterbuffer ! rtph264depay ! h264parse !rtph264pay name=pay0 pt=96 )");

  g_signal_connect (factory, "media-configure", (GCallback) media_configure, NULL);

  gst_rtsp_mount_points_add_factory (mounts, "/test", factory);

  g_object_unref (mounts);

  gst_rtsp_server_attach (server, NULL);

  g_print ("RTSP server started at rtsp://%s/test\n", argv[1]);

  loop = g_main_loop_new (NULL, FALSE);
  g_main_loop_run (loop);

  return 0;
}
