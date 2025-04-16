import psycopg2

def get_connection():
    """
    Cria e retorna uma conexão com o banco Supabase.
    As credenciais são lidas das variáveis de ambiente.
    """
    SUPABASE_HOST = "aws-0-sa-east-1.pooler.supabase.com"
    SUPABASE_PORT = 6543
    SUPABASE_DATABASE = "postgres"
    SUPABASE_USER = "postgres.azriarqzqraykgbsqlst"
    SUPABASE_PASSWORD = "MinasGerais123"

    conn = psycopg2.connect(
        host=SUPABASE_HOST,
        port=SUPABASE_PORT,
        dbname=SUPABASE_DATABASE,
        user=SUPABASE_USER,
        password=SUPABASE_PASSWORD
    )
    
    return conn
