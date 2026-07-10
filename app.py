from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

import os
import uuid

from werkzeug.utils import secure_filename

from config import Config
from models import (
    db,
    Company,
    Product,
    Contact,
    Photo
)

# --------------------------------------------------
# App Configuration
# --------------------------------------------------

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

with app.app_context():
    db.create_all()

# Create upload folder only when running locally
if __name__ == "__main__":
    os.makedirs(
        app.config["UPLOAD_FOLDER"],
        exist_ok=True
    )

    with app.app_context():
        db.create_all()

# --------------------------------------------------
# Upload Settings
# --------------------------------------------------

ALLOWED_EXTENSIONS = {
    "png",
    "jpg",
    "jpeg",
    "gif",
    "webp"
}


def allowed_file(filename):

    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in ALLOWED_EXTENSIONS
    )


# --------------------------------------------------
# Dashboard
# --------------------------------------------------

# @app.route("/")
# def dashboard():

#     companies = (
#         Company.query
#         .order_by(Company.created_at.desc())
#         .limit(10)
#         .all()
#     )

#     stats = {

#         "companies": Company.query.count(),

#         "products": Product.query.count(),

#         "contacts": Contact.query.count(),

#         "photos": Photo.query.count(),

#         "favorites":
#             Company.query.filter_by(
#                 favorite=True
#             ).count(),

#         "high":
#             Company.query.filter_by(
#                 priority="High"
#             ).count(),

#         "medium":
#             Company.query.filter_by(
#                 priority="Medium"
#             ).count(),

#         "low":
#             Company.query.filter_by(
#                 priority="Low"
#             ).count()

#     }

#     return render_template(
#         "dashboard.html",
#         companies=companies,
#         stats=stats
#     )

@app.route("/")
def dashboard():

    companies = (
        Company.query
        .order_by(Company.created_at.desc())
        .limit(10)
        .all()
    )

    stats = {
        "companies": Company.query.count(),
        "products": Product.query.count(),
        "contacts": Contact.query.count(),
        "photos": Photo.query.count(),
        "favorites": Company.query.filter_by(favorite=True).count(),
        "high": Company.query.filter_by(priority="High").count(),
        "medium": Company.query.filter_by(priority="Medium").count(),
        "low": Company.query.filter_by(priority="Low").count(),
    }

    return render_template(
        "dashboard.html",
        companies=companies,
        stats=stats
    )
# --------------------------------------------------
# Companies
# --------------------------------------------------

@app.route("/companies")
def companies():

    search = request.args.get(
        "search",
        ""
    ).strip()

    query = Company.query

    if search:

        query = query.filter(

            (Company.company_name.contains(search))

            |

            (Company.category.contains(search))

            |

            (Company.contact_person.contains(search))

            |

            (
                Company.tags.is_not(None)
                &
                Company.tags.contains(search)
            )

            |

            (
                Company.website.is_not(None)
                &
                Company.website.contains(search)
            )

        )

    companies = query.order_by(
        Company.company_name
    ).all()

    return render_template(
        "companies.html",
        companies=companies,
        search=search
    )


@app.route("/company/<int:id>")
def company(id):

    company = Company.query.get_or_404(id)

    return render_template(
        "company.html",
        company=company
    )


@app.route(
    "/add-company",
    methods=["GET", "POST"]
)
def add_company():

    if request.method == "POST":

        company = Company(

            company_name=request.form.get(
                "company_name"
            ),

            booth_number=request.form.get(
                "booth_number"
            ),

            category=request.form.get(
                "category"
            ),

            contact_person=request.form.get(
                "contact_person"
            ),

            phone=request.form.get(
                "phone"
            ),

            whatsapp=request.form.get(
                "whatsapp"
            ),

            email=request.form.get(
                "email"
            ),

            website=request.form.get(
                "website"
            ),

            address=request.form.get(
                "address"
            ),

            notes=request.form.get(
                "notes"
            ),

            rating=int(
                request.form.get(
                    "rating",
                    3
                )
            ),

            priority=request.form.get(
                "priority"
            ),

            followup=request.form.get(
                "followup"
            ),

            favorite="favorite" in request.form,

            tags=request.form.get(
                "tags"
            ),

            gst_number=request.form.get(
                "gst_number"
            ),

            company_type=request.form.get(
                "company_type"
            ),

            country=request.form.get(
                "country"
            ),

            state=request.form.get(
                "state"
            ),

            city=request.form.get(
                "city"
            ),

            postal_code=request.form.get(
                "postal_code"
            ),

            linkedin=request.form.get(
                "linkedin"
            ),

            facebook=request.form.get(
                "facebook"
            ),

            instagram=request.form.get(
                "instagram"
            ),

            employee_count=int(
                request.form.get(
                    "employee_count"
                ) or 0
            )

        )

        try:

            db.session.add(company)
            db.session.commit()

            flash(
                "Company Added Successfully",
                "success"
            )

            return redirect(
                url_for("companies")
            )

        except Exception as e:

            db.session.rollback()

            flash(
                f"Error: {e}",
                "danger"
            )

    return render_template(
        "add_company.html"
    )

