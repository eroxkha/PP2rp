CREATE OR REPLACE FUNCTION search_contacts(p TEXT)
RETURNS TABLE(name VARCHAR, phone VARCHAR)
AS $$
BEGIN
    RETURN QUERY
    SELECT name, phone
    FROM contacts
    WHERE name ILIKE '%' || p || '%'
       OR phone ILIKE '%' || p || '%';
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION get_contacts_paginated(lim INT, off INT)
RETURNS TABLE(name VARCHAR, phone VARCHAR)
AS $$
BEGIN
    RETURN QUERY
    SELECT name, phone
    FROM contacts
    LIMIT lim OFFSET off;
END;
$$ LANGUAGE plpgsql;