import os
import random
from faker import Faker
from db_connection import get_connection

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
        "DELETE FROM Grade_Curso;",   
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
        profs_do_departamento = [p['id'] for p in professores if p['id_departamento'] == dept['id']]
        chefe = random.choice(profs_do_departamento)
        dml_statements.append(
            f"UPDATE Departamento SET id_chefe_departamento = {chefe} WHERE id_departamento = {dept['id']};"
        )

    # Inserindo Cursos
    nomes_cursos = ["Engenharia Civil", "Ciencia da Computacao", "Estatistica", "Fisica Computacional", "Quimica Aplicada"]
    for i, nome in enumerate(nomes_cursos, start=1):
        id_departamento = departamentos[i - 1]['id']
        profs_do_departamento = [p['id'] for p in professores if p['id_departamento'] == id_departamento]
        id_coordenador = random.choice(profs_do_departamento)
        cursos.append({"id": i, "id_departamento": id_departamento, "nome": nome})
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
        aluno = {'id': i, 'curso': id_curso}
        alunos.append(aluno)
        dml_statements.append(
            f"INSERT INTO Aluno (id_aluno, nome, cpf, email, matricula, id_curso) VALUES "
            f"({i}, '{nome}', '{cpf}', '{(nome.split(' ')[0]).lower()}@alunoFEI.com.br', '{matricula}', {id_curso});"
        )

    #DICIONARIO RELACIONANDO AS DISCIPLINAS COM OS CURSOS
    disciplinas_por_curso = {
        "Engenharia Civil": [
            "Mecânica dos Solos", "Estruturas de Concreto", "Construção Civil", 
            "Geotecnia", "Hidráulica", "Desenho Técnico"
        ],
        "Ciencia da Computacao": [
            "Algoritmos", "Estruturas de Dados", "Redes de Computadores", 
            "Banco de Dados", "Sistemas Operacionais", "Inteligência Artificial"
        ],
        "Estatistica": [
            "Probabilidade", "Inferência Estatística", "Modelos Lineares", 
            "Estatística Computacional", "Análise Multivariada", "Séries Temporais"
        ],
        "Fisica Computacional": [
            "Mecânica Computacional", "Simulações Numéricas", "Modelos Físicos", 
            "Termodinâmica Computacional", "Física Matemática", "Programação Científica"
        ],
        "Quimica Aplicada": [
            "Química Orgânica", "Química Inorgânica", "Fisico-Química", 
            "Química Industrial", "Química Analítica", "Química Ambiental"
        ]
    }
    
    # Inserindo Disciplinas relacionando-as aos cursos
    disciplinas = []
    discipline_counter = 1
    for curso in cursos:
        nome_curso = curso.get("nome")
        id_departamento = curso.get("id_departamento")
        # Caso haja disciplinas definidas para o curso
        if nome_curso in disciplinas_por_curso:
            for nome_disciplina in disciplinas_por_curso[nome_curso]:
                codigo = f"D{discipline_counter:03}"
                disciplinas.append({"id": discipline_counter, "id_departamento": id_departamento})
                dml_statements.append(
                    f"INSERT INTO Disciplina (id_disciplina, nome, codigo, id_departamento) VALUES "
                    f"({discipline_counter}, '{nome_disciplina}', '{codigo}', {id_departamento});"
                )
                discipline_counter += 1
    
        # Inserindo Histórico de Professores
        # Seleciona apenas disciplinas do mesmo departamento do professor.
        for professor in professores:
            disciplinas_prof = [d for d in disciplinas if d['id_departamento'] == professor['id_departamento']]
            
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
    # Lógica que garante que, se um aluno reprovou, em alguma tentativa posterior ele obterá aprovação.
    for aluno in alunos:
        aprovados = {}    # Registra disciplinas já aprovadas
        tentativas = {}   # Registra disciplinas já tentadas e com falha (ainda não aprovadas)

        curso_aluno = aluno['curso']
        departamento = 0
        
        for curso in cursos:
            if curso['id'] == curso_aluno:
                departamento = curso['id_departamento']

        disciplinas_curso = [d for d in disciplinas if d['id_departamento'] == departamento]
        profs_do_departamento = [p['id'] for p in professores if p['id_departamento'] == departamento]
   
        # Gera semestres únicos e ordenados cronologicamente para o aluno
        num_semestres = random.randint(2, 4)
        semestres_set = set()
        while len(semestres_set) < num_semestres:
            semestres_set.add(gerar_semestre())

        semestres_lista = []
        for s in semestres_set:
            ano_str, sem_str = s.split('/')
            semestres_lista.append((int(ano_str), int(sem_str), s))
        semestres_ordenados = sorted(semestres_lista, key=lambda x: (x[0], x[1]))

        # Processa cada semestre (em ordem)
        for i, (_, _, semestre) in enumerate(semestres_ordenados):
            is_last = (i == len(semestres_ordenados) - 1)
            disciplinas_no_semestre = set()
            quantidade = random.randint(4, 6)
            iteracao = 0
            while len(disciplinas_no_semestre) < quantidade and iteracao < 100:
                iteracao += 1
                disciplina = random.choice(disciplinas)
                disciplina_id = disciplina['id']

                if disciplina_id in aprovados:
                    continue  # Já aprovado, não tenta novamente

                if (semestre, disciplina_id) in disciplinas_no_semestre:
                    continue  # Evita duplicidade neste semestre

                # Se já houve tentativa (falha) anterior para essa disciplina, forçamos aprovação.
                if disciplina_id in tentativas:
                    nota = round(random.uniform(5, 10), 2)
                    situacao = 'aprovado'
                else:
                    nota = round(random.uniform(0, 10), 2)
                    situacao = 'aprovado' if nota >= 5 else 'reprovado'

                professor_id = random.choice(profs_do_departamento)
                dml_statements.append(
                    f"INSERT INTO Historico_Aluno (id_aluno, id_disciplina, semestre, nota, situacao, id_professor) VALUES "
                    f"({aluno['id']}, {disciplina_id}, '{semestre}', {nota}, '{situacao}', {professor_id});"
                )

                if situacao == 'aprovado':
                    aprovados[disciplina_id] = 'aprovado'
                    if disciplina_id in tentativas:
                        del tentativas[disciplina_id]
                else:
                    if disciplina_id not in tentativas:
                        tentativas[disciplina_id] = 'reprovado'

                disciplinas_no_semestre.add((semestre, disciplina_id))

            # No último semestre, garante que todas as disciplinas com tentativa anterior sejam aprovadas.
            if is_last:
                for disc_id in list(tentativas.keys()):
                    if any(disc_id == did for (_, did) in disciplinas_no_semestre):
                        continue
                    professor_id = random.choice(professores)['id']
                    nota = round(random.uniform(5, 10), 2)
                    situacao = 'aprovado'
                    dml_statements.append(
                        f"INSERT INTO Historico_Aluno (id_aluno, id_disciplina, semestre, nota, situacao, id_professor) VALUES "
                        f"({aluno['id']}, {disc_id}, '{semestre}', {nota}, '{situacao}', {professor_id});"
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
        num_alunos = random.randint(1,5)
        alunos_tcc = [alunos_disponiveis.pop() for _ in range(num_alunos)]
        for aluno_id in alunos_tcc:
            dml_statements.append(
                f"INSERT INTO Aluno_TCC (id_tcc, id_aluno) VALUES ({tcc_id}, {aluno_id['id']});"
            )

    # Gerando a matriz curricular do curso
    for c in cursos:
        random.shuffle(disciplinas)
        num_disc = random.randint(10,15)
        for i in range(1, num_disc):
            dml_statements.append(
                f"INSERT INTO Grade_Curso (id_curso, id_disciplina) VALUES ({c['id']}, {disciplinas[i]['id']});"
            )

    return "\n".join(dml_statements)


def execute_script_from_files():
    """
    Executa os scripts 'ddl_script.sql' e 'dml_script.sql' da raiz do projeto.
    O DDL é executado primeiro, e só se ele for bem-sucedido o DML é executado.
    """
    ddl_path = "sql/ddl_tabelas.sql"
    dml_path = "sql/dml_script.sql"

    try:
        with open(ddl_path, 'r', encoding='utf-8') as ddl_file:
            ddl_script = ddl_file.read()
        with open(dml_path, 'r', encoding='utf-8') as dml_file:
            dml_script = dml_file.read()

        conn = get_connection()
        cur = conn.cursor()
        print("Conectado ao Supabase com sucesso.")

        # Executa DDL
        if ddl_script:
            print("Executando script DDL...")
            for comando in ddl_script.split(";"):
                comando = comando.strip()
                if comando:
                    cur.execute(comando + ";")
            conn.commit()
            print("Script DDL executado com sucesso.")

        # Executa DML
        if dml_script:
            print("Executando script DML...")
            for comando in dml_script.split(";"):
                comando = comando.strip()
                if comando:
                    cur.execute(comando + ";")
            conn.commit()
            print("Script DML executado com sucesso.")

        cur.close()
        conn.close()
        print("Todos os comandos foram executados com sucesso.")

    except FileNotFoundError as fe:
        print(f"Arquivo não encontrado: {fe.filename}")
    except Exception as e:
        print(f"Erro ao executar os comandos no Supabase: {e}")

if __name__ == "__main__":
    # Gera o script DML
    script_dml = gerar_dml()

    # Opcional: gravar o script em um arquivo
    with open("sql/dml_script.sql", "w", encoding='utf-8') as file:
        file.write(script_dml)
    print("Script DML gerado e salvo com sucesso!")

    # Executa o script no Supabase
    execute_script_from_files()
