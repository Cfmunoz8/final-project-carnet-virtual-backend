from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Patient(db.Model):
    __tablename__ = "patients"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    rut = db.Column(db.String(100), nullable=False, unique=True)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(50))
    birth_date = db.Column(db.Date, nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    phone_number = db.Column(db.Integer, nullable=False)
    alive = db.Column(db.Boolean, default=True)
    caregiver = db.relationship("Caregiver", back_populates="patient", uselist=False)
    clinical_record = db.relationship("Clinical_record", back_populates="patient", uselist=False)


class Caregiver(db.Model):
    __tablename__ = "caregivers"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    rut = db.Column(db.String(100), nullable=False, unique=True)
    address = db.Column(db.String(200))
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.id"))
    patient = db.relationship("Patient", back_populates="caregiver")


class Clinical_record(db.Model):
    __tablename__ = "clinical_records"
    id = db.Column(db.Integer, primary_key=True)
    program = db.Column(db.String(100))
    registration_date = db.Column(db.Date)
    barthel_index = db.Column(db.String(100), nullable=False)
    zarit_scale_caregiver = db.Column(db.String(100))
    number_of_controls = db.Column(db.Integer)
    last_control_date = db.Column(db.Date, nullable=False)
    drugs = db.relationship("Drug")
    pathologies = db.relationship("Pahology")
    surgeries = db.relationship("Surgery")
    alergies = db.relationship("Alergy")
    habits = db.relationship("Habit", back_populates="clinical_record", uselist=False)
    controls = db.relationship("Control", back_populates="clinical_record")
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.id"))
    patient = db.relationship("Patient", back_populates="clinical_record")


class Drug(db.Model):
    __tablename__ = "drugs"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    posology = db.Column(db.String(100), nullable=False)
    clinical_record_id = db.Column(db.Integer, db.ForeignKey("clinical_records.id"), nullable=False)


class Pathology(db.Model):
    __tablename__ = "pathologies"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    clinical_record_id = db.Column(db.Integer, db.ForeignKey("clinical_records.id"), nullable=False)


class Surgery(db.Model):
    __tablename__ = "surgeries"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    clinical_record_id = db.Column(db.Integer, db.ForeignKey("clinical_records.id"), nullable=False)


class Alergy(db.Model):
    __tablename__ = "alergies"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    clinical_record_id = db.Column(db.Integer, db.ForeignKey("clinical_records.id"), nullable=False)


class Habit(db.Model):
    __tablename__ = "habits"
    id = db.Column(db.Integer, primary_key=True)
    smoke = db.Column(db.Boolean, default=False)
    alcohol = db.Column(db.Boolean, default=False)
    other_drugs = db.Column(db.String(100))
    clinical_record_id = db.Column(db.Integer, db.ForeignKey("clinical_records.id"), nullable=False)
    clinical_record = db.relationship("Clinical_record", back_populates="habit")


class Control(db.Model):
    __tablename__ = "controls"
    id = db.Column(db.Integer, primary_key=True)   
    reason = db.Column(db.String(100), nullable=False)
    description =db.Column(db.String(1000), nullable=False)
    indications =db.Column(db.String(1000), nullable=False)
    date = db.Column(db.Date, nullable=False)
    professional = db.relationship("Professional",back_populates="control")
    professional_id = db.Column(db.Integer, db.ForeignKey("professionals.id"), nullable=False)
    clinical_record_id = db.Column(db.Integer, db.ForeignKey("clinical_records.id"), nullable=False)


class Professional(db.Model):
    __tablename__ = "professionals"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    rut = db.Column(db.String(100), nullable=False, unique=True)
    role = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)
    control_id = db.Column(db.Integer, db.ForeignKey("controls.id"))
    control = db.relationship("Control", back_populates="professional")