-- Updated validate_quorum function to return FALSE when input array is empty
CREATE OR REPLACE FUNCTION validate_quorum(votes BOOLEAN[], threshold FLOAT)
RETURNS BOOLEAN AS $$
BEGIN
    IF array_length(votes, 1) = 0 THEN
        RETURN FALSE;
    END IF;
    RETURN (array_length(array_positions(votes, TRUE),1)::FLOAT / array_length(votes,1)) >= threshold;
END;
$$ LANGUAGE plpgsql;
