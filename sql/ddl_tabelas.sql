-- Tabela: Departamento (sem restrição inline para id_chefe_departamento)
CREATE TABLE Departamento (
    id_departamento SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    id_chefe_departamento INT  -- Será definida a FK posteriormente
);

-- Tabela: Professor
CREATE TABLE Professor (
    id_professor SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cpf VARCHAR(20) UNIQUE NOT NULL,
    email VARCHAR(100) NOT NULL,
    id_departamento INT REFERENCES Departamento(id_departamento) ON DELETE SET NULL
);

-- Adiciona a restrição de chave estrangeira na tabela Departamento, agora que Professor já existe
ALTER TABLE Departamento
    ADD CONSTRAINT fk_departamento_chefe
    FOREIGN KEY (id_chefe_departamento) REFERENCES Professor(id_professor) ON DELETE SET NULL;

-- Tabela: Curso
CREATE TABLE Curso (
    id_curso SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    id_departamento INT NOT NULL REFERENCES Departamento(id_departamento) ON DELETE CASCADE,
    id_coordenador INT REFERENCES Professor(id_professor) ON DELETE SET NULL
);

-- Tabela: Aluno
CREATE TABLE Aluno (
    id_aluno SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cpf VARCHAR(20) UNIQUE NOT NULL,
    email VARCHAR(100) NOT NULL,
    matricula VARCHAR(20) UNIQUE NOT NULL,
    id_curso INT REFERENCES Curso(id_curso) ON DELETE SET NULL
);

-- Tabela: Disciplina
CREATE TABLE Disciplina (
    id_disciplina SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    codigo VARCHAR(20) UNIQUE NOT NULL,
    id_departamento INT REFERENCES Departamento(id_departamento) ON DELETE SET NULL
);

-- Tabela: Historico_Aluno
CREATE TABLE Historico_Aluno (
    id_historico SERIAL PRIMARY KEY,
    id_aluno INT NOT NULL REFERENCES Aluno(id_aluno) ON DELETE CASCADE,
    id_disciplina INT NOT NULL REFERENCES Disciplina(id_disciplina),
    semestre VARCHAR(10) NOT NULL,
    nota DECIMAL(5,2) NOT NULL,
    situacao VARCHAR(20) CHECK (situacao IN ('aprovado', 'reprovado')),
    id_professor INT REFERENCES Professor(id_professor)
);

-- Tabela: Historico_Professor
CREATE TABLE Historico_Professor (
    id_historico SERIAL PRIMARY KEY,
    id_professor INT NOT NULL REFERENCES Professor(id_professor) ON DELETE CASCADE,
    id_disciplina INT NOT NULL REFERENCES Disciplina(id_disciplina),
    semestre VARCHAR(10) NOT NULL
);

-- Tabela: TCC
CREATE TABLE TCC (
    id_tcc SERIAL PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    id_orientador INT NOT NULL REFERENCES Professor(id_professor)
);

-- Tabela: Aluno_TCC
CREATE TABLE Aluno_TCC (
    id_tcc INT REFERENCES TCC(id_tcc),
    id_aluno INT REFERENCES Aluno(id_aluno),
    UNIQUE (id_tcc, id_aluno)
);
