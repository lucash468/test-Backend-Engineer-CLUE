import unittest
from app import app, db, User, SubscriptionPlan, create_access_token
from flask_jwt_extended import get_jwt_identity
from datetime import date

class SubscriptionTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        
        with app.app_context():
            db.create_all()

            plan1 = SubscriptionPlan(name='plan1', price=0)
            plan2 = SubscriptionPlan(name='Plan2', price=10)
            db.session.add(plan1)
            db.session.add(plan2)
            db.session.commit()

    def tearDown(self):

        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_register_user(self):
        response = self.app.post('/register', json={
            "username": "test_user",
            "password": "password123"
        })
        self.assertEqual(response.status_code, 201)

    def test_login_user(self):
        self.app.post('/register', json={
            "username": "test_user",
            "password": "password123"
        })

        response = self.app.post('/login', json={
            "username": "test_user",
            "password": "password123"
        })
        self.assertEqual(response.status_code, 200)

    def test_get_plans(self):
        response = self.app.get('/plans')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.json) > 0)

    def test_subscribe(self):
        with app.app_context():

            test_user = User(username="test_user", password="hashedpassword")
            db.session.add(test_user)
            db.session.commit()

            access_token = create_access_token(identity=str(test_user.id))

            plan = SubscriptionPlan.query.first()
            if not plan:
                self.fail("No subscription plans found.")

        response = self.app.post('/subscribe', json={"plan_id": plan.id}, headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        })

        self.assertEqual(response.status_code, 201)
        self.assertIn("Subscription created successfully", response.json["msg"])

if __name__ == '__main__':
    unittest.main()
