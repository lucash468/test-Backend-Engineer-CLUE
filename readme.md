# Subscription Management API

This is a simple Flask-based API for user registration, authentication, and subscription management.

## Features
- User Registration (`/register`)
- User Login (`/login`)
- Fetch Available Subscription Plans (`/plans`)
- Subscribe to a Plan (`/subscribe`)
- JWT-based authentication

## Technologies Used
- Flask
- Flask SQLAlchemy
- Flask JWT Extended
- SQLite (for database)
- Unittest (for testing)

## Installation

1. **Clone the Repository**
   ```sh
   git clone https://github.com/lucash468/test-Backend-Engineer-CLUE.git
   cd test-Backend-Engineer-CLUE
   ```

2. **Create a Virtual Environment**
   ```sh
   python -m venv venv
   source venv/bin/activate   # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**
   ```sh
   pip install -r requirements.txt
   ```

4. **Run the Application**
   ```sh
   python app.py
   ```

## API Endpoints

### 1. Register User
- **Endpoint:** `/register`
- **Method:** `POST`
- **Request Body:**
  ```json
  {
    "username": "test_user",
    "password": "password123"
  }
  ```
- **Response:**
  ```json
  {
    "msg": "User registered successfully"
  }
  ```

### 2. Login User
- **Endpoint:** `/login`
- **Method:** `POST`
- **Request Body:**
  ```json
  {
    "username": "test_user",
    "password": "password123"
  }
  ```
- **Response:**
  ```json
  {
    "access_token": "<JWT_TOKEN>"
  }
  ```

### 3. Get Subscription Plans
- **Endpoint:** `/plans`
- **Method:** `GET`
- **Response:**
  ```json
  [
    {
      "id": 1,
      "name": "plan1",
      "price": 0
    },
    {
      "id": 2,
      "name": "Plan2",
      "price": 10
    }
  ]
  ```

### 4. Subscribe to a Plan
- **Endpoint:** `/subscribe`
- **Method:** `POST`
- **Headers:**
  ```
  Authorization: Bearer <JWT_TOKEN>
  ```
- **Request Body:**
  ```json
  {
    "plan_id": 1
  }
  ```
- **Response:**
  ```json
  {
    "msg": "Subscription created successfully"
  }
  ```

## Optimizing Database Queries
To enhance database performance, consider the following optimizations:

1. **Use Indexing:**
   - Ensure frequently queried columns have indexes, such as `user_id` and `plan_id` in `UserSubscription`.
   ```python
   user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"), nullable=False, index=True)
   ```

2. **Avoid Unnecessary Queries:**
   - Use `exists()` instead of fetching full objects when checking for existence.
   ```python
   from sqlalchemy.sql import exists
   user_exists = db.session.query(exists().where(User.username == username)).scalar()
   ```

3. **Batch Inserts:**
   - Instead of inserting records one by one, batch inserts improve performance.
   ```python
   db.session.bulk_save_objects([SubscriptionPlan(name='Basic', price=5), SubscriptionPlan(name='Premium', price=15)])
   db.session.commit()
   ```

4. **Optimize Queries with `selectinload` or `joinedload`:**
   - When loading relationships, use eager loading to reduce queries.
   ```python
   from sqlalchemy.orm import joinedload
   user = User.query.options(joinedload(User.subscriptions)).filter_by(id=user_id).first()
   ```

5. **Use Connection Pooling:**
   - Configure SQLAlchemy to maintain persistent connections.
   ```python
   app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_size': 10, 'max_overflow': 20}
   ```

## Running Tests
To run the test suite:
```sh
python -m unittest test_app.py
```

## Notes
- Ensure the database file (`subscriptions.db`) is created automatically on first run.
- Change `JWT_SECRET_KEY` in `app.py` before deploying to production.

---

### License
This project is open-source. Feel free to modify and use as needed.

