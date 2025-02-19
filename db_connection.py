import psycopg2

# Database Connection Details
DB_NAME = "speakwrite"
DB_USER = "speakwrite_user"
DB_PASSWORD = "onhQjQKz9GY5RpNr66Fj4rGNTu54eylp"
DB_HOST = "dpg-cunn7stumphs73bomfb0-a.oregon-postgres.render.com"  
DB_PORT = "5432"

#Connect to PostgreSQL
conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        sslmode='require'
)
