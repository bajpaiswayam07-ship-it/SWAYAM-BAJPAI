import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "python_ui"))
from auth_manager import AuthManager, UserAccount

class TestAuthManager(unittest.TestCase):
    def setUp(self):
        self.auth = AuthManager()

    def test_admin_account_exists(self):
        admin_users = [u for u in self.auth.get_all_users() if u.is_admin()]
        self.assertTrue(len(admin_users) > 0, "At least one admin account must exist")
        admin = admin_users[0]
        self.assertTrue(admin.is_admin())
        self.assertTrue(len(admin.email) > 0, "Admin must have an email")

    def test_email_login_for_admin(self):
        # Test login via Email for admin
        res = self.auth.login("adminswayam@gmail.com", "admin@123")
        self.assertIsNotNone(res)
        self.assertTrue(self.auth.is_current_admin())
        self.assertEqual(res.username, "adminswayam")

    def test_username_login_for_admin(self):
        # Test login via Username for admin
        res = self.auth.login("adminswayam", "admin@123")
        self.assertIsNotNone(res)
        self.assertTrue(self.auth.is_current_admin())

    def test_email_login_case_insensitivity(self):
        # Test case-insensitivity of email lookup
        res = self.auth.login("ADMINSWAYAM@GMAIL.COM", "admin@123")
        self.assertIsNotNone(res)
        self.assertTrue(self.auth.is_current_admin())

    def test_user_email_login(self):
        # Test login via Email for standard listener
        res = self.auth.login("swayam@gmail.com", "user123")
        self.assertIsNotNone(res)
        self.assertFalse(self.auth.is_current_admin())

        # Test login via Username for standard listener
        res2 = self.auth.login("user", "user123")
        self.assertIsNotNone(res2)
        self.assertFalse(self.auth.is_current_admin())

    def test_failed_logins(self):
        # Wrong password
        self.assertIsNone(self.auth.login("adminswayam@gmail.com", "wrongpass"))
        # Non-existent email
        self.assertIsNone(self.auth.login("unknown@spotify.com", "admin@123"))

    def test_register_duplicate_prevention(self):
        # Attempting duplicate email should fail
        success = self.auth.add_user("testuser_dup", "adminswayam@gmail.com", "pass123")
        self.assertFalse(success)

    def test_user_self_registration(self):
        uname = "swayam_listener"
        email = "swayam_fan@spotify.com"
        # Cleanup if exists
        self.auth.remove_user(uname)
        success = self.auth.add_user(uname, email, "listener123", role="user", display_name="Swayam Listener")
        self.assertTrue(success)

        # Verify login via email
        user = self.auth.login(email, "listener123")
        self.assertIsNotNone(user)
        self.assertEqual(user.role, "user")
        self.assertFalse(user.is_admin())
        self.assertEqual(user.display_name, "Swayam Listener")

        # Cleanup
        self.auth.remove_user(uname)

if __name__ == "__main__":
    unittest.main()
