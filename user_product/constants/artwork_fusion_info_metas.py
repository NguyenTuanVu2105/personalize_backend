class LayerType:
    ARTWORK = '1'
    PERSONAL_TEXT = '2'


class VerboseLayerType:
    ARTWORK = 'artwork'
    PERSONAL_TEXT = 'text_personalization'


LAYER_TYPE_CHOICES = [
    (LayerType.ARTWORK, VerboseLayerType.ARTWORK),
    (LayerType.PERSONAL_TEXT, VerboseLayerType.PERSONAL_TEXT)
]


def default_position():
    return {
        "x": 0,
        "y": 0
    }


default_rotation = 0
default_scale = 1

MAX_SCALE_ALLOW = 2.0
MAX_DRAG_RATIO = 0.9

DEFAULT_BACKGROUND_COLOR = "#FFFFFF"
# MIN_SCALE_ALLOW = 0.3
