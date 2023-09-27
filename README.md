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
          - name: "כאן חינוכית"
            sensor_name: "kan_kids"
            url: https://kan23.media.kan.org.il/hls/live/2024691/2024691/master.m3u8
            thumbnail: https://www.kankids.org.il/favicon-kids/apple-touch-icon.png

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
| `channels` | channel array | optional | additional channels to use with services and media source  |
| `name` | string | **required** | name of channel as found [here](https://www.bevy.be/bevyfiles/israelpremium.xml.txt)   |
| `sensor_name` | string | **required** |  name for programming sensor |
| `url` | string | **required** | m3u8 url that you provide |
| `thumbnail` | string | optional | thumbnail url that you provide for media source icon |



## Services

The following services are implemented by the component:
- `play_channel_XX` - enable you to play the selected channel in the media player that you choose

- `play_custom_channel` - enable you to play the selected channel (from the additional channels) in the media player that you choose
  ```
  service: israeli_tv.play_custom_channel
  data:
    channel_name: kan_kids ## the sensor_name from configuration entry
  target:
    entity_id: media_player.office_display```

- `get_channel_url` - get the url of channel in the response


## Automation example
```
- alias: Send channel 11
  description: 'Send link to mobile phone when show started'
  trigger:
  - platform: state
    entity_id:
    - sensor.israeli_tv_channel_11
      to: "חדשות הלילה"
  action:
  - service: israeli_tv.get_channel_url
    data: 
      channel_name: channel_11
    response_variable: channel
  - service: notify.mobile_app_XXXXX
    data:
      message: "האם תרצה לצפות?"
      title: "מתחילה עכשיו {{states( 'sensor.israeli_tv_channel_11')  }}"
      data:
        actions:
        - action: "URI" # Must be set to URI if you plan to use a URI
          title: "Open Url"
          uri: "{{channel.url }}"
  mode: single
```

## TODO

- Add more cahnnels.
- Make it generic
