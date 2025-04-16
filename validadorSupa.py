from db_connection import get_connection

def check_consistency(conn):
    cur = conn.cursor()

    # Verificação 1: Histórico de Professores
    # Valida se cada registro do histórico possui uma disciplina cujo departamento
    # seja o mesmo do professor.
    query_prof = """
    SELECT hp.id_professor, hp.id_disciplina, p.id_departamento AS prof_depto, d.id_departamento AS disc_depto
    FROM Historico_Professor hp
    JOIN Professor p ON p.id_professor = hp.id_professor
    JOIN Disciplina d ON d.id_disciplina = hp.id_disciplina
    WHERE p.id_departamento <> d.id_departamento;
    """
    cur.execute(query_prof)
    inconsistencias_prof = cur.fetchall()
    if inconsistencias_prof:
        print("Inconsistências encontradas no Histórico de Professores:")
        for row in inconsistencias_prof:
            print(f"Professor ID: {row[0]} | Disciplina ID: {row[1]} | Dept. Professor: {row[2]} | Dept. Disciplina: {row[3]}")
    else:
        print("Histórico de Professores: Todos os dados estão consistentes.")

    # Verificação 2: Histórico de Alunos
    # Aqui, como exemplo, vamos buscar pares (aluno, disciplina) em que exista
    # uma data de aprovação (primeira tentativa aprovada) anterior a uma reprovação (última reprovação).
    # Isso indicaria que após a aprovação, houve um registro posterior de reprovação.
    #
    # Para comparar os semestres (no formato "YYYY/S"), usaremos funções SQL para converter em números,
    # fazendo: número = ano * 10 + semestre.
    query_aluno = """
    WITH semestre_numerico AS (
      SELECT
         id_aluno,
         id_disciplina,
         situacao,
         semestre,
         CAST(split_part(semestre, '/', 1) AS int) * 10 + CAST(split_part(semestre, '/', 2) AS int) AS sem_num
      FROM Historico_Aluno
    ),
    resumo AS (
      SELECT 
         id_aluno,
         id_disciplina,
         MIN(sem_num) FILTER (WHERE situacao = 'aprovado') AS primeiro_aprovado,
         MAX(sem_num) FILTER (WHERE situacao = 'reprovado') AS ultima_reprovado
      FROM semestre_numerico
      GROUP BY id_aluno, id_disciplina
      HAVING MIN(sem_num) FILTER (WHERE situacao = 'aprovado') IS NOT NULL 
         AND MAX(sem_num) FILTER (WHERE situacao = 'reprovado') IS NOT NULL
    )
    SELECT id_aluno, id_disciplina, primeiro_aprovado, ultima_reprovado
    FROM resumo
    WHERE primeiro_aprovado < ultima_reprovado;
    """
    cur.execute(query_aluno)
    inconsistencias_aluno = cur.fetchall()
    if inconsistencias_aluno:
        print("\nInconsistências encontradas no Histórico de Alunos:")
        print("Alunos que possuem aprovação ocorrendo antes de uma reprovação posterior:")
        for row in inconsistencias_aluno:
            print(f"Aluno ID: {row[0]} | Disciplina ID: {row[1]} | Primeiro Aprovado: {row[2]} | Última Reprovado: {row[3]}")
    else:
        print("\nHistórico de Alunos: Todos os dados estão consistentes.")

    cur.close()


if __name__ == "__main__":
    try:
        conn = get_connection()
        print("Conectado ao Supabase com sucesso!")
        check_consistency(conn)
        conn.close()
    except Exception as e:
        print(f"Erro ao conectar ou validar dados: {e}")
