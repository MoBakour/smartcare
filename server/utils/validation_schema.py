from marshmallow import Schema, fields, validate

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