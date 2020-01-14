# Inspecting the Vimeo Android App

## Prerequisites

* Ubuntu 18.04
* Android Studio 3
* Apktool (https://ibotpeaches.github.io/Apktool/)
* mitmproxy (https://mitmproxy.org/)
* Add Android Sdk tools to `PATH`:
  ```bash
  # Android Sdk
  ANDROID_SDK_ROOT=~/Android/Sdk
  export PATH=$PATH:$ANDROID_SDK_ROOT/build-tools/29.0.2
  export PATH=$PATH:$ANDROID_SDK_ROOT/platform-tools
  export PATH=$PATH:$ANDROID_SDK_ROOT/tools
  ```

## Download APK

Install the Vimeo-App on your Android phone.

```bash
# Find APK on phone
adb shell pm list packages | grep vimeo
adb shell pm path com.vimeo.android.videoapp

# Download APK from phone
adb pull/data/app/com.vimeo.android.videoapp-5_5xt0A4JQp9O0bhh2I-5A==/base.apk
mv base.apk com.vimeo.android.videoapp.apk
```

## Enable debug mode and disable certificate pinning

```bash
# Decompile APK
apktool d com.vimeo.android.videoapp.apk

# Add `android:debuggable="true"` to the <application> element
vi com.vimeo.android.videoapp/AndroidManifest.xml

# Disable certificate pinning by removing lines
# > .line 12
# > invoke-direct {p0, v0}, Lcom/vimeo/networking/RetrofitSetup;->setupCertPinning(Lcom/vimeo/networking/RetrofitClientBuilder;)V
vi com.vimeo.android.videoapp/smali_classes2/com/vimeo/networking/RetrofitSetup.smali

# Enable user certs for all domains
# (https://android-developers.googleblog.com/2016/07/changes-to-trusted-certificate.html)
# Replace the contents of the network config with the following code:
# <?xml version="1.0" encoding="utf-8"?>
# <network-security-config>  
#     <base-config>  
#          <trust-anchors>  
#             <!-- Trust preinstalled CAs -->  
#             <certificates src="system" />  
#             <!-- Additionally trust user added CAs -->  
#             <certificates src="user" />  
#         </trust-anchors>  
#     </base-config>  
# </network-security-config>
vi com.vimeo.android.videoapp/res/xml/network_security_config.xml

# Compile
apktool b com.vimeo.android.videoapp --use-aapt2

# Sign APK (https://developer.android.com/studio/build/building-cmdline#sign_cmdline)
cd com.vimeo.android.videoapp/dist/
keytool -genkey -v -keystore release-key.jks -keyalg RSA -keysize 2048 -validity 10000 -alias test
zipalign -v -p 4 com.vimeo.android.videoapp.apk com.vimeo.android.videoapp.aligned.apk
apksigner sign --ks release-key.jks --out com.vimeo.android.videoapp.aligned.signed.apk com.vimeo.android.videoapp.aligned.apk
```

## Inspect traffic

* Start mitmproxy by running `mitmweb`.
* Open Android Studio and select "Profile or debug APK".
  Select the previously generated file `com.vimeo.android.videoapp.aligned.signed.apk`.
* Make sure to have a device in AVD Manager.
* Click the "Run" button. Add the proxy config to the emulator settings.
  (Your IP [`ip a`] and port `8080`)
* Install the mitm certificate inside Android by visiting [mitm.it](mitm.it).
* You should now be able to inspect all network traffic.
