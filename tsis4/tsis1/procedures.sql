-- добавление телефона
CREATE OR REPLACE PROCEDURE add_phone(p_contact_name VARCHAR, p_phone VARCHAR, p_type VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    INSERT INTO phones (contact_id, phone, type)
    SELECT id, p_phone, p_type FROM contacts WHERE name = p_contact_name;
END;
$$;

-- перемещение в группу с созданием группы если её нет
CREATE OR REPLACE PROCEDURE move_to_group(p_contact_name VARCHAR, p_group_name VARCHAR)
LANGUAGE plpgsql AS $$
DECLARE
    v_group_id INTEGER;
BEGIN
    INSERT INTO groups (name) VALUES (p_group_name) ON CONFLICT (name) DO NOTHING;
    SELECT id INTO v_group_id FROM groups WHERE name = p_group_name;
    
    UPDATE contacts SET group_id = v_group_id WHERE name = p_contact_name;
END;
$$;

-- расширенный поиск
CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE(id INTEGER, name VARCHAR, email VARCHAR, birthday DATE, group_name VARCHAR, all_phones TEXT) 
LANGUAGE plpgsql AS $$
BEGIN
    RETURN QUERY
    SELECT c.id, c.name, c.email, c.birthday, g.name, string_agg(p.phone, ', ')
    FROM contacts c
    LEFT JOIN groups g ON c.group_id = g.id
    LEFT JOIN phones p ON c.id = p.contact_id
    WHERE c.name ILIKE '%' || p_query || '%'
       OR c.email ILIKE '%' || p_query || '%'
       OR p.phone ILIKE '%' || p_query || '%'
    GROUP BY c.id, g.name;
END;
$$;