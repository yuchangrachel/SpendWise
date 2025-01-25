# smart-tracker
Track your expenses effectively with Smart-Tracker

# Roadmap
Implement UI for Authentication and Authorization.
Develop backend APIs for the session-based authentication service.
Design and establish the database schema and connections.
Implement basic & JWT-cookie authentication and authorization accessing to customer's dashboard
Fix JWT token is shared if loginout and login with another users shortly
Implement Cache, pagination technique to reduce conjestion and optimize data retrieval from the database.
Build Expense Record Form to record expenses in the past(max: today, location is West US).
Build the Paginated Expense Record Table(create, view) with sorting function(with Boostrap).
Integrate with Plotly Dash and optimize asynchronous Chart Loading

Implement RabbitMQ to publish and consume messages, including email notifications to users.
Provide microservices for:
Authentication Service
Expense Service
Notification Service
Report Service
Allow users upload bunch of expense record
Insights Service (AI-powered)


# Challenge 
1. Missing Authorization in header 


# TODO feature 
1. User edit / delete existing expense record
2. Customize category (add / edit / delete user's categories)
3. Add filter functionality: current month, previous month, all as default
4. Add third-party authentication via using oAuth2
5. Enhance JWT implementation(Revoke multiple tokens for same users/limit concurrent logins)

# Backend Setup
## Run the Application
To start the Flask application, use the following command:
```
flask run
```

## Update Database in development stage
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
