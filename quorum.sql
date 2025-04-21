-- Quorum validation function for Windsurf
CREATE OR REPLACE FUNCTION validate_quorum(votes BOOLEAN[], threshold FLOAT)
RETURNS BOOLEAN AS $$
DECLARE
    approval_count INT := array_length(array_positions(votes, TRUE),1);
BEGIN
    RETURN (approval_count::FLOAT / array_length(votes,1)) >= threshold;
END;
$$ LANGUAGE plpgsql;
