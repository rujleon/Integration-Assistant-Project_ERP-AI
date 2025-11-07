from sqlalchemy import create_engine, text

def get_engine():
    host = "localhost"
    port = 3307
    user = "root"
    password = ""
    database = "gl_comptable"

    engine = create_engine(f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}")
    return engine


def execute_sql(query):
    """Exécute une requête SQL et retourne le résultat sous forme de liste de dictionnaires"""
    engine = get_engine()
    with engine.connect() as connection:
        result = connection.execute(text(query))
        # Si c’est une requête SELECT, on renvoie les lignes
        if result.returns_rows:
            data = [dict(row._mapping) for row in result]
            return data
        else:
            # Pour les INSERT/UPDATE/DELETE
            connection.commit()
            return {"message": "Requête exécutée avec succès"}


