import json
import os
from typing import Optional, List, Dict
from dataclasses import dataclass

@dataclass
class UserAccount:
    username: str
    email: str
    password: str
    role: str       # "admin" or "user"
    display_name: str

    def is_admin(self) -> bool:
        return self.role.lower() == "admin"

class AuthManager:
    def __init__(self, filepath: Optional[str] = None):
        if filepath is None:
            base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
            filepath = os.path.join(base_dir, "data", "users.json")
        self.filepath = filepath
        self.users: Dict[str, UserAccount] = {}
        self.current_user: Optional[UserAccount] = None
        self.load()

        # Default fallback if file was empty
        if not self.users:
            self.users["adminswayam"] = UserAccount(
                username="adminswayam",
                email="adminswayam@gmail.com",
                password="admin@123",
                role="admin",
                display_name="System Admin"
            )
            self.save()

        # Start with an admin session active if available
        admin_acc = next((u for u in self.users.values() if u.is_admin()), None)
        self.current_user = admin_acc if admin_acc else (list(self.users.values())[0] if self.users else None)

    def load(self):
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for u in data.get("users", []):
                        uname = u["username"]
                        default_email = f"{uname.lower()}@spotify.com"
                        email = u.get("email", "").strip() or default_email
                        self.users[uname] = UserAccount(
                            username=uname,
                            email=email,
                            password=u["password"],
                            role=u.get("role", "user"),
                            display_name=u.get("display_name") or u.get("displayName") or uname
                        )
            except Exception as e:
                print(f"[AuthManager] Error loading users: {e}")

    def save(self) -> bool:
        try:
            os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
            data = {
                "users": [
                    {
                        "username": u.username,
                        "email": u.email,
                        "password": u.password,
                        "role": u.role,
                        "display_name": u.display_name,
                        "displayName": u.display_name
                    }
                    for u in self.users.values()
                ]
            }
            with open(self.filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            return True
        except Exception as e:
            print(f"[AuthManager] Error saving users: {e}")
            return False

    def login(self, identifier: str, password: str) -> Optional[UserAccount]:
        """
        Authenticate using either Email or Username (case-insensitive identifier match).
        """
        target = identifier.strip().lower()
        if not target or not password:
            return None

        for user in self.users.values():
            if (user.username.lower() == target or user.email.lower() == target) and user.password == password:
                self.current_user = user
                return user
        return None

    def logout(self):
        self.current_user = None

    def add_user(self, username: str, email: str, password: str, role: str = "user", display_name: str = "") -> bool:
        un = username.strip()
        em = email.strip()
        if not un or not password:
            return False

        # Validate unique username and email
        for u in self.users.values():
            if u.username.lower() == un.lower():
                return False
            if em and u.email.lower() == em.lower():
                return False

        if not em:
            em = f"{un.lower()}@spotify.com"

        d_name = display_name.strip() if display_name else un
        self.users[un] = UserAccount(
            username=un,
            email=em,
            password=password,
            role=role,
            display_name=d_name
        )
        return self.save()

    def remove_user(self, username: str) -> bool:
        if username in self.users:
            # Cannot delete the only admin
            if self.users[username].is_admin():
                admin_count = sum(1 for u in self.users.values() if u.is_admin())
                if admin_count <= 1:
                    return False
            del self.users[username]
            if self.current_user and self.current_user.username == username:
                # Switch to another admin if available
                admin_acc = next((u for u in self.users.values() if u.is_admin()), None)
                self.current_user = admin_acc if admin_acc else (list(self.users.values())[0] if self.users else None)
            return self.save()
        return False

    def get_all_users(self) -> List[UserAccount]:
        return list(self.users.values())

    def is_current_admin(self) -> bool:
        return bool(self.current_user and self.current_user.is_admin())
