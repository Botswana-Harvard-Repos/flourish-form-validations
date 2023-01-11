from edc_constants.constants import NO, YES, OTHER, NOT_APPLICABLE
from edc_form_validators import FormValidator
from .crf_form_validator import FormValidatorMixin


class TbReferralOutcomesFormValidator(FormValidatorMixin, FormValidator):

    def clean(self):
        self.required_if(
            YES,
            field='tb_eval',
            field_required='tb_eval_location'
        )

        self.validate_other_specify(
            field='tb_eval_location',
            field_required='tb_eval_location_other'
        )

        self.m2m_required_if(
            YES,
            field='tb_diagnostic_perf',
            m2m_field='tb_diagnostics')

        self.m2m_other_specify(
            OTHER,
            m2m_field='tb_diagnostics',
            field_other='tb_diagnostics_other')

        self.required_if(
            YES,
            field='tb_diagnostic_perf',
            field_required='tb_diagnose_pos')

        self.required_if(
            YES,
            field='tb_diagnose_pos',
            field_required='tb_test_results')

        self.required_if(
            *[YES, NO],
            field='tb_diagnose_pos',
            field_required='tb_treat_start',
        )

        self.required_if(
            NO,
            field='tb_diagnostic_perf',
            field_required='tb_treat_start',
            inverse=False
        )

        self.required_if(
            NO,
            field='tb_treat_start',
            field_required='tb_prev_therapy_start')
