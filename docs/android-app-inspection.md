# Inspecting the Vimeo Android App

## Prerequisites

* Ubuntu 18.04
* Android Studio 3/4 (Android Sdk)
* apk-mitm (https://github.com/shroudedcode/apk-mitm, https://github.com/shroudedcode/apk-mitm/pull/36)
* mitmproxy (https://mitmproxy.org/)
* Add Android Sdk tools to `PATH`:
  ```bash
  # Android Sdk
  ANDROID_SDK_ROOT=~/Android/Sdk
  export PATH=$PATH:$ANDROID_SDK_ROOT/build-tools/29.0.2
  export PATH=$PATH:$ANDROID_SDK_ROOT/emulator
  export PATH=$PATH:$ANDROID_SDK_ROOT/platform-tools
  export PATH=$PATH:$ANDROID_SDK_ROOT/tools
  ```

## Download APK

Enable USB debugging on your Android phone, install the Vimeo-App via Play Store and connect your phone via USB.

```bash
# Find APK on phone
adb shell pm list packages | grep vimeo
adb shell pm path com.vimeo.android.videoapp

# Download APK from phone
adb pull /data/app/com.vimeo.android.videoapp-5_5xt0A4JQp9O0bhh2I-5A==/base.apk
mv base.apk com.vimeo.android.videoapp.apk
```

## Patch APK

```bash
npx apk-mitm com.vimeo.android.videoapp.apk
```

## Setup AVD Virtual Device (Android 11)

You can do this via Android Studio or the `emulator`-tool included in the AndroidSdk.

## Inspect traffic

* Start mitmproxy by running `mitmweb`.
* Open Android Studio and select "Profile or debug APK".
  Select the previously generated file `com.vimeo.android.videoapp-patched`.
* Make sure to have a device in AVD Manager.
* Click the "Run" button. Add the proxy config to the emulator settings.
  (Your IP [`ip a`] and port `8080`)
* Install the mitm certificate inside Android by visiting [mitm.it](mitm.it).
* You should now be able to inspect all network traffic.
