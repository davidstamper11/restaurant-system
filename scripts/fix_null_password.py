from passlib.context import CryptContext
from app.services.db_service import get_db
from app.models.authorized_reviewer import AuthorizedReviewer

# Use the same hashing scheme as the rest of the app
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

def fix_null_password():
    db = next(get_db())
    reviewers = db.query(AuthorizedReviewer).filter(
        (AuthorizedReviewer.password.is_(None)) |
        (AuthorizedReviewer.password == "None") |
        (AuthorizedReviewer.password == "")
    ).all()
    if not reviewers:
        print("No reviewers with NULL password found.")
        return
    for reviewer in reviewers:
        temp_password = "temporary123"  # replace with desired password
        reviewer.password = pwd_context.hash(temp_password)
        print(f"Set temporary password for reviewer {reviewer.email}")
    db.commit()
    print("Done.")

if __name__ == "__main__":
    fix_null_password()
