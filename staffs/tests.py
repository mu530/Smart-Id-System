from django.test import TestCase
from django.contrib.auth import get_user_model

Staff = get_user_model()


class StaffTest(TestCase):
    def test_create_staff(self):
        staff = Staff.objects.create_user(
            username="will", email="will@email.com", password="testpass123"
        )
        self.assertEqual(staff.username, "will")
        self.assertEqual(staff.email, "will@email.com")
        self.assertTrue(staff.is_active)
        self.assertFalse(staff.is_staff)
        self.assertFalse(staff.is_superuser)

    def test_create_superuser(self):
        superuser = Staff.objects.create_superuser(
            username="superadmin", email="superadmin@email.com", password="testpass123"
        )
        self.assertEqual(superuser.username, "superadmin")
        self.assertEqual(superuser.email, "superadmin@email.com")
        self.assertTrue(superuser.is_active)
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
