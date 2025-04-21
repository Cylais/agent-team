-- Create testdb and validate_quorum function for Windsurf tests
-- Run as a superuser (e.g., postgres)

-- Create the test database if it doesn't exist
CREATE DATABASE testdb;

\c testdb

-- Create the validate_quorum function if it doesn't exist
CREATE OR REPLACE FUNCTION validate_quorum(votes BOOLEAN[], threshold FLOAT)
RETURNS BOOLEAN AS $$
DECLARE
    approval_count INT := array_length(array_positions(votes, TRUE),1);
BEGIN
    RETURN (approval_count::FLOAT / array_length(votes,1)) >= threshold;
END;
$$ LANGUAGE plpgsql;
