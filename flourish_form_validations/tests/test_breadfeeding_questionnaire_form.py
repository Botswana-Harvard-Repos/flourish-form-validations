
from django.test import TestCase, tag
from django.core.exceptions import ValidationError
from edc_base.utils import get_utcnow
from edc_constants.constants import YES, NO, NOT_APPLICABLE
from ..form_validators import BreastFeedingQuestionnaireFormValidator
from flourish_form_validations.tests.test_model_mixin import TestModeMixin
from .models import (FlourishConsentVersion, SubjectConsent,
                     Appointment, MaternalVisit, ListModel)
from dateutil.relativedelta import relativedelta
from edc_constants.constants import OTHER 

@tag('bfq')
class TestBreastFeedingQuestionnaireForm(TestModeMixin,TestCase):
    
    def __init__(self, *args, **kwargs):
        super().__init__(BreastFeedingQuestionnaireFormValidator, *args, **kwargs)

    def setUp(self):
        
        FlourishConsentVersion.objects.create(
            screening_identifier='ABC12345')
        
        self.subject_consent = SubjectConsent.objects.create(
            subject_identifier='11111111',
            screening_identifier='ABC12345',
            gender='F',
            dob=(get_utcnow() - relativedelta(years=25)).date(),
            consent_datetime=get_utcnow(),
            version='1')

        appointment = Appointment.objects.create(
            subject_identifier=self.subject_consent.subject_identifier,
            appt_datetime=get_utcnow(),
            visit_code='2001M')

        self.maternal_visit = MaternalVisit.objects.create(
            appointment=appointment,
            subject_identifier=self.subject_consent.subject_identifier,
            report_datetime=get_utcnow())

        self.options = {
            'maternal_visit': self.maternal_visit,
            
        }
        
  
    def test_during_preg_influencers_specify_required(self):
        """ Assert that the During Pregnancy Influencers specify raises an error if 
            during pregnancy influencers includes other, but not specified.
        """
        
        ListModel.objects.create(name=OTHER)
        self.options.update(
            during_preg_influencers=ListModel.objects.all(),
            during_preg_influencers_other=None)
        
        form_validator = BreastFeedingQuestionnaireFormValidator(cleaned_data=self.options)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('during_preg_influencers_other',form_validator._errors)
        
    
    def test_during_preg_influencers_specify_valid(self):
        """ Tests if During Pregnancy Influencers includes other and
            other is specified, cleaned data validates or fails the
            tests if the Validation Error is raised unexpectedly.
        """
        
        ListModel.objects.create(name=OTHER)
        self.options.update(
            during_preg_influencers=ListModel.objects.all(),
            during_preg_influencers_other='blah')
        
        form_validator = BreastFeedingQuestionnaireFormValidator(cleaned_data=self.options)
        import pdb;pdb.set_trace()
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    # after delivery
    def test_after_delivery_influencers_specify_required(self):
        """ Assert that the After Pregnancy Influencers specify raises an error if 
            after pregnancy influencers includes other, but not specified.
        """
        
        ListModel.objects.create(name=OTHER)
        data = {
            'after_delivery_influencers':ListModel.objects.all(),
            'after_delivery_influencers_other':None
        }
            
        form_validator = BreastFeedingQuestionnaireFormValidator(cleaned_data=data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('after_delivery_influencers_other',form_validator._errors)
        
    
    def test_after_delivery_influencers_specify_valid(self):
        """ Tests if After Pregnancy Influencers includes other and
            other is specified, cleaned data validates or fails the
            tests if the Validation Error is raised unexpectedly.
        """
        
        ListModel.objects.create(name=OTHER)
        self.options.update(
            after_delivery_influencers=ListModel.objects.all(),
            after_delivery_influencers_other='blah')
        
        form_validator = BreastFeedingQuestionnaireFormValidator(cleaned_data=self.options)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')
    

    def test_infant_feeding_reasons_specify_required(self):
        """ Assert that the Infant Feeding specify raises an error if 
            infant feeding includes other, but not specified.
        """
        
        ListModel.objects.create(name=OTHER)
        self.options.update(
            infant_feeding_reasons=ListModel.objects.all(),
            infant_feeding_other=None)
        
        form_validator = BreastFeedingQuestionnaireFormValidator(cleaned_data=self.options)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('infant_feeding_other',form_validator._errors)
        
    
    def test_infant_feeding_reasons_specify_valid(self):
        """ Tests if Infant Feeding includes other and
            other is specified, cleaned data validates or fails the
            tests if the Validation Error is raised unexpectedly.
        """
        
        ListModel.objects.create(name=OTHER)
        self.options.update(
            infant_feeding_reasons=ListModel.objects.all(),
            infant_feeding_other='blah')
        
        form_validator = BreastFeedingQuestionnaireFormValidator(cleaned_data=self.options)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')
      
      
    def test_hiv_status_aware_required(self):
        
        self.options.update(
            feeding_hiv_status=NO,
            hiv_status_aware=None)
        
        form_validator = BreastFeedingQuestionnaireFormValidator(cleaned_data=self.options)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('hiv_status_aware',form_validator._errors)
      
      
    def test_hiv_status_aware_valid(self):
        
        self.options.update(
            feeding_hiv_status=NO,
            hiv_status_aware='blah')
        
        form_validator = BreastFeedingQuestionnaireFormValidator(cleaned_data=self.options)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}') 
        
       
    def test_on_hiv_status_aware_required(self):
        
        self.options.update(
            feeding_hiv_status=NO,
            on_hiv_status_aware=None)
        
        form_validator = BreastFeedingQuestionnaireFormValidator(cleaned_data=self.options)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('on_hiv_status_aware',form_validator._errors)  
              
            
    def test_on_hiv_status_aware_valid(self):
        
        self.options.update(
            feeding_hiv_status=NO,
            on_hiv_status_aware='blah')
        
        form_validator = BreastFeedingQuestionnaireFormValidator(cleaned_data=self.options)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')      
        

    def test_hiv_status_known_by_required(self):
        
        self.options.update(
            hiv_status_during_preg=YES,
            hiv_status_known_by=None)
        
        form_validator = BreastFeedingQuestionnaireFormValidator(cleaned_data=self.options)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('hiv_status_known_by',form_validator._errors)  
              
    
    def test_hiv_status_known_by_valid(self):
        
        self.options.update(
            hiv_status_during_preg=YES,
            hiv_status_known_by='blah')
        
        form_validator = BreastFeedingQuestionnaireFormValidator(cleaned_data=self.options)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')   
    
    def test_influenced_during_preg_required(self):
        
        self.options.update(
            hiv_status_during_preg=NO,
            influenced_during_preg=None)
        
        form_validator = BreastFeedingQuestionnaireFormValidator(cleaned_data=self.options)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('influenced_during_preg',form_validator._errors)  
              
    def test_influenced_during_preg_valid(self):
        
        self.options.update(
            hiv_status_during_preg=NO,
            influenced_during_preg='blah')
        
        form_validator = BreastFeedingQuestionnaireFormValidator(cleaned_data=self.options)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')   
    
        
        
        