
# Installing the C++ version of the server
## Install dependencies

```bash
sudo apt update
sudo apt install pkg-config
sudo apt install libgstreamer1.0-dev
sudo apt install libgstrtspserver-1.0-dev
```

## Clone this repo

```bash
git clone https://github.com/Vince-vd/upd-rtsp-server.git
```

## Compile the server file

```bash
g++ rtsp-server-cpp.cpp -o rtsp_server_cpp `pkg-config --cflags --libs gstreamer-1.0 gstreamer-rtsp-1.0 gstreamer-rtsp-server-1.0`
```

## Run the server with your wlan0 ip address as argument

```bash
./rtsp_server_cpp <ip-address>
```
# Optional: run the C version
## Edit the server file

<aside>
‼️ You need to change the ip to the wlan0 ip of your raspberry pi!

</aside>

## Compile the server file

```bash
gcc rtsp-server.c -o rtsp-server $(pkg-config --cflags --libs gstreamer-1.0 gstreamer-rtsp-server-1.0)
```

## Run the compiled server

```bash
./rtsp-server
```

# Installing the python version of the server

Under construction
