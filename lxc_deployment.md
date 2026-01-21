# Running Audio Transcriber in LXC

Yes, it is possible to run the application inside an LXC container with access to the screen (GUI) and microphone. However, since LXC containers are isolated by default, you need to explicitly configure **pass-through** for the display and audio devices.

## Prerequisities

- Host OS running Linux with LXD/LXC installed.
- Host running a desktop environment (X11 or Wayland setup for XWayland).
- PulseAudio or PipeWire running on the host.

## 1. GUI Access (X11 Forwarding)

To verify the GUI works, you need to mount the X11 socket from the host into the container.

### Step 1: Profile Configuration

Create or edit an LXC profile (e.g., `gui-profile`):

```bash
lxc profile create gui-profile
```

Edit the profile (`lxc profile edit gui-profile`) and add the following configuration to map the X11 socket and GPU:

```yaml
config:
  environment.DISPLAY: :0
  user.user-data: |
    #cloud-config
    package_update: true
    packages:
      - x11-apps
      - mesa-utils
      - python3-tk
      - libasound2
devices:
  X0:
    bind: container
    connect: /tmp/.X11-unix/X0
    listen: /tmp/.X11-unix/X0
    security.gid: "1000"
    security.uid: "1000"
    type: proxy
  mygpu:
    type: gpu
```
*Note: Adjust `DISPLAY` (:0 or :1) and security UIDs/GIDs to match your host user.*

## 2. Microphone Access (PulseAudio Forwarding)

To access the microphone, the easiest way is to pass the PulseAudio socket.

### Step 2: Add Audio Device to Profile

Add the following to the `devices` section of your profile:

```yaml
  PASocket:
    bind: container
    connect: /run/user/1000/pulse/native
    listen: /run/user/1000/pulse/native
    security.gid: "1000"
    security.uid: "1000"
    type: proxy
```

*Note: You also need to set the `PULSE_SERVER` environment variable in the container.*

Add to `config` section:
```yaml
config:
  environment.PULSE_SERVER: unix:/run/user/1000/pulse/native
```

## 3. Launching the Container

Launch a container using the profile:

```bash
lxc launch ubuntu:22.04 transcribe-container --profile default --profile gui-profile
```

## 4. Running the App

1. **Enter the container**:
   ```bash
   lxc exec transcribe-container -- bash
   ```

2. **Install Dependencies**:
   Inside the container, you will need to install system libraries for Tkinter and Audio:
   ```bash
   apt update
   apt install -y python3-tk libasound2 libpulse0 x11-apps
   ```

3. **User Setup**:
   Ensure you run the app as a user with the same UID (usually 1000) as the host, or configured in the mapping, so it has permission to write to the forwarded sockets.

   ```bash
   # Create user ubuntu (UID 1000 is usually default on ubuntu images)
   su - ubuntu
   ```

4. **Run the App**:
   Copy your `dist/AudioTranscriber.bin` to the container and run it.
   ```bash
   ./AudioTranscriber.bin
   ```

## Summary

- **Screen**: Works by mapping `/tmp/.X11-unix/X0`.
- **Microphone**: Works by mapping `/run/user/1000/pulse/native`.

If configured correctly, the app window will appear on your host desktop, and it will be able to record audio using your host's microphone.