# --------------------------------------------------
# Edit Company
# --------------------------------------------------

@app.route(
    "/edit-company/<int:id>",
    methods=["GET", "POST"]
)
def edit_company(id):

    company = Company.query.get_or_404(id)

    if request.method == "POST":

        company.company_name = request.form.get("company_name")
        company.booth_number = request.form.get("booth_number")
        company.category = request.form.get("category")
        company.contact_person = request.form.get("contact_person")
        company.phone = request.form.get("phone")
        company.whatsapp = request.form.get("whatsapp")
        company.email = request.form.get("email")
        company.website = request.form.get("website")
        company.address = request.form.get("address")
        company.notes = request.form.get("notes")

        company.gst_number = request.form.get("gst_number")
        company.company_type = request.form.get("company_type")
        company.country = request.form.get("country")
        company.state = request.form.get("state")
        company.city = request.form.get("city")
        company.postal_code = request.form.get("postal_code")

        company.linkedin = request.form.get("linkedin")
        company.facebook = request.form.get("facebook")
        company.instagram = request.form.get("instagram")

        company.employee_count = int(
            request.form.get("employee_count") or 0
        )

        company.rating = int(
            request.form.get("rating", 3)
        )

        company.priority = request.form.get("priority")
        company.followup = request.form.get("followup")
        company.favorite = "favorite" in request.form
        company.tags = request.form.get("tags")

        try:

            db.session.commit()

            flash(
                "Company Updated Successfully",
                "success"
            )

            return redirect(
                url_for(
                    "company",
                    id=id
                )
            )

        except Exception as e:

            db.session.rollback()

            flash(
                f"Error: {e}",
                "danger"
            )

    return render_template(
        "edit_company.html",
        company=company
    )


# --------------------------------------------------
# Delete Company
# --------------------------------------------------

@app.route("/delete-company/<int:id>")
def delete_company(id):

    company = Company.query.get_or_404(id)

    try:

        db.session.delete(company)
        db.session.commit()

        flash(
            "Company Deleted Successfully",
            "success"
        )

    except Exception as e:

        db.session.rollback()

        flash(
            f"Error: {e}",
            "danger"
        )

    return redirect(
        url_for("companies")
    )


# --------------------------------------------------
# Products
# --------------------------------------------------

@app.route("/products")
def products():

    products = Product.query.order_by(
        Product.id.desc()
    ).all()

    return render_template(
        "products.html",
        products=products
    )


@app.route(
    "/company/<int:id>/add-product",
    methods=["GET", "POST"]
)
def add_product(id):

    company = Company.query.get_or_404(id)

    if request.method == "POST":

        product = Product(

            company_id=id,

            product_name=request.form.get(
                "product_name"
            ),

            product_category=request.form.get(
                "product_category"
            ),

            wholesale_price=float(
                request.form.get(
                    "wholesale_price"
                ) or 0
            ),

            retail_price=float(
                request.form.get(
                    "retail_price"
                ) or 0
            ),

            moq=int(
                request.form.get(
                    "moq"
                ) or 0
            ),

            material=request.form.get(
                "material"
            ),

            description=request.form.get(
                "description"
            )

        )

        try:

            db.session.add(product)
            db.session.commit()

            flash(
                "Product Added Successfully",
                "success"
            )

            return redirect(
                url_for(
                    "company",
                    id=id
                )
            )

        except Exception as e:

            db.session.rollback()

            flash(
                f"Error: {e}",
                "danger"
            )

    return render_template(
        "add_product.html",
        company=company
    )


@app.route("/delete-product/<int:id>")
def delete_product(id):

    product = Product.query.get_or_404(id)

    company_id = product.company_id

    try:

        db.session.delete(product)
        db.session.commit()

        flash(
            "Product Deleted",
            "success"
        )

    except Exception as e:

        db.session.rollback()

        flash(
            f"Error: {e}",
            "danger"
        )

    return redirect(
        url_for(
            "company",
            id=company_id
        )
    )


