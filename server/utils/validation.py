from marshmallow import Schema, fields, validate, ValidationError, validates
import re

class WoundSchema(Schema):
    type = fields.String(required=True, validate=validate.OneOf([
        "Burn",
        "Puncture",
        "Abrasion",
        "Surgical Wound",
        "Ulcer",
        "Pressure Ulcer",
        "Diabetic Ulcer",
        "Laceration"
    ]))
    location = fields.String(required=True, validate=validate.OneOf([
        "Elbow",
        "Hand",
        "Head",
        "Shoulder",
        "Torso",
        "Knee",
        "Foot",
        "Back",
        "Arm",
        "Leg"
    ]))
    severity = fields.String(required=True, validate=validate.OneOf([
        "Moderate",
        "Mild",
        "Severe"
    ]))
    infected = fields.String(required=True, validate=validate.OneOf(["Yes", "No"]))
    size = fields.Float(required=True, as_string=True)
    treatment = fields.String(required=True, validate=validate.OneOf([
        "Surgical Debridement",
        "Antibiotics (Oral)",
        "Moist Wound Dressing",
        "Negative Pressure Wound Therapy",
        "Cleaning and Bandage",
        "No Treatment (for mild cases)",
        "Antibiotics (Topical)"
    ]))

class NewPatientSchema(Schema):
    supervisor = fields.String(required=True, validate=validate.Length(min=1))
    name = fields.String(required=True, validate=validate.Length(min=1))
    avatar = fields.String()
    gender = fields.String(required=True, validate=validate.OneOf([
        "Male",
        "Female"]))
    age = fields.Int(required=True, as_string=True)
    bed = fields.Int(required=True, as_string=True)
    department = fields.String(required=True, validate=validate.Length(min=1))
    blood_type = fields.String(required=True, validate=validate.Length(min=1))
    wound = fields.Nested(WoundSchema, required=True)



# custom validation functions

class ValidationError(Exception):
    def __init__(self, message):
        self.message = message
        self.type = "validation_error"


def validate_signup(data):
    error = ""    
        
    # password validation
    if not data["password"] or len(data["password"]) == 0:
        error = "Password is required"
    elif len(data["password"]) < 6:
        error = "Password must be at least 6 characters long"
        
    # email validation
    if not data["email"] or len(data["email"]) == 0:
        error = "Email is required"
    elif not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', data["email"]):
        error = "Invalid email address"

    # username validation
    if not data["username"] or len(data["username"]) == 0:
        error = "Username is required"
    elif len(data["username"]) > 24:
        error = "Username must be max 24 characters"
    elif len(data["username"]) < 3:
        error = "Username must be at least 3 characters long"

    if error:
        raise ValidationError(error)
    
    return True


def validate_login(data):
    error = ""    
        
    if not data["password"] or len(data["password"]) == 0:
        error = "Password is required"

    if not data["email"] or len(data["email"]) == 0:
        error = "Email is required"
        
    if error:
        raise ValidationError(error)
    
    return True

