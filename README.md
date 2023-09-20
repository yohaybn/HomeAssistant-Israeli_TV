# HomeAssistant-Israeli_TV
HomeAssistant integration for Israeli TV channels
## Installation

Installation via [HACS](https://hacs.xyz/) (recommended) or by copying files to `custom_components/israeli_tv` in your Home Assistant configuration directory.

## Configuration

The component requires configuration via the Home Assistant configuration file. The following parameters are required:

    # Example configuration.yaml entry
    ...
    israeli_tv:
    ...

## Services

The following services are implemented by the component:
- `play_channel_XX` - enable you to play the selected channel in the media player that you choose


## TODO

- Add more cahnnels.
- Make it generic
