from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Company(db.Model):

    __tablename__ = "companies"

    id = db.Column(db.Integer, primary_key=True)

    company_name = db.Column(db.String(200), nullable=False)

    booth_number = db.Column(db.String(50))

    category = db.Column(db.String(100))

    contact_person = db.Column(db.String(100))

    phone = db.Column(db.String(20))

    whatsapp = db.Column(db.String(20))

    email = db.Column(db.String(150))

    website = db.Column(db.String(200))

    address = db.Column(db.Text)

    notes = db.Column(db.Text)

    rating = db.Column(db.Integer, default=3)

    priority = db.Column(db.String(20), default="Medium")

    followup = db.Column(db.String(30))

    favorite = db.Column(db.Boolean, default=False)

    tags = db.Column(db.String(300))

    # Business Information
    gst_number = db.Column(db.String(30))
    company_type = db.Column(db.String(100))
    country = db.Column(db.String(100))
    state = db.Column(db.String(100))
    city = db.Column(db.String(100))
    postal_code = db.Column(db.String(20))
    
    # Social Media
    linkedin = db.Column(db.String(250))
    facebook = db.Column(db.String(250))
    instagram = db.Column(db.String(250))
    
    # Business
    employee_count = db.Column(db.Integer)
    annual_revenue = db.Column(db.String(100))
    
    # Exhibition
    meeting_status = db.Column(db.String(50), default="Visited")
    company_score = db.Column(db.Integer, default=50)

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    products = db.relationship(
        "Product",
        backref="company",
        cascade="all, delete-orphan",
        lazy=True
    )

    contacts = db.relationship(
        "Contact",
        backref="company",
        cascade="all, delete-orphan",
        lazy=True
    )

    photos = db.relationship(
        "Photo",
        backref="company",
        cascade="all, delete-orphan",
        lazy=True
    )


class Product(db.Model):

    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)

    company_id = db.Column(
        db.Integer,
        db.ForeignKey("companies.id"),
        nullable=False
    )

    product_name = db.Column(db.String(200))

    product_category = db.Column(db.String(100))

    wholesale_price = db.Column(db.Float)

    retail_price = db.Column(db.Float)

    moq = db.Column(db.Integer)

    material = db.Column(db.String(100))

    description = db.Column(db.Text)


class Contact(db.Model):

    __tablename__ = "contacts"

    id = db.Column(db.Integer, primary_key=True)

    company_id = db.Column(
        db.Integer,
        db.ForeignKey("companies.id"),
        nullable=False
    )

    name = db.Column(db.String(100))

    designation = db.Column(db.String(100))

    phone = db.Column(db.String(20))

    email = db.Column(db.String(150))


class Photo(db.Model):

    __tablename__ = "photos"

    id = db.Column(db.Integer, primary_key=True)

    company_id = db.Column(
        db.Integer,
        db.ForeignKey("companies.id"),
        nullable=False
    )

    image = db.Column(db.String(250))

    image_type = db.Column(db.String(50))

    uploaded_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )