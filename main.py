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
        dml_statements.append(
            f"INSERT INTO Departamento (id_departamento, nome) VALUES ({i}, '{nome}');"
        )

    # Inserindo Professores
    for i in range(1, 21):
        nome = fake.name()
        cpf = fake.cpf()
        id_departamento = random.choice(departamentos)['id']
        professores.append({"id": i, "id_departamento": id_departamento})
        dml_statements.append(
            f"INSERT INTO Professor (id_professor, nome, cpf, email, id_departamento) VALUES "
            f"({i}, '{nome}', '{cpf}', '{(nome.split(' ')[0]).lower()}@profFEI.com.br', {id_departamento});"
        )

    # Definindo chefes de departamento (1 por departamento)
    for dept in departamentos:
        chefe = next(p for p in professores if p['id_departamento'] == dept['id'])
        dml_statements.append(
            f"UPDATE Departamento SET id_chefe_departamento = {chefe['id']} WHERE id_departamento = {dept['id']};"
        )

    # Inserindo Cursos
    nomes_cursos = ["Engenharia Civil", "Ciencia da Computacao", "Estatistica", "Fisica Computacional", "Quimica Aplicada"]
    for i, nome in enumerate(nomes_cursos, start=1):
        id_departamento = departamentos[i - 1]['id']
        profs_do_departamento = [p['id'] for p in professores if p['id_departamento'] == id_departamento]
        id_coordenador = random.choice(profs_do_departamento)
        cursos.append({"id": i, "id_departamento": id_departamento})
        dml_statements.append(
            f"INSERT INTO Curso (id_curso, nome, id_departamento, id_coordenador) VALUES "
            f"({i}, '{nome}', {id_departamento}, {id_coordenador});"
        )

    # Inserindo Alunos
    for i in range(1, 101):
        nome = fake.name()
        cpf = fake.cpf()
        matricula = f"MAT{i:05}"
        id_curso = random.choice(cursos)['id']
        alunos.append(i)
        dml_statements.append(
            f"INSERT INTO Aluno (id_aluno, nome, cpf, email, matricula, id_curso) VALUES "
            f"({i}, '{nome}', '{cpf}', '{(nome.split(' ')[0]).lower()}@alunoFEI.com.br', '{matricula}', {id_curso});"
        )

    # Inserindo Disciplinas
    disciplinas = []
    for i in range(1, 31):
        nome = f"Disciplina de {fake.word().capitalize()}"
        codigo = f"D{i:03}"
        id_departamento = random.choice(departamentos)['id']
        disciplinas.append({"id": i, "id_departamento": id_departamento})
        dml_statements.append(
            f"INSERT INTO Disciplina (id_disciplina, nome, codigo, id_departamento) VALUES "
            f"({i}, '{nome}', '{codigo}', {id_departamento});"
        )

    # Inserindo Histórico de Professores
    # Agora, para cada professor, selecionamos apenas as disciplinas do mesmo departamento.
    for professor in professores:
        # Filtra disciplinas que pertencem ao departamento do professor
        disciplinas_prof = [d for d in disciplinas if d['id_departamento'] == professor['id_departamento']]
        # Verifica se há disciplinas disponíveis para o departamento
        if not disciplinas_prof:
            continue
        for _ in range(random.randint(1, 4)):
            disciplina = random.choice(disciplinas_prof)
            semestre = gerar_semestre()
            dml_statements.append(
                f"INSERT INTO Historico_Professor (id_professor, id_disciplina, semestre) VALUES "
                f"({professor['id']}, {disciplina['id']}, '{semestre}');"
            )

    # Inserindo Histórico de Alunos
    # Para cada aluno, geramos os semestres e os processamos em ordem cronológica.
    # A lógica garante:
    #   - Se o aluno já foi aprovado em uma disciplina, não teremos novas tentativas para ela.
    #   - Se o aluno falhar, em uma tentativa subsequente essa disciplina será forçada à aprovação.
    #   - No último semestre, se restarem disciplinas com apenas reprovação, é inserida um registro forçado de aprovação.
    for aluno_id in alunos:
        aprovados = {}    # armazena disciplinas já aprovadas
        tentativas = {}   # armazena disciplinas já tentadas (falha) sem aprovação ainda

        # Gera um conjunto de semestres para o aluno
        num_semestres = random.randint(2, 4)
        semestres_set = set()
        while len(semestres_set) < num_semestres:
            semestres_set.add(gerar_semestre())

        # Converte as strings de semestre em tuplas para ordenar (ano, semestre, string_original)
        semestres_lista = []
        for s in semestres_set:
            ano_str, sem_str = s.split('/')
            semestres_lista.append((int(ano_str), int(sem_str), s))
        semestres_ordenados = sorted(semestres_lista, key=lambda x: (x[0], x[1]))

        # Para cada semestre (processados em ordem)
        for i, (_, _, semestre) in enumerate(semestres_ordenados):
            is_last = (i == len(semestres_ordenados) - 1)
            disciplinas_no_semestre = set()
            quantidade = random.randint(4, 6)
            iteracao = 0  # para evitar loops infinitos
            while len(disciplinas_no_semestre) < quantidade and iteracao < 100:
                iteracao += 1
                disciplina = random.choice(disciplinas)
                disciplina_id = disciplina['id']

                # Se disciplina já foi aprovada, não inserir nova tentativa
                if disciplina_id in aprovados:
                    continue

                # Evita duplicidade neste mesmo semestre
                if (semestre, disciplina_id) in disciplinas_no_semestre:
                    continue

                # Se já houve tentativa (falha) anterior, forçamos aprovação para essa disciplina nesta nova tentativa
                if disciplina_id in tentativas:
                    nota = round(random.uniform(5, 10), 2)
                    situacao = 'aprovado'
                else:
                    nota = round(random.uniform(0, 10), 2)
                    situacao = 'aprovado' if nota >= 5 else 'reprovado'

                professor_id = random.choice(professores)['id']
                dml_statements.append(
                    f"INSERT INTO Historico_Aluno (id_aluno, id_disciplina, semestre, nota, situacao, id_professor) VALUES "
                    f"({aluno_id}, {disciplina_id}, '{semestre}', {nota}, '{situacao}', {professor_id});"
                )

                if situacao == 'aprovado':
                    aprovados[disciplina_id] = 'aprovado'
                    # Se já houver registro de tentativa com falha, removemos, pois agora a disciplina foi aprovada
                    if disciplina_id in tentativas:
                        del tentativas[disciplina_id]
                else:
                    # Registra que houve tentativa (falha) para esta disciplina
                    if disciplina_id not in tentativas:
                        tentativas[disciplina_id] = 'reprovado'

                disciplinas_no_semestre.add((semestre, disciplina_id))

            # No último semestre, garantimos que disciplinas apenas com reprovação sejam finalmente aprovadas.
            if is_last:
                for disc_id in list(tentativas.keys()):
                    if any(disc_id == did for (_, did) in disciplinas_no_semestre):
                        continue
                    professor_id = random.choice(professores)['id']
                    nota = round(random.uniform(5, 10), 2)
                    situacao = 'aprovado'
                    dml_statements.append(
                        f"INSERT INTO Historico_Aluno (id_aluno, id_disciplina, semestre, nota, situacao, id_professor) VALUES "
                        f"({aluno_id}, {disc_id}, '{semestre}', {nota}, '{situacao}', {professor_id});"
                    )
                    aprovados[disc_id] = 'aprovado'
                    del tentativas[disc_id]
                    disciplinas_no_semestre.add((semestre, disc_id))

    # Inserindo TCCs
    for tcc_id in range(1, 21):
        titulo = fake.sentence(nb_words=6).replace("'", "")
        orientador_id = random.choice(professores)['id']
        dml_statements.append(
            f"INSERT INTO TCC (id_tcc, titulo, id_orientador) VALUES ({tcc_id}, '{titulo}', {orientador_id});"
        )

    # Inserindo alunos em TCCs (máximo 5 por TCC)
    alunos_disponiveis = alunos.copy()
    random.shuffle(alunos_disponiveis)
    for tcc_id in range(1, 21):
        num_alunos = min(5, len(alunos_disponiveis))
        alunos_tcc = [alunos_disponiveis.pop() for _ in range(num_alunos)]
        for aluno_id in alunos_tcc:
            dml_statements.append(
                f"INSERT INTO Aluno_TCC (id_tcc, id_aluno) VALUES ({tcc_id}, {aluno_id});"
            )

    return "\n".join(dml_statements)


# Gerando o arquivo DML
with open("sql/dml_script.sql", "w", encoding='utf-8') as file:
    file.write(gerar_dml())

print("Script DML gerado com sucesso!")
