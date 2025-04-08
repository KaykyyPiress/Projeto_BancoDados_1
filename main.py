import random
from faker import Faker

fake = Faker('pt_BR')


def gerar_semestre():
    ano = random.randint(2022, 2025)
    semestre = random.choice([1, 2])
    return f"{ano}/{semestre}"


def gerar_dml():
    dml_statements = [
        "DELETE FROM Aluno_TCC;",
        "DELETE FROM TCC;",
        "DELETE FROM Historico_Professor;",
        "DELETE FROM Historico_Aluno;",
        "DELETE FROM Disciplina;",
        "DELETE FROM Aluno;",
        "DELETE FROM Curso;",
        "DELETE FROM Professor;",
        "DELETE FROM Departamento;"
    ]

    departamentos = []
    cursos = []
    professores = []
    alunos = []

    # Inserindo Departamentos
    nomes_departamentos = ["Engenharia", "Tecnologia da Informacao", "Matematica", "Fisica", "Quimica"]
    for i, nome in enumerate(nomes_departamentos, start=1):
        departamentos.append({"id": i, "nome": nome})
        dml_statements.append(f"INSERT INTO Departamento (id_departamento, nome) VALUES ({i}, '{nome}');")

    # Inserindo Professores
    for i in range(1, 21):
        nome = fake.name()
        cpf = fake.cpf()
        id_departamento = random.choice(departamentos)['id']
        professores.append({"id": i, "id_departamento": id_departamento})
        dml_statements.append(
            f"INSERT INTO Professor (id_professor, nome, cpf, email, id_departamento) VALUES ({i}, '{nome}', '{cpf}', '{(nome.split(' ')[0]).lower()}@profFEI.com.br', {id_departamento});"
        )

    # Definindo chefes de departamento (1 por departamento)
    for dept in departamentos:
        chefe = next(p for p in professores if p['id_departamento'] == dept['id'])
        dml_statements.append(
            f"UPDATE Departamento SET id_chefe_departamento = {chefe['id']} WHERE id_departamento = {dept['id']};")

    # Inserindo Cursos
    nomes_cursos = ["Engenharia Civil", "Ciencia da Computacao", "Estatistica", "Fisica Computacional", "Quimica Aplicada"]
    for i, nome in enumerate(nomes_cursos, start=1):
        id_departamento = departamentos[i - 1]['id']
        profs_do_departamento = [p['id'] for p in professores if p['id_departamento'] == id_departamento]
        id_coordenador = random.choice(profs_do_departamento)
        cursos.append({"id": i, "id_departamento": id_departamento})
        dml_statements.append(
            f"INSERT INTO Curso (id_curso, nome, id_departamento, id_coordenador) VALUES ({i}, '{nome}', {id_departamento}, {id_coordenador});")

    # Inserindo Alunos
    for i in range(1, 101):
        nome = fake.name()
        cpf = fake.cpf()
        matricula = f"MAT{i:05}"
        id_curso = random.choice(cursos)['id']
        alunos.append(i)
        dml_statements.append(f"INSERT INTO Aluno (id_aluno, nome, cpf, email, matricula, id_curso) VALUES ({i}, '{nome}', '{cpf}', '{(nome.split(' ')[0]).lower()}@alunoFEI.com.br', '{matricula}', {id_curso});")

    # Inserindo Disciplinas
    disciplinas = []
    for i in range(1, 31):
        nome = f"Disciplina de {fake.word().capitalize()}"
        codigo = f"D{i:03}"
        id_departamento = random.choice(departamentos)['id']
        disciplinas.append({"id": i, "id_departamento": id_departamento})
        dml_statements.append(f"INSERT INTO Disciplina (id_disciplina, nome, codigo, id_departamento) VALUES ({i}, '{nome}', '{codigo}', {id_departamento});")

    # Inserindo Histórico de Professores
    for professor in professores:
        for _ in range(random.randint(1, 4)):
            disciplina = random.choice(disciplinas)
            semestre = gerar_semestre()
            dml_statements.append(f"INSERT INTO Historico_Professor (id_professor, id_disciplina, semestre) VALUES ({professor['id']}, {disciplina['id']}, '{semestre}');")

    # Inserindo Histórico de Alunos
    for aluno_id in alunos:
        historico = {}
        for _ in range(random.randint(2, 4)):
            semestre = gerar_semestre()
            disciplinas_no_semestre = set()
            while len(disciplinas_no_semestre) < random.randint(4, 6):
                disciplina = random.choice(disciplinas)
                disciplina_id = disciplina['id']
                if disciplina_id in historico and historico[disciplina_id] == 'aprovado':
                    continue
                if (semestre, disciplina_id) in disciplinas_no_semestre:
                    continue
                nota = round(random.uniform(0, 10), 2)
                situacao = 'aprovado' if nota >= 5 else 'reprovado'
                professor_id = random.choice(professores)['id']
                dml_statements.append(
                    f"INSERT INTO Historico_Aluno (id_aluno, id_disciplina, semestre, nota, situacao, id_professor) VALUES ({aluno_id}, {disciplina_id}, '{semestre}', {nota}, '{situacao}', {professor_id});")
                if situacao == 'aprovado':
                    historico[disciplina_id] = 'aprovado'
                disciplinas_no_semestre.add((semestre, disciplina_id))

    # Inserindo TCCs
    for tcc_id in range(1, 21):
        titulo = fake.sentence(nb_words=6).replace("'", "")
        orientador_id = random.choice(professores)['id']
        dml_statements.append(f"INSERT INTO TCC (id_tcc, titulo, id_orientador) VALUES ({tcc_id}, '{titulo}', {orientador_id});")

    # Inserindo alunos em TCCs (máximo 5 por TCC)
    alunos_disponiveis = alunos.copy()
    random.shuffle(alunos_disponiveis)
    for tcc_id in range(1, 21):
        num_alunos = min(5, len(alunos_disponiveis))
        alunos_tcc = [alunos_disponiveis.pop() for _ in range(num_alunos)]
        for aluno_id in alunos_tcc:
            dml_statements.append(f"INSERT INTO Aluno_TCC (id_tcc, id_aluno) VALUES ({tcc_id}, {aluno_id});")

    return "\n".join(dml_statements)

     


# Gerando o arquivo DML
with open("sql/dml_script.sql", "w", encoding='utf-8') as file:
    file.write(gerar_dml())

print("Script DML gerado com sucesso!")

