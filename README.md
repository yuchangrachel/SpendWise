# smart-tracker
Track your expenses effectively with Smart-Tracker

# Roadmap
Implement UI for Authentication and Authorization.
Develop backend APIs for the authentication service.
Design and establish the database schema and connections.
Build the Expense Form feature in the UI.
Build the Expense List feature in the UI.
Set up backend APIs for core functionality.
Implement RabbitMQ to publish and consume messages, including email notifications to users.
Provide microservices for:
Authentication Service
Expense Service
Notification Service
Report Service
Insights Service (AI-powered)


# Backend Setup
## Run the Application
To start the Flask application, use the following command:
```
flask run
```

## Database migration
#### To upgrade the existing database 
(e.g., adding a new column to a table without losing existing data), follow these steps:
```
flask db init         # Initializes the migrations folder (if not already done)
flask db migrate -m "Initial migration"  # Creates a new migration script, check migrations/
flask db upgrade      # Applies the migration to the database
```

#### Change `id` type in `users`table
To change the ID type in the users table (from a truncated UUID string to an auto-increment integer), use the following steps:
1. Ensure PostgreSQL is installed on your system. in macos `brew install psql`.
2. Navigate to the backend/db_script directory.
3. Run the SQL script as follows:
```
psql -h <host: localhost> -U <username:postgres> -d <database:auth> -f update_users_table_id.sql
```
