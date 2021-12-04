"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


from app import app, signup
import os
from unittest import TestCase
from sqlalchemy.exc import IntegrityError


from models import db, User, Message, Follows

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app


# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserModelTestCase(TestCase):
    """Tests for User model"""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        self.client = app.test_client()

    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(len(u.messages), 0)
        self.assertEqual(len(u.followers), 0)

    def test_repr_display(self):
        """Does the repr method work as expected?"""
        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        self.assertIn('test@test.com', u.__repr__())
        self.assertIn('testuser', u.__repr__())

    def test_is_following(self):
        """Does the is_following method work porperly?"""
        u1 = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )
        u2 = User(
            email="test2@test.com",
            username="test2user",
            password="HASHED_PASSWORD2"
        )
        db.session.add_all([u1, u2])
        db.session.commit()

        # Does is_following successfully detect when user1 is following user2?
        u1.following.append(u2)
        db.session.commit()
        self.assertTrue(u1.is_following(u2))

        # Does is_following successfully detect when user1 is not following user2?
        u1.following.remove(u2)
        db.session.commit()
        self.assertFalse(u1.is_following(u2))

    def test_is_followed(self):
        """Does the is_followed method work properly?"""
        u1 = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )
        u2 = User(
            email="test2@test.com",
            username="test2user",
            password="HASHED_PASSWORD2"
        )
        db.session.add_all([u1, u2])
        db.session.commit()

        # Does is_followed_by successfully detect when user1 is followed by user2?
        u1.following.append(u2)
        db.session.commit()
        self.assertTrue(u2.is_followed_by(u1))

        # Does is_followed_by successfully detect when user1 is not followed by user2?
        u1.following.remove(u2)
        db.session.commit()
        self.assertFalse(u2.is_followed_by(u1))

    def test_user_signup(self):
        """Does the User.signup method work properly?"""

        # Does User.signup successfully create a new user given valid credentials?
        username = 'Test'
        email = 'Test@Test.com'
        password = 'TestPassword'
        image_url = '/static/images/default-pic.png'
        u = User.signup(username=username, email=email,
                        password=password, image_url=image_url)
        self.assertIsInstance(u, User)

        # Does User.signup fail to create a new user if any of the validations (e.g. uniqueness, non-nullable fields) fail?
        username2 = 'Test'
        email2 = 'Test@Test.com'
        password2 = 'TestPassword'
        image_url2 = '/static/images/default-pic.png'
        u2 = User.signup(username=username2, email=email2,
                         password=password2, image_url=image_url2)
        try:
            db.session.commit()
        except IntegrityError:
            u2 = 'Invalid credentials/username already taken'
        self.assertIn(u2, 'Invalid credentials/username already taken')

    def test_user_authenticate(self):
        """Does User.authenticate work properly?"""
        username = 'Test'
        email = 'Test@Test.com'
        password = 'TestPassword'
        image_url = '/static/images/default-pic.png'
        u = User.signup(username=username, email=email,
                        password=password, image_url=image_url)
        db.session.commit()

        # Does User.authenticate successfully return a user when given a valid username and password?
        self.assertIsInstance(User.authenticate(
            username=username, password=password), User)
        # Does User.authenticate fail to return a user when the username is invalid?
        self.assertFalse(User.authenticate(
            username='FakeUsername', password=password))
        # Does User.authenticate fail to return a user when the password is invalid?
        self.assertFalse(User.authenticate(
            username=username, password='FakePassword'))
