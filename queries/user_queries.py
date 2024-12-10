class UserQueries:
    create_table = """
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL
        );
    """
    
    insert_user = """
        INSERT INTO users (name, email) VALUES (%s, %s);
    """
    
    get_users = """
        SELECT * FROM users ORDER BY id;
    """
    
    get_user = """
        SELECT * FROM users WHERE id = %s;
    """
    
    update_user ="""
        UPDATE users
        SET name = %s, email = %s
        WHERE id = %s;
    """
    
    del_user ="""
        DELETE FROM users WHERE id = %s;
    """
    
    
    
