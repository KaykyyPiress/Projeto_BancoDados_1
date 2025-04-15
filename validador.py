class FakeCursor:
    def execute(self, query):
        print("Executando query:")
        print(query)
        # Para fins de teste, nenhum registro de inconsistência será retornado.
        self._result = []
    
    def fetchall(self):
        return self._result
    
    def close(self):
        print("FakeCursor encerrado.\n")


class FakeConnection:
    def cursor(self):
        return FakeCursor()
    
    def close(self):
        print("FakeConnection encerrada.")


def check_consistency(conn):
    cur = conn.cursor()

    # --- Validação 1: Histórico de Professores ---
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

    # --- Validação 2: Histórico de Alunos ---
    # A query assume que o campo 'semestre' está no formato "YYYY/S" e converte para um número: ano * 10 + semestre.
    query_aluno = """
    WITH semestre_numerico AS (
      SELECT
         id_aluno,
         id_disciplina,
         situacao,
         semestre,
         CAST(split_part(semestre, '/', 1) AS int) * 10 +
         CAST(split_part(semestre, '/', 2) AS int) AS sem_num
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
    # Para teste, usamos a FakeConnection no lugar de uma conexão real com o Supabase.
    conn = FakeConnection()
    print("Simulação de validação de consistência dos dados:")
    check_consistency(conn)
    conn.close()
