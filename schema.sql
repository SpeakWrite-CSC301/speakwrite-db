CREATE TABLE IF NOT EXISTS users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
);

CREATE TABLE IF NOT EXISTS sessions (
    session_id SERIAL PRIMARY KEY,
    session_name VARCHAR(50) NOT NULL,
    user_id INT REFERENCES users(user_id) ON DELETE CASCADE,
    start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    end_time TIMESTAMP,
    status VARCHAR(50) DEFAULT 'active',
    context JSONB DEFAULT '{}'
);

-- Messages Table
CREATE TABLE IF NOT EXISTS chats (
    chats_id SERIAL PRIMARY KEY,
    session_id INT REFERENCES sessions(session_id) ON DELETE CASCADE,
    sender VARCHAR(50) NOT NULL,  
    message TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
