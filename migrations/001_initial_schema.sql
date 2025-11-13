-- Migration: 001_initial_schema
-- Description: Create initial database schema for Admin Portal
-- Date: 2025-01-13

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    INDEX idx_email (email),
    INDEX idx_is_active (is_active),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Create schema_migrations table to track applied migrations
CREATE TABLE IF NOT EXISTS schema_migrations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    migration_file VARCHAR(255) UNIQUE NOT NULL,
    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Insert test data for development (optional - remove in production)
INSERT INTO users (name, email, password, is_active) VALUES
('John Doe', 'john@example.com', NULL, TRUE),
('Jane Smith', 'jane@example.com', NULL, TRUE),
('Admin User', 'admin@example.com', NULL, TRUE);

-- Record this migration
INSERT INTO schema_migrations (migration_file) VALUES ('001_initial_schema.sql')
ON DUPLICATE KEY UPDATE migration_file = migration_file;
