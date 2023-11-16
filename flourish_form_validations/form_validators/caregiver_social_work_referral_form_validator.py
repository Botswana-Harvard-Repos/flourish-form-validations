from edc_form_validators import FormValidator
from .crf_form_validator import FormValidatorMixin


class CaregiverSocialWorkReferralFormValidator(FormValidatorMixin, FormValidator):

    def clean(self):

        self.validate_referral_reason()

        caregiver_fields = ['is_preg', 'current_hiv_status']
        for field in caregiver_fields:
            self.required_if(
                'caregiver', field='referral_for',
                field_required=field
            )
        self.required_if('child',
                         field='referral_for', field_required='child_exposure_status')

    def validate_referral_reason(self):
        self.m2m_other_specify('refer_other',
                               m2m_field='referral_reason',
                               field_other='reason_other')

        referral_reason = self.cleaned_data.get('referral_reason')
        selected = [reason.short_name for reason in referral_reason]
        value_field = {'local_medical_facility': 'comment', }

        for value, field in value_field.items():
            if isinstance(field, list):
                for required in field:
                    self.required_if_true(
                        value in selected,
                        field_required=required)
            else:
                self.required_if_true(
                    value in selected,
                    field_required=field)