# --------------------------------------------------
# Contacts
# --------------------------------------------------

@app.route("/contacts")
def contacts():

    contacts = Contact.query.order_by(
        Contact.name
    ).all()

    return render_template(
        "contacts.html",
        contacts=contacts
    )


@app.route(
    "/company/<int:id>/add-contact",
    methods=["GET", "POST"]
)
def add_contact(id):

    company = Company.query.get_or_404(id)

    if request.method == "POST":

        contact = Contact(

            company_id=id,

            name=request.form.get("name"),

            designation=request.form.get(
                "designation"
            ),

            phone=request.form.get("phone"),

            email=request.form.get("email")

        )

        try:

            db.session.add(contact)
            db.session.commit()

            flash(
                "Contact Added Successfully",
                "success"
            )

            return redirect(
                url_for(
                    "company",
                    id=id
                )
            )

        except Exception as e:

            db.session.rollback()

            flash(
                f"Error: {e}",
                "danger"
            )

    return render_template(
        "add_contact.html",
        company=company
    )


@app.route("/delete-contact/<int:id>")
def delete_contact(id):

    contact = Contact.query.get_or_404(id)

    company_id = contact.company_id

    try:

        db.session.delete(contact)
        db.session.commit()

        flash(
            "Contact Deleted",
            "success"
        )

    except Exception as e:

        db.session.rollback()

        flash(
            f"Error: {e}",
            "danger"
        )

    return redirect(
        url_for(
            "company",
            id=company_id
        )
    )

# --------------------------------------------------
# Gallery
# --------------------------------------------------

@app.route("/gallery")
def gallery():

    photos = Photo.query.order_by(
        Photo.uploaded_at.desc()
    ).all()

    return render_template(
        "gallery.html",
        photos=photos
    )


@app.route(
    "/company/<int:id>/upload-photo",
    methods=["GET", "POST"]
)
def upload_photo(id):

    company = Company.query.get_or_404(id)

    if request.method == "POST":

        file = request.files.get("image")

        if not file or file.filename == "":
            flash(
                "Please select an image.",
                "warning"
            )
            return redirect(request.url)

        if not allowed_file(file.filename):
            flash(
                "Invalid image format.",
                "danger"
            )
            return redirect(request.url)

        upload_folder = app.config["UPLOAD_FOLDER"]

        os.makedirs(
            upload_folder,
            exist_ok=True
        )

        filename = (
            f"{uuid.uuid4()}_"
            f"{secure_filename(file.filename)}"
        )

        filepath = os.path.join(
            upload_folder,
            filename
        )

        try:

            file.save(filepath)

            photo = Photo(
                company_id=id,
                image=filename,
                image_type=request.form.get(
                    "image_type"
                )
            )

            db.session.add(photo)
            db.session.commit()

            flash(
                "Photo Uploaded Successfully",
                "success"
            )

            return redirect(
                url_for(
                    "company",
                    id=id
                )
            )

        except Exception as e:

            db.session.rollback()

            flash(
                f"Upload failed: {e}",
                "danger"
            )

    return render_template(
        "upload_photo.html",
        company=company
    )


@app.route("/delete-photo/<int:id>")
def delete_photo(id):

    photo = Photo.query.get_or_404(id)

    company_id = photo.company_id

    try:

        filepath = os.path.join(
            app.config["UPLOAD_FOLDER"],
            photo.image
        )

        if os.path.exists(filepath):
            os.remove(filepath)

    except Exception:
        pass

    try:

        db.session.delete(photo)
        db.session.commit()

        flash(
            "Photo Deleted Successfully",
            "success"
        )

    except Exception as e:

        db.session.rollback()

        flash(
            f"Error: {e}",
            "danger"
        )

    return redirect(
        url_for(
            "company",
            id=company_id
        )
    )


# --------------------------------------------------
# Settings
# --------------------------------------------------

@app.route("/settings")
def settings():

    return render_template(
        "settings.html"
    )


# --------------------------------------------------
# Error Pages
# --------------------------------------------------

@app.errorhandler(404)
def page_not_found(error):

    return (
        render_template("404.html"),
        404
    )


@app.errorhandler(500)
def internal_error(error):

    db.session.rollback()

    return (
        render_template("500.html"),
        500
    )


# --------------------------------------------------
# Entry Point
# --------------------------------------------------

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )