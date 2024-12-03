from ..import db



class Organisation(db.Model):
    organisation_id = db.Column(db.Integer, primary_key=True)
    organisation_name = db.Column(db.String(100), nullable=False)
    organisation_address = db.Column(db.String(100), nullable=False)
    organisation_phone = db.Column(db.String(100), nullable=False)
    organisation_email = db.Column(db.String(100), nullable=False)
    organisation_website = db.Column(db.String(100), nullable=False)
    organisation_logo = db.Column(db.String(100), nullable=False)
    organisation_description = db.Column(db.String(100), nullable=False)
    organisation_type = db.Column(db.String(100), nullable=False)
    organisation_status = db.Column(db.String(100), nullable=False)
    organisation_created_at = db.Column(db.String(100), nullable=False)
    organisation_updated_at = db.Column(db.String(100), nullable=False)
    organisation_created_by = db.Column(db.String(100), nullable=False)
    organisation_updated_by = db.Column(db.String(100), nullable=False)
    organisation_deleted_at = db.Column(db.String(100), nullable=False)
    organisation_deleted_by = db.Column(db.String(100), nullable=False)
    organisation_deleted = db.Column(db.String(100), nullable=False)
