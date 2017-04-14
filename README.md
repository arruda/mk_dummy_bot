# Mage Knight Dummy Bot
A simple Dummy player app for Mage Knight using Kivy.

# Screenshot
There are some images in the [docs](/docs) dir

## Dev
### Install Requirements

```
pip install -r base_requirements.txt
pip install -r requirements.txt
```

### Building app
**OBS:** Might be necessary to start adb server as root before, ex:
`sudo /home/myuser/.buildozer/android/platform/android-sdk-20/platform-tools/adb start-server`

`buildozer android debug deploy`

## Publishing
`buildozer android release`


# License
Software under MIT license. See LICENSE file for more details.