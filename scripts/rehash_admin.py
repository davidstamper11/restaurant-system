from passlib.context import CryptContext
from app.services.db_service import get_db
from app.models.authorized_reviewer import AuthorizedReviewer

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

def rehash_admin():
    db = next(get_db())
    admin = db.query(AuthorizedReviewer).filter(AuthorizedReviewer.is_admin_yn == True).first()
    if admin and admin.password:
        # If password is already a hash, skip
        if admin.password.startswith("$pbkdf2-sha256$"):
            print("Admin password already hashed.")
        else:
            admin.password = pwd_context.hash(admin.password)
            db.commit()
            print("Admin password re‑hashed.")
    else:
        print("No admin with a password found.")

if __name__ == "__main__":
    rehash_admin()

