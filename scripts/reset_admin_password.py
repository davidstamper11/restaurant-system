from passlib.context import CryptContext
from app.services.db_service import get_db
from app.models.authorized_reviewer import AuthorizedReviewer

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
NEW_PASSWORD = "TempPass123"


def reset_admin_password():
    db = next(get_db())
    admin = db.query(AuthorizedReviewer).filter(AuthorizedReviewer.is_admin_yn == True).first()
    if not admin:
        print("Admin user not found.")
        return
    admin.password = pwd_context.hash(NEW_PASSWORD)
    db.commit()
    print(f"Admin password reset to '{NEW_PASSWORD}' (hashed).")


if __name__ == "__main__":
    reset_admin_password()
