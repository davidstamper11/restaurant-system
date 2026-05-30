# scripts/fix_null_password.py
from passlib.context import CryptContext
from app.services.db_service import get_db
from app.models.authorized_reviewer import AuthorizedReviewer

# Use the same hashing scheme as the rest of the app
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

def fix_null_password():
    db = next(get_db())

    # Find reviewers (including non‑admins) whose password is NULL
    reviewers = (
        db.query(AuthorizedReviewer)
        .filter(AuthorizedReviewer.password.is_(None))
        .all()
    )

    if not reviewers:
        print("No reviewers with NULL password found.")
        return

    for reviewer in reviewers:
        # Assign a temporary password – you can change it later via the UI
        temp_password = "!Foobar11"
        reviewer.password = pwd_context.hash(temp_password)