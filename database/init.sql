-- Database initialization script for AI Chatbot
-- This script will be executed when the PostgreSQL container starts for the first time

-- Create the database if it doesn't exist (handled by POSTGRES_DB env var)
-- Create the user if it doesn't exist (handled by POSTGRES_USER env var)

-- Grant necessary permissions
GRANT ALL PRIVILEGES ON DATABASE chatbot_db TO chatbot_user;

-- Create extensions if needed
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- The tables will be created by SQLAlchemy when the backend starts
-- This script is mainly for any additional database setup

-- Optional: Create indexes for better performance (will be created after tables exist)
-- These will be executed by the backend application, but kept here for reference

/*
-- Future indexes for performance optimization:
-- CREATE INDEX IF NOT EXISTS idx_chat_messages_timestamp ON chat_messages(timestamp DESC);
-- CREATE INDEX IF NOT EXISTS idx_chat_messages_user_message ON chat_messages USING gin(to_tsvector('english', user_message));
*/

-- Log the initialization
SELECT 'Database initialization completed' as status;
