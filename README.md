# HomeAssistant-Israeli_TV
HomeAssistant integration for Israeli TV channels
## Installation

Installation via [HACS](https://hacs.xyz/) (recommended) or by copying  `custom_components/israeli_tv` into your Home Assistant configuration directory.

## Configuration

The component requires configuration via the Home Assistant configuration file. The following parameters are required:

    # Example configuration.yaml entry
    ...
    israeli_tv:
        use_defaults: false #optinal- default = true 
        channels: #optinal
          - name: "some name"
            sensor_name: "name for programming sensor"
            url: m3u8_url

    ...

To create sensors with television programming for the channels add 

    # Example configuration.yaml entry
    ...
    sensor:
      - platform: israeli_tv
    ...

| Name | Type | Default |  Description |
| --- | --- | --- | --- | 
| `use_defaults` | bool | true |  create sensors and services for israeli channels (11-14) |
| `channels` | channel array | optional |   |
| `name` | string | **required** | name of channel as found [here](https://www.bevy.be/bevyfiles/israelpremium.xml) (id)  |
| `sensor_name` | string | **required** |  name for programming sensor |
| `url` | string | **required** | m3u8 url that you provide |



## Services

The following services are implemented by the component:
- `play_channel_XX` - enable you to play the selected channel in the media player that you choose


## TODO

- Add more cahnnels.
- Make it generic
