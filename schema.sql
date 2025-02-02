CREATE TABLE users (
    user_id PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
);

CREATE TABLE session (
    session_id PRIMARY KEY,
    user_id INT REFERENCES users(user_id),
    start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    end_time TIMESTAMP,
    status VARCHAR(50) DEFAULT 'active',
    context JSONB DEFAULT '{}'
);

-- Messages Table
CREATE TABLE chats (
    chats_id PRIMARY KEY,
    session_id INT REFERENCES sessions(session_id),
    sender VARCHAR(50) NOT NULL,  
    message TEXT NOT NULL,
    chat_type VARCHAR(50) DEFAULT 'text',
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    chat_data DEFAULT '{}'
);
