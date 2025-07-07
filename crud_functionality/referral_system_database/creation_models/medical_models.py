from django.db import models
from referral_system_database.default import DefaultModel
from referral_system_database.creation_models.master_models import ClinicalPrivilege


class MedicalCondition(DefaultModel):
    icd = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    status = models.BooleanField(default=False)
    head_name = models.CharField(max_length=100)
    sub_head_name = models.CharField(max_length=100)
    diagnosis = models.TextField(max_length=300, blank=True, null=True)

class ProgramMaster(DefaultModel):
    program_name = models.CharField(max_length=100)
    program_duration = models.IntegerField(null=True)
    clinical_privileges = models.ForeignKey(ClinicalPrivilege, on_delete=models.CASCADE, null=True, blank=True)

class Expert(DefaultModel):
    expert_name = models.CharField(max_length=100)
    expert_keywords = models.CharField(max_length=100)

    def __str__(self):
        return self.expert_name
