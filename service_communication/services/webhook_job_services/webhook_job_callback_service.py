import json
import logging

logger = logging.getLogger(__name__)


class CallbackType:
    SUCCESS = 0
    ERROR = 1


class WebhookJobCallbackService:
    WEBHOOK_JOB_CALLBACKS = {
        # FORMAT: request_type : [success_callback, error_callback]
        # CALL: callback_type (by index): 0 = success_callback / 1 = error_callback /
    }

    @classmethod
    def register_callbacks(cls, request_type, callbacks):
        assert request_type not in cls.WEBHOOK_JOB_CALLBACKS, "Duplicate request_type {} callback while registering to webhook job callback service".format(
            request_type)
        assert isinstance(callbacks, tuple) and len(
            callbacks) == 2, "Invalid callbacks registered, callbacks param must be tuple and is formatted (success_callback, error_callback)"
        cls.WEBHOOK_JOB_CALLBACKS[request_type] = callbacks

    @classmethod
    def handle_successful_result(cls, webhook_job_obj, response_text):
        is_success, json_response = cls.parse_response(response_text)
        logger.info("Handling callback for successful result - Webhook job {}".format(webhook_job_obj.id))
        if is_success:
            cls.handle_result(CallbackType.SUCCESS, webhook_job_obj, json_response)
        else:
            raise ValueError("Responded error message - Webhook job {}".format(webhook_job_obj.id))

    @classmethod
    def handle_failed_result(cls, webhook_job_obj, response_text):
        try:
            _, json_response = cls.parse_response(response_text)
        except Exception:
            logger.warning("Failed to parse json response - {}".format(webhook_job_obj.id))
            json_response = {}
        logger.info("Handling callback for failed result - Webhook job {}".format(webhook_job_obj.id))
        cls.handle_result(CallbackType.ERROR, webhook_job_obj, json_response)

    @classmethod
    def handle_result(cls, callback_type, webhook_job_obj, json_response):
        request_type = webhook_job_obj.request_type
        relate_obj = webhook_job_obj.relate_object
        try:
            callback = cls.WEBHOOK_JOB_CALLBACKS.get(request_type)[callback_type]
        except Exception:
            pass
        else:
            if callable(callback):
                callback(relate_obj, json_response)

    @classmethod
    def parse_response(cls, response_text):
        if not response_text:
            return False, {}
        try:
            json_response = json.loads(response_text)
        except Exception:
            return False, {}
        else:
            return json_response.get("success") is True, json_response
