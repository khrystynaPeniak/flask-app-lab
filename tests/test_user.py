import unittest
from app import create_app, db
from app.users.models import User

class TestAuth(unittest.TestCase):
    def setUp(self):
        """Налаштування тестового середовища."""
        self.app = create_app(config_name="config.TestConfig")
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        """Очищення після тестів."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_registration_page_loads(self):
        """Тест завантаження сторінки реєстрації."""
        response = self.client.get('/user/register')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Register', response.data)

    def test_login_page_loads(self):
        """Тест завантаження сторінки входу."""
        response = self.client.get('/user/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)

    def test_user_registration(self):
        """Тест процесу реєстрації користувача."""
        response = self.client.post('/user/register', data={
            'username': 'someUser',
            'email': 'user@testing.com',
            'password': 'userpass',
            'confirm_password': 'userpass'
        }, follow_redirects=True)
        
        self.assertIn(b'Account for someUser was created!', response.data)
        
        user = User.query.filter_by(username='someUser').first()
        self.assertIsNotNone(user)
        self.assertEqual(user.email, 'user@testing.com')

    def test_user_login_logout(self):
        """Тест входу та виходу користувача."""
        password = 'userpass'
        hashed_password = User.hash_password(password)
        user = User(
            username='someUser',
            email='user@testing.com',
            password=hashed_password
        )
        db.session.add(user)
        db.session.commit()

        response = self.client.post('/user/login', data={
            'username': 'someUser',
            'password': 'userpass',
            'remember': False
        }, follow_redirects=True)
        self.assertIn(b'You logged in successfully!', response.data)

        response = self.client.get('/user/account')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/user/logout', follow_redirects=True)
        self.assertIn(b'You have successfully logged out.', response.data)

        response = self.client.get('/account')
        self.assertNotEqual(response.status_code, 200)

    def test_invalid_login(self):
        """Тест входу з неправильними даними."""
        response = self.client.post('/user/login', data={
            'username': 'wronguser',
            'password': 'wrongpass',
            'remember': False
        }, follow_redirects=True)
        self.assertIn(b'Invalid username or password', response.data)

if __name__ == '__main__':
    unittest.main()
