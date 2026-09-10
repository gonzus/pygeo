from typing import List
from core.database import db_session
from users.models import UserModel

class UserDomainService:
    @staticmethod
    def get_user_by_id(user_id: int) -> UserModel | None:
        """
        Retrieves a single user from the database by their unique ID.
        Returns None if no matching user is found.
        """
        return db_session.query(UserModel).filter_by(id=user_id).first()


    @staticmethod
    def create_user(email: str, name: str) -> UserModel:
        """
        Orchestrates user creation business logic and data persistence.
        """
        # 1. Clean data inputs (strip down spaces, uniform casing)
        clean_email = email.strip().lower()
        clean_name = name.strip()

        if not clean_email or "@" not in clean_email:
            raise ValueError("A valid email address is required.")

        if not clean_name:
            raise ValueError("User name cannot be empty.")

        # 2. Enforce global business domain uniqueness rules
        existing_user = db_session.query(UserModel).filter_by(email=clean_email).first()
        if existing_user:
            raise ValueError(f"User with email '{clean_email}' already exists.")

        # 3. Instantiate and persist the infrastructure model
        new_user = UserModel(
            email=clean_email,
            name=clean_name,
            is_active=True  # Default state set explicitly at the business layer
        )

        db_session.add(new_user)
        db_session.commit()
        db_session.refresh(new_user)

        # 4. Handle cross-domain triggers or side effects safely here
        # (e.g., dispatching user-created message events)

        return new_user


    @staticmethod
    def delete_user_by_id(user_id: int) -> str:
        """
        Executes a real SQL DELETE statement on the users table.

        Returns:
            "deleted" if the row was removed successfully.
            "not_found" if the user ID does not exist.
            "has_dependent_orders" if foreign key constraints block the delete.
        """
        user = db_session.query(UserModel).filter_by(id=user_id).first()

        if not user:
            return "not_found"

        try:
            # Tell SQLAlchemy to issue a real SQL DELETE command
            db_session.delete(user)
            db_session.commit()
            return "deleted"

        except IntegrityError:
            # Roll back the active transaction session so the connection remains stable
            db_session.rollback()
            return "has_dependent_orders"


    @staticmethod
    def get_all_users() -> List[UserModel]:
        """
        Retrieves all active users from the database.
        """
        return db_session.query(UserModel).filter_by(is_active=True).all()


    @staticmethod
    def search_users_by_name(search_term: str) -> List[UserModel]:
        """
        Searches for active users whose names contain the search term (case-insensitive).
        """
        clean_term = search_term.strip()

        # If the search query is empty, return an empty list immediately without hitting the DB
        if not clean_term:
            return []

        # Build a SQL wild-card pattern (e.g., '%alan%')
        like_pattern = f"%{clean_term}%"

        return (
            db_session.query(UserModel)
            .filter(UserModel.name.ilike(like_pattern))
            .filter(UserModel.is_active == True)
            .all()
        )
