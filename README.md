# Installing the C version of the server
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

## Create the server file

<aside>
‼️ You need to change the ip to the wlan0 ip of your raspberry pi!

</aside>

Create a file `rtsp-server.c`

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
