import uuid

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

from .default import DefaultModel
from .creation_models.location_models import State, Block, District
from .creation_models.medical_models import  ProgramMaster, MedicalCondition, Expert
from .creation_models.master_models import Empanelments, HospitalType, Incharges, WorkRole, Employer, ServiceCadre, Speciality, TrainingProvider, Position


class StaffUserManager(BaseUserManager):
    """
        Manager for the StaffUser model, providing helper methods for creating users and superusers.
    """

    def create_user(self, email, password=None, **extra_fields):
        """
           Creates and returns a regular staff user.

           Args:
               email (str): Email of the user.
               password (str): Password of the user.
               extra_fields (dict): Additional fields to set on the user.

           Returns:
               StaffUser: The created staff user instance.
        """
        if not email:
            raise ValueError("The Email field must be set.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
            Creates and returns a superuser with elevated permissions.

            Args:
                email (str): Email of the superuser.
                password (str): Password of the superuser.
                extra_fields (dict): Additional fields to set on the user.

            Returns:
                StaffUser: The created superuser instance.
        """

        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')

        return self.create_user(email, password, **extra_fields)

    def create_site_admin(self, email, password=None, **extra_fields):
        extra_fields.setdefault('role', 'SITE_ADMIN')
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(email, password, **extra_fields)

    def create_hospital_admin(self, email, password=None, **extra_fields):
        extra_fields.setdefault('role', 'HOSPITAL_ADMIN')
        extra_fields.setdefault('is_staff', True)
        return self.create_user(email, password, **extra_fields)

    def create_staff_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('role', 'STAFF')
        return self.create_user(email, password, **extra_fields)


class StaffUser(DefaultModel, AbstractBaseUser, PermissionsMixin):
    """
        A model representing a staff user in the system.

        Attributes:
            GENDER_CHOICES (list): Available gender choices.
            STATUS_CHOICES (list): Available status choices.
            BLOOD_GROUP_CHOICES (list): Available blood group options.
            WORK_STATUS_CHOICES (list): Available work status options.
            SERVICE_STATUS_CHOICES (list): Available service status options.
            ROLE_CHOICES (list): Available roles status options.
    """

    GENDER_CHOICES = [
        ('MALE', 'Male'),
        ('FEMALAE', 'Female'),
        ('OTHERS', 'Other'),
    ]

    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('INACTIVE', 'Inactive'),
    ]

    BLOOD_GROUP_CHOICES = [
        ('AB-', 'AB-'),
        ('AB+', 'AB+'),
        ('O-', 'O-'),
        ('O+', 'O+'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('A-', 'A-'),
        ('A+', 'A+')
    ]

    WORK_STATUS_CHOICES = [
        ('AVAILABLE', 'Available'),
        ('ON-CALL', 'On Call'),
        ('OFF-DUTY', 'Off Duty'),
        ('ON-LEAVE', 'On Leave'),
        ('ON_MATERNITY-LEAVE', 'On Maternity Leave'),
        ('OUT-ON-ADMIN-DUTIES', 'Out On Admin Duties'),
        ('OUT-ON-TRAINING', 'Out On Training'),
        ('NOT-AVAILABLE', 'Not Available'),
        ('ABSCONDING', 'Absconding'),
        ('RETIRED', 'Retired'),
        ('OTHER', 'Other')
    ]

    SERVICE_STATUS_CHOICES = [
        ('REGULAR', 'Regular'),
        ('CONTRACTUAL', 'Contractual'),
        ('SHORT-SERVICE-BOND', 'Short Service Bond'),
        ('PART-TIME', 'Part Time'),
        ('OUTSOURCED', 'Outsourced'),
        ('PROBATIONARY','Probationary'),
        ('INTERN', 'Intern'),
        ('VALUTARY', 'Valuntary'),
        ('DEPUTATION', 'Deputation'),
        ('OTHER', 'Other')
    ]

    ROLE_CHOICES = [
        ('SITE_ADMIN', 'Site Admin'),
        ('HOSPITAL_ADMIN', 'Hospital Admin'),
        ('STAFF', 'Staff User'),
    ]

    full_name = models.CharField(
        max_length=255, null=True, blank=True,
        help_text="Full name of the staff user."
    )
    salutations = models.CharField(
        max_length=25, null=True, blank=True,
        help_text="Salutation for the staff user (e.g., Mr., Ms., Dr.)."
    )
    staff_user_id = models.CharField(
        max_length=25, unique=True,
        help_text="Unique identifier for the staff user."
    )

    mobile_number = models.CharField(
        max_length=12, null=True, blank=True,
        help_text="Mobile number of the staff user."
    )
    profile_picture = models.ImageField(
        upload_to='Staff_User_Profile_Picture/', null=True, blank=True,
        help_text="Profile picture of the staff user."
    )
    gender = models.CharField(
        max_length=25, choices=GENDER_CHOICES, null=True, blank=True,
        help_text="Gender of the staff user."
    )
    dob = models.DateField(
        null=True, blank=True,
        help_text="Date of birth of the staff user."
    )
    blood_group = models.CharField(
        max_length=25, choices=BLOOD_GROUP_CHOICES, null=True, blank=True,
        help_text="Blood group of the staff user."
    )
    emergency_contact_number = models.CharField(
        max_length=12, null=True, blank=True,
        help_text="Emergency contact number of the staff user."
    )
    email = models.EmailField(
        _('Email Address'), unique=True,
        help_text="Email address of the staff user."
    )

    # Work details
    medical_service_unit = models.ForeignKey(
        'MedicalServiceUnit', on_delete=models.SET_NULL, null=True,
        help_text="Medical service unit where the staff user works."
    )
    work_role = models.ForeignKey(
        WorkRole, on_delete=models.SET_NULL, null=True, blank=True, 
        help_text="Work role of the staff user in the organization."
    )
    work_status = models.CharField(
        max_length=25, choices=WORK_STATUS_CHOICES, null=True, blank=True,
        help_text="Current work status of the staff user."
    )

    # Service details
    service_joining_year = models.IntegerField(
        null=True, blank=True,
        help_text="Year the staff user joined the service."
    )
    employer = models.ForeignKey(
        Employer, on_delete=models.CASCADE, null=True, blank=True,
        help_text="Employer of the staff user."
    )
    service_status = models.CharField(
        max_length=25, choices=SERVICE_STATUS_CHOICES, null=True, blank=True,
        help_text="Current service status of the staff user."
    )
    service_cadre = models.ForeignKey(
        ServiceCadre, on_delete=models.CASCADE, null=True, blank=True,
        help_text="Service cadre of the staff user."
    )
    speciality = models.ForeignKey(
        Speciality, on_delete=models.CASCADE, null=True, blank=True,
        help_text="Speciality area of the staff user."
    )
    place_of_posting = models.ForeignKey(
        'Hospital', on_delete=models.SET_NULL, null=True, related_name='posted_staff',
        help_text="Hospital or facility where the staff user is currently posted."
    )
    position = models.ForeignKey(
        Position, on_delete=models.SET_NULL, null=True,
        help_text="Position held by the staff user."
    )
    
    expert = models.ManyToManyField(
        Expert,
        blank=True,
        help_text="Expertise areas of the staff user."
    )
    sign_in_status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='ACTIVE',
        help_text="Sign-in status of the staff user."
    )
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='ACTIVE',
        help_text="Overall status of the staff user in the system."
    )

    # Incharge settings
    unit_incharge = models.BooleanField(default=False, help_text='unit incharge in hospital')
    unit_nursing_incharge = models.BooleanField(default=False, help_text='nursing unit incharge of hospital')
    incharge_roles = models.ManyToManyField(Incharges, blank=True, help_text='Incharge roles held by the staff user.')

    # Permissions and other settings
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='STAFF')
    is_active = models.BooleanField(
        default=True,
        help_text="Indicates whether the user account is active."
    )
    is_staff = models.BooleanField(
        default=False,
        help_text="Indicates whether the user has staff-level permissions."
    )
    saved_hospitals = models.ManyToManyField('Hospital', help_text='List of saved hospitals by staff user')
    saved_experts = models.ManyToManyField('self', help_text='List of saved experts by staff user')

    USERNAME_FIELD = "email"

    objects = StaffUserManager()

    class Meta:
        verbose_name = _('staff user')
        verbose_name_plural = _('staff users')

    def __str__(self):
        """
            Returns the string representation of the staff user.

            Returns:
                str: Email of the staff user.
        """
        return self.email

    def save(self, *args, **kwargs):
        # Generate unique staff_user_id if not set
        if not self.staff_user_id:
            self.staff_user_id = str(uuid.uuid4())[:25]

        # Set staff status based on role
        if self.role in ['SITE_ADMIN', 'HOSPITAL_ADMIN']:
            self.is_staff = True

        super().save(*args, **kwargs)

    def has_perm(self, perm, obj=None):
        """
        Basic permission check based on role
        """
        return self.is_staff

    def has_module_perms(self, app_label):
        """
        Basic module permission check based on role
        """
        return self.is_staff

    @property
    def is_site_admin(self):
        return self.role == 'SITE_ADMIN'

    @property
    def is_hospital_admin(self):
        return self.role == 'HOSPITAL_ADMIN'

    @property
    def is_hospital_staff(self):
        return self.role == 'STAFF'


class StaffUserEducation(DefaultModel):
    """
        Model representing the educational background of a staff user.

        Attributes:
            staff_user (ForeignKey): A reference to the staff user who completed the education.
            program (ForeignKey): The program or course completed by the staff user.
            passing_year (IntegerField): The year the staff user completed the program.
            training_provider (ForeignKey): The institution or organization that provided the training.
            attachments (FileField): Optional file attachments related to the education (e.g., certificates).
    """
    staff_user = models.ForeignKey(
        'StaffUser', on_delete=models.CASCADE,
        help_text="The staff user associated with this education record."
    )
    program = models.ForeignKey(
        ProgramMaster, on_delete=models.PROTECT, null=True,
        help_text="The educational program or course completed by the staff user."
    )
    passing_year = models.IntegerField(
        help_text="The year the staff user completed the program."
    )
    training_provider = models.ForeignKey(
        TrainingProvider, on_delete=models.CASCADE, null=True,
        help_text="The institution or organization that provided the training."
    )
    attachments = models.FileField(
        upload_to='education/', null=True, blank=True,
        help_text="Optional file attachments, such as certificates or related documents."
    )

    def __str__(self):
        """
        Returns the string representation of the staff user's education.

        Returns:
            str: A combination of the staff user's email and program name.
        """
        return f"{self.staff_user.email} - {self.program}"

    class Meta:
        """
        Meta options for the StaffUserEducation model.

        Attributes:
            unique_together (list): Ensures the combination of staff_user, program, and passing_year is unique.
        """
        unique_together = ['staff_user', 'program', 'passing_year']


class Hospital(DefaultModel):
    """
    Model representing a hospital and its details.

    Attributes:
        STATUS_CHOICES (list): Operational status of the hospital (Active/Inactive).
        SETTING_CHOICES (list): Setting/location type (Rural, Urban, etc.).
        OWNERSHIP_CHOICES (list): Ownership type (Public, Private, etc.).
        hospital_name (CharField): Name of the hospital.
        hospital_id (CharField): Unique identifier, auto-generated, immutable.
        hospital_type (ForeignKey): Category/type of hospital.
        setting (CharField): Setting/location type.
        contact_number (CharField): Contact phone number.
        email (EmailField): Contact email.
        picture (ImageField): Optional image of the hospital.
        hospital_description (TextField): Optional description/details.
        ownership (CharField): Ownership type.
        empanelments (ForeignKey): Empanelment record (optional).
        org_facility_id (CharField): Organizational Facility ID (optional).
        state/district/block (ForeignKeys): Location hierarchy.
        city_or_village (CharField): City or village name.
        address (TextField): Detailed postal address.
        geo_lat/geo_long/geo_alt (DecimalFields): Geographical coordinates.
        status (CharField): Operational status (Active/Inactive).
        higher_facility (BooleanField): Flag if it's a higher facility.
        delivery_point (BooleanField): Flag if it's a delivery point.
        medical_service_unit (ManyToManyField): Linked medical service units.
        training_institute/fru/sncu/nbsu (BooleanFields): Facility flags.
    """

    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('INACTIVE', 'Inactive'),
    ]

    SETTING_CHOICES = [
        ('RURAL', 'Rural'),
        ('URBAN', 'Urban'),
        ('PERI-URBAN', 'Peri Urban'),
        ('MOBILE', 'Mobile'),
        ('OTHER', 'Other'),
    ]

    OWNERSHIP_CHOICES = [
        ('PUBLIC', 'Public'),
        ('PRIVATE', 'Private'),
        ('PPP', 'PPP'),
        ('CHARITABLE', 'Charitable'),
        ('PUBLIC_FOR_EMPLOYEES', 'Public For Employees'),
        ('PRIVATE_FOR_EMPLOYEES', 'Private For Employees'),
        ('OTHER', 'Others'),
    ]

    # Basic Information
    hospital_name = models.CharField(
        max_length=255,
        db_index=True,  # Frequently searched field
        help_text="The name of the hospital."
    )

    hospital_id = models.CharField(
        max_length=25, unique=True,
        help_text="A unique identifier for the hospital, auto-generated."
    )

    hospital_type = models.ForeignKey(
        HospitalType, on_delete=models.CASCADE, null=True,
        help_text="The type or category of the hospital."
    )

    setting = models.CharField(
        max_length=255, choices=SETTING_CHOICES, blank=True, null=True, db_index=True,
        help_text="The setting of the hospital (e.g., Rural, Urban)."
    )

    contact_number = models.CharField(
        max_length=12, null=True, blank=True,
        help_text="The contact phone number of the hospital."
    )

    email = models.EmailField(
        null=True, blank=True,
        help_text="The contact email address of the hospital."
    )

    picture = models.ImageField(
        upload_to='Hospital_Picture/', null=True, blank=True,
        help_text="Optional image of the hospital."
    )

    hospital_description = models.TextField(
        null=True, blank=True,
        help_text="Optional description providing details about the hospital."
    )

    ownership = models.CharField(
        max_length=255, choices=OWNERSHIP_CHOICES, blank=True, null=True, db_index=True,
        help_text="Ownership type of the hospital."
    )

    empanelments = models.ForeignKey(
        Empanelments, on_delete=models.CASCADE, null=True, blank=True,
        help_text="Empanelment record of the hospital (if applicable)."
    )

    org_facility_id = models.CharField(
        max_length=50, null=True, blank=True, db_index=True,
        help_text="Organizational Facility ID (if applicable)."
    )

    # Location Information
    state = models.ForeignKey(
        State, on_delete=models.PROTECT, default=None, null=True,
        help_text="The state where the hospital is located."
    )

    district = models.ForeignKey(
        District, on_delete=models.PROTECT, default=None, null=True,
        help_text="The district where the hospital is located."
    )

    block = models.ForeignKey(
        Block, on_delete=models.PROTECT, default=None, null=True,
        help_text="The block where the hospital is located."
    )

    city_or_village = models.CharField(
        max_length=255, null=True, blank=True, db_index=True,
        help_text="The city or village where the hospital is located."
    )

    address = models.TextField(
        null=True, blank=True,
        help_text="The detailed postal address of the hospital."
    )

    # Geolocation Information
    geo_lat = models.DecimalField(
        max_digits=8, decimal_places=6, null=True, blank=True,
        help_text="Latitude of the hospital's location."
    )

    geo_long = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True,
        help_text="Longitude of the hospital's location."
    )

    geo_alt = models.DecimalField(
        max_digits=10, decimal_places=6, null=True, blank=True,
        help_text="Altitude of the hospital's location."
    )

    # Operational Information
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='ACTIVE', db_index=True,
        help_text="Operational status of the hospital (Active/Inactive)."
    )

    higher_facility = models.BooleanField(
        default=False,
        help_text="Indicates whether the hospital is a higher-level facility."
    )

    delivery_point = models.BooleanField(
        default=False,
        help_text="Indicates whether the hospital serves as a delivery point."
    )

    medical_service_unit = models.ManyToManyField(
        'MedicalServiceUnit',
        help_text="Medical service units associated with the hospital.", through='HospitalMedicalServiceUnit'
    )

    # Additional Facility Flags
    training_institure = models.BooleanField(
        default=False,
        help_text="Indicates if the hospital is a training institute."
    )

    fru = models.BooleanField(
        default=False,
        help_text="Indicates if the hospital is a First Referral Unit."
    )

    sncu = models.BooleanField(
        default=False,
        help_text="Indicates if the hospital has a Special Newborn Care Unit."
    )

    nbsu = models.BooleanField(
        default=False,
        help_text="Indicates if the hospital has a Newborn Stabilization Unit."
    )

    class Meta:
        """
        Meta options for the Hospital model.

        Attributes:
            ordering (tuple): Default ordering of hospital objects by ID.
        """
        ordering = ('id',)

    def __str__(self):
        """
        Returns the string representation of the hospital.

        Returns:
            str: The name of the hospital.
        """
        return self.hospital_name


class MedicalServiceUnit(DefaultModel):
    """
        Model representing a medical service unit.

        Attributes:
            STATUS_CHOICES (list): Status options for the medical service unit (e.g., Active, Inactive).
            msu_name (CharField): The name or title of the medical service unit.
            msu_picture (ImageField): Optional image of the medical service unit.
            msu_description (TextField): Optional description providing details about the medical service unit.
            status (CharField): The operational status of the medical service unit (e.g., Active, Inactive).
    """
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('INACTIVE', 'Inactive'),
    ]

    msu_name = models.CharField(
        max_length=255, db_index=True,
        help_text="The name or title of the medical service unit."
    )
    msu_picture = models.ImageField(
        upload_to='MSU_Picture/', null=True, blank=True,
        help_text="Optional image of the medical service unit."
    )
    msu_description = models.TextField(
        null=True, blank=True,
        help_text="Optional description providing details about the medical service unit."
    )
    msu_department = models.CharField(
        null=True, blank=True, 
        help_text='Optional department provided',
        max_length=255
    )
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='ACTIVE', db_index=True,
        help_text="The operational status of the medical service unit (e.g., Active, Inactive)."
    )

    def __str__(self):
        """
            Returns the string representation of the medical service unit.

            Returns:
                str: The name of the medical service unit.
        """
        return self.msu_name
    

class HospitalMedicalServiceUnit(models.Model):
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    msu = models.ForeignKey(MedicalServiceUnit, on_delete=models.CASCADE)

    # dynamic fields — specific to this hospital–MSU pair:
    msu_services = models.TextField(null=True, blank=True)
    bed_count = models.IntegerField(null=True, blank=True)
    contact_number = models.CharField(max_length=15, null=True, blank=True)
    empanelments = models.TextField(null=True, blank=True)

    class Meta:
        unique_together = ('hospital', 'msu')


class HospitalIncharge(models.Model):
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    staff_user = models.ForeignKey(StaffUser, on_delete=models.CASCADE)
    incharge_role = models.ForeignKey(Incharges, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('hospital', 'incharge_role')


class File(DefaultModel):
    """
        Model representing a generic file upload.

        Attributes:
            file (FileField): A file to be uploaded, stored in the specified directory.
    """
    file = models.FileField(
        upload_to='file/', null=True, blank=True,
        help_text="A file to be uploaded, stored in the 'file/' directory."
    )

class CaseStatus(DefaultModel):
    CASE_STATUS_CHOICES = [
        ('IN-TRANSIT', 'In Transit'),
        ('RETURN-DISCHARGE', 'Return Discharge'),
        ('TRIAGE-CARE', 'Triage Care'),
        ('OPD_CARE', 'OPD Care'),
        ('DAY-CARE-ADMISSION', 'Day Care Admission'),
        ('IPD-ADMISSION', 'IPD Admission'),
        ('DISCHARGED', 'Discharged'),
        ('REFERRED', 'Referred'),
        ('LAMA', 'LAMA'),
        ('DEMISE', 'Demise'),
        ('DID-NOT-ARRIVE', 'Did Not Arrive'),
        ('OTHER', 'Other')
    ]
    SITE_OF_DEMISE_CHOICES = [
        ('IN-TRANSIT', 'In Transit'),
        ('IN-HOSPITAL', 'In Hospital'),
        ('HOME', 'Home'),
        ('IN-EMERGENCY-ROOM', 'In Emergency Room'),
        ('OTHER', 'Other')
    ]
    case_file = models.ForeignKey('CaseFile',on_delete=models.CASCADE)
    status = models.CharField(choices=CASE_STATUS_CHOICES, default='IN-TRANSIT', max_length=255)
    datetime = models.DateTimeField(auto_now=True)
    medical_condition = models.TextField(max_length=300, blank=True, null=True)
    note = models.TextField(max_length=300, blank=True, null=True)
    side_of_demise = models.CharField(choices=SITE_OF_DEMISE_CHOICES,max_length=20,blank=True,null=True)
    referral = models.ForeignKey('Referral',on_delete=models.CASCADE,null=True,blank=True)


class CaseFile(DefaultModel):
    """
        Model representing a case file for a patient.
    """
    GENDER_CHOICES = [
        ('MALE', 'Male'),
        ('FEMALE', 'Female'),
        ('OTHERS', 'Other'),
    ]

    patient_name = models.CharField(
        max_length=550,
        help_text="The full name of the patient."
    )

    years = models.IntegerField(
        null=True,
        help_text="The number of years of the patient's age."
    )

    months = models.IntegerField(
        null=True,
        help_text="The number of months of the patient's age."
    )

    gender = models.CharField(
        max_length=20, choices=GENDER_CHOICES,
        help_text="The gender of the patient (e.g., Male, Female, Other)."
    )
    patient_attendant_name = models.CharField(
        max_length=55,
        help_text="The name of the attendant accompanying the patient."
    )
    patient_attendant_relation = models.CharField(
        max_length=55,
        help_text="The relationship of the attendant to the patient."
    )
    contact_number = models.CharField(
        max_length=12,
        help_text="The contact number of the patient or attendant."
    )
    medical_condition = models.ForeignKey(
        MedicalCondition, on_delete=models.CASCADE, null=True,
        help_text="The medical condition associated with the patient."
    )


class IntermediatesStatusClass(DefaultModel):
    case_file = models.ForeignKey(CaseFile, on_delete=models.CASCADE)
    case_status = models.ForeignKey(CaseStatus, on_delete=models.CASCADE)



class Referral(DefaultModel):
    """
        Model representing a patient referral process.
    """
    TRANSPORT_MODE_CHOICES = [
        ('108-AMBULANCE', '108 Ambulance'),
        ('PAID-AMBULANCE', 'Paid Ambulance'),
        ('HIRED-VEHICLE', 'Hired Vehicle'),
        ('SELF', 'Self'),
        ('OTHER', 'Other')
    ]

    SITE_OF_DEMISE_CHOICES = [
        ('IN-TRANSIT', 'In Transit'),
        ('IN-HOSPITAL', 'In Hospital'),
        ('HOME', 'Home'),
        ('IN-EMERGENCY-ROOM', 'In Emergency Room'),
        ('OTHER', 'Other')
    ]
    
    case_notes = models.TextField(
        null=True,
        blank=True,
        max_length=5000,
        help_text="Notes about the case."
    )
    referral_reason = models.TextField(
        null=True,
        blank=True,
        max_length=5000,
        help_text="Reason for the referral."
    )
    attachments_referral_form = models.ManyToManyField(
        File,
        related_name='attachments_referral_form',
        help_text="Referral form attachments.",

    )
    attachments_investigation_reports = models.ManyToManyField(
        File,
        related_name='attachments_investigation_reports',
        help_text="Attachments of investigation reports."
    )
    advance_information_send = models.BooleanField(
        default=False,
        help_text="Whether advance information was sent to the referred hospital."
    )
    referred_facility_staff_informed_person_name = models.CharField(
        default='',
        null=True,
        blank=True,
        max_length=255
    )
    referred_facility_staff_informed = models.BooleanField(
        default=False,
        help_text="Whether the referred hospital staff has been informed."
    )
    transport_mode = models.CharField(
        max_length=40,
        choices=TRANSPORT_MODE_CHOICES,
        null=True,
        help_text="Mode of transport used during the referral."
    )
    referred_hospital = models.ForeignKey(
        Hospital,
        on_delete=models.CASCADE,
        related_name='referred_hospital',
        null=True,
        help_text="The hospital to which the patient is referred."
    )
    source_hospital = models.ForeignKey(
        Hospital,
        on_delete=models.CASCADE,
        related_name='source_hospital',
        null=True,
        help_text="The hospital from which the patient is referred."
    )
    datetime = models.DateTimeField(
        default=timezone.now,
        help_text="The timestamp of the referral."
    )
    referred_by = models.ForeignKey(
        StaffUser,
        on_delete=models.CASCADE,
        null=True,
        help_text="The staff user who referred the patient."
    )
    site_of_demise = models.CharField(
        max_length=155, 
        choices = SITE_OF_DEMISE_CHOICES,
        null=True,
        help_text="Site of demise, if applicable (linked to a healthcare record)."
    )
    medical_Service_Unit = models.ForeignKey(
        MedicalServiceUnit,
        on_delete=models.CASCADE,
        null=True,
        help_text="The medical service unit associated with the referral."
    )


class CaseFollowUp(DefaultModel):
    """
        Model representing a follow-up on a patient case.
    """
    CALL_NOT_ANSWERED_CHOICES = [
        ('SWITCH-OFF', 'Switch Off'),
        ('NOT-REACHABLE', 'Not Reachable'),
        ('OUT-OF-NETWORK', 'Out Of Network'),
        ('NOT-CONNECTED', 'Not Connected'),
        ('LINE-BUSY', 'Line Busy'),
        ('NO-RESPONSE', 'No Response'),
        ('PHONE-PICKED-AND-DISCONNECTED', 'Phone Picked And Disconnected'),
        ('INVALID-NUMBER', 'Invalid Number'),
        ('INCOMING-NOT-AVAILABLE', 'Incoming Not Available'),
        ('DO-NOT-DISTURB', 'Do Not Disturb'),
        ('OTHER', 'Other')
    ]

    CASE_LOCATION_CHOICES = [
        ('REACHED-REFERRED-HOSPITAL', 'Reached Referred Hospital'),
        ('IN-TRANSIT', 'In Transit'),
        ('REACHED-ANOTHER-HOSPITAL', 'Reached Another Hospital'),
        ('GOING-TO-ANOTHER-HOSPITAL', 'Going To Another Hospital'),
        ('DEMISE', 'Demise'),
        ('HOME', 'Home'),
        ('OTHER', 'Other')
    ]

    PATIENT_STATUS_CHOICES = [
        ('HEALTHY', 'Healthy'),
        ('RECOVERING', 'Recovering'),
        ('SICK', 'Sick'),
        ('DEMISE', 'Demise'),
        ('NO-RESPONSE', 'No Response'),
        ('DECLINED-TO-TALK' ,'Declined to Talk'),
        ('OTHER', 'Other')
    ]

    caller_staff_id = models.ForeignKey(
        StaffUser,
        on_delete=models.CASCADE,
        null=True,
        help_text="The staff user who made the follow-up call."
    )
    call_date = models.DateTimeField(
        default=timezone.now,
        help_text="The date and time of the follow-up call."
    )
    call_answered = models.BooleanField(
        default=False,
        help_text="Whether the follow-up call was answered."
    )
    call_not_answered_reasons = models.CharField(
        max_length=55,
        choices=CALL_NOT_ANSWERED_CHOICES,
        null=True,
        blank=True,
        help_text="Reason for an unanswered call."
    )
    case_status = models.ForeignKey(
        Referral,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text="The status of the associated referral case."
    )
    case_location = models.CharField(
        max_length=55,
        choices=CASE_LOCATION_CHOICES,
        null=True,
        blank=True,
        help_text="The location status of the patient."
    )
    support_required = models.BooleanField(
        default=False,
        help_text="Whether additional support was required."
    )
    support_notes = models.TextField(
        null=True,
        blank=True,
        max_length=500,
        help_text="Notes about the required support."
    )
    grievance_reported = models.BooleanField(
        default=False,
        help_text="Whether a grievance was reported."
    )
    grievance_notes = models.TextField(
        null=True,
        blank=True,
        max_length=500,
        help_text="Notes about the grievance, if reported."
    )
    call_close_time = models.DateTimeField(
        null=True,
        blank=True,
        help_text="The time the call was closed."
    )
    patient_status = models.CharField(
        max_length=55,
        choices=PATIENT_STATUS_CHOICES,
        null=True,
        blank=True,
        help_text="The health status of the patient."
    )


class Logging(models.Model):
    """
        Model representing system logs.

        Attributes:
            LoggingID (AutoField): Primary key for the log entry.
            LogLevel (CharField): The severity level of the log (e.g., INFO, WARNING, ERROR).
            LogActivity (CharField): A short description of the activity being logged.
            LogData (CharField): Additional data related to the logged activity.
            LogDetails (CharField): Detailed description of the logged event.
    """
    LoggingID = models.AutoField(primary_key=True)
    LogLevel = models.CharField(
        max_length=500,
        default="INFO",
        help_text="The severity level of the log (e.g., INFO, WARNING, ERROR)."
    )
    LogActivity = models.CharField(
        max_length=500,
        default="Log Activity",
        help_text="A short description of the activity being logged."
    )
    LogData = models.CharField(
        max_length=500,
        default="Log Data",
        help_text="Additional data related to the logged activity."
    )
    LogDetails = models.CharField(
        max_length=500,
        default="Log Details",
        help_text="Detailed description of the logged event."
    )
