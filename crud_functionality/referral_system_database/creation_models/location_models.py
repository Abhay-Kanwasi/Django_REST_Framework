from django.db import models

from referral_system_database.default import DefaultModel


class State(DefaultModel):
    state_name = models.CharField(max_length=255, unique=True)
    num_code = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.state_name

    def title(self):
        return self.state_name

class District(DefaultModel):
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='districts')
    district_name = models.CharField(max_length=255, blank=True)
    district_num_code = models.CharField(max_length=255, unique=True, blank=True)

    def __str__(self):
        return f"{self.district_name}, {self.state.state_name}"


class Block(DefaultModel):
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='blocks')
    block_name = models.CharField(max_length=255)
    block_num_code = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f"{self.block_name}, {self.district.district_name}"


