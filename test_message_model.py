"""Messages model tests."""

from app import app
import os
from unittest import TestCase


from models import db, User, Message, Follows


os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


db.create_all()


class MessageModelTestCase(TestCase):
    """Tests for Message model"""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        self.client = app.test_client()

    def test_repr_display(self):
        """Does the repr method work as expected?"""
        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )
        db.session.add(u)
        db.session.commit()

        msg = Message(
            text="Test Text",
            user_id=u.id
        )
        db.session.add(msg)
        db.session.commit()

        self.assertIn(str(msg.id), msg.__repr__())
        self.assertIn(str(u.id), msg.__repr__())

    def test_message_connected_to_user(self):
        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )
        db.session.add(u)
        db.session.commit()

        msg = Message(
            text="Test Text",
            user_id=u.id
        )
        db.session.add(msg)
        db.session.commit()

        self.assertEqual(msg.user_id, u.id)
