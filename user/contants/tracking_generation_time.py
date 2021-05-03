class TrackingGenerationTime:
    DEFAULT = -3
    ASAP = -2
    AT_PACKAGING_STAGE = -1


class TrackingGenerationTimeVerbal:
    DEFAULT = {}
    ASAP = {"generate_label_config": {"mode": "after_pushed"}}
    AT_PACKAGING_STAGE = {"generate_label_config": {"mode": "after_produced"}}


TRACKING_GENERATION_TIME_VERBOSE_DICT = {
    TrackingGenerationTime.DEFAULT: TrackingGenerationTimeVerbal.DEFAULT,
    TrackingGenerationTime.ASAP: TrackingGenerationTimeVerbal.ASAP,
    TrackingGenerationTime.AT_PACKAGING_STAGE: TrackingGenerationTimeVerbal.AT_PACKAGING_STAGE,
}


def get_track_generation_json(time):
    if time in TRACKING_GENERATION_TIME_VERBOSE_DICT:
        return TRACKING_GENERATION_TIME_VERBOSE_DICT[time]
    else:
        return {"generate_label_config": {"delay_days": time}}


