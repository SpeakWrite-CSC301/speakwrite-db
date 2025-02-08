import psycopg2

# Database Connection Details
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASSWORD = "lolxdlolnoice13245"
DB_HOST = "localhost"  
DB_PORT = "5432"

#Connect to PostgreSQL
conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
)
