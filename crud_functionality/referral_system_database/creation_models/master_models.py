from django.db import models

class DefaultModel(models.Model):
    # Assume your DefaultModel has some common fields or methods
    class Meta:
        abstract = True

class HospitalType(DefaultModel):
    name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name

class WorkRole(DefaultModel):
    name = models.CharField(max_length=155, blank=True, null=True)

    def __str__(self):
        return self.name

class Employer(DefaultModel):
    name = models.CharField(max_length=155, blank=True, null=True)

    def __str__(self):
        return self.name

class ServiceCadre(DefaultModel):
    name = models.CharField(max_length=155, null=True, blank=True)

    def __str__(self):
        return self.name

class Speciality(DefaultModel):
    name = models.CharField(max_length=155, null=True, blank=True)

    def __str__(self):
        return self.name

class ExpertKeyword(DefaultModel):
    keyword = models.CharField(max_length=155, blank=True, null=True)

    def __str__(self):
        return self.keyword

class TrainingProvider(DefaultModel):
    name = models.CharField(max_length=155, blank=True, null=True)

    def __str__(self):
        return self.name

class Position(DefaultModel):
    name = models.CharField(max_length=155, blank=True, null=True)

    def __str__(self):
        return self.name
    
class Incharges(DefaultModel):
    name = models.CharField(max_length=155, blank=True, null=True)

    def __str__(self):
        return self.name

class CertificationProvider(DefaultModel):
    name = models.CharField(max_length=155, blank=True, null=True)

    def __str__(self):
        return self.name

class ClinicalPrivilege(DefaultModel):
    name = models.CharField(max_length=155, blank=True, null=True)

    def __str__(self):
        return self.name

class Empanelments(DefaultModel):
    name = models.CharField(max_length=155, blank=True, null=True)

    def __str__(self):
        return self.name

class HealthcareRecord(DefaultModel):
    hospital_type = models.ForeignKey(HospitalType, on_delete=models.CASCADE, null=True, blank=True)
    work_role = models.ForeignKey(WorkRole, on_delete=models.CASCADE, null=True, blank=True)
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE, null=True, blank=True)
    service_cadre = models.ForeignKey(ServiceCadre, on_delete=models.CASCADE, null=True, blank=True)
    speciality = models.ForeignKey(Speciality, on_delete=models.CASCADE, null=True, blank=True)
    expert_keywords = models.ForeignKey(ExpertKeyword, on_delete=models.CASCADE, blank=True, null=True)
    training_provider = models.ForeignKey(TrainingProvider, on_delete=models.CASCADE, null=True, blank=True)
    position = models.ForeignKey(Position, on_delete=models.CASCADE,null=True,blank=True)
    incharges = models.ForeignKey(Incharges, on_delete=models.CASCADE, null=True, blank=True)
    certification_provider = models.ForeignKey(CertificationProvider, on_delete=models.CASCADE, null=True, blank=True)
    clinical_privilege = models.ForeignKey(ClinicalPrivilege, on_delete=models.CASCADE, null=True, blank=True)
    empanelments = models.ForeignKey(Empanelments, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"Healthcare Record: {self.hospital_type} - {self.work_role}"