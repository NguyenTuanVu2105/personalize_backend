import logging

from django import forms
from django.forms import ModelForm as BaseModelForm

from HUB.exceptions.FormValidationError import FormValidationError

logger = logging.getLogger(__name__)


class ModelForm(BaseModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        optional_fields = getattr(self.Meta, "optional_fields", [])
        for field in optional_fields:
            if field in self.fields:
                self.fields[field].required = False
        if not self.data:
            self.fields = {}

    def validate(self, raise_exception=True):
        valid = super().is_valid()
        if not valid and raise_exception:
            logger.info(self.errors.get_json_data())
            raise FormValidationError(errors=self.errors.get_json_data())
        return valid


class BaseForm(forms.Form):
    def validate(self, raise_exception=True):
        valid = super().is_valid()
        if not valid and raise_exception:
            logger.info(self.errors.get_json_data())
            raise FormValidationError(errors=self.errors.get_json_data())
        return valid


class PreserveNotNoneInitialValueModelFormMixin:
    def clean(self):
        cleaned_data = super().clean()
        for key, value in cleaned_data.items():
            if not value:
                cleaned_data[key] = self.initial[key]
        return cleaned_data


class PreserveNotNoneDataValueModelFormMixin:
    def clean(self):
        # because JSONField = {} is set to None by default
        # -> should preserve it for not null constraint
        cleaned_data = super().clean()
        for key, value in cleaned_data.items():
            if not value:
                cleaned_data[key] = self.data[key]
        return cleaned_data


class PreserveNotNoneInitialValueModelForm(PreserveNotNoneInitialValueModelFormMixin, ModelForm):
    pass


class PreserveNotNoneDataValueModelForm(PreserveNotNoneDataValueModelFormMixin, ModelForm):
    pass
