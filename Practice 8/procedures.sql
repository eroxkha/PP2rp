CREATE OR REPLACE PROCEDURE upsert_contact(p_name VARCHAR, p_phone VARCHAR)
LANGUAGE plpgsql
AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM contacts WHERE name = p_name) THEN
        UPDATE contacts SET phone = p_phone WHERE name = p_name;
    ELSE
        INSERT INTO contacts(name, phone) VALUES(p_name, p_phone);
    END IF;
END;
$$;

CREATE OR REPLACE PROCEDURE delete_contact(p TEXT)
LANGUAGE plpgsql
AS $$
BEGIN
    DELETE FROM contacts
    WHERE name = p OR phone = p;
END;
$$;


CREATE OR REPLACE PROCEDURE bulk_insert(data TEXT[][])
LANGUAGE plpgsql
AS $$
DECLARE i INT;
BEGIN
    FOR i IN 1..array_length(data,1) LOOP
        IF data[i][2] ~ '^[0-9+]+$' THEN
            CALL upsert_contact(data[i][1], data[i][2]);
        END IF;
    END LOOP;
END;
$$;