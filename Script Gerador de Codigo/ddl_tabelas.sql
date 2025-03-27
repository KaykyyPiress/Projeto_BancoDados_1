-- Tabela: Departamento
CREATE TABLE Departamento (
    id_departamento SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL
);

-- Tabela: Professor
CREATE TABLE Professor (
    id_professor SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    id_departamento INT REFERENCES Departamento(id_departamento),
    chefe_departamento BOOLEAN DEFAULT FALSE
);

-- Tabela: Curso
CREATE TABLE Curso (
    id_curso SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    id_departamento INT REFERENCES Departamento(id_departamento),
    id_coordenador INT REFERENCES Professor(id_professor)
);

-- Tabela: Aluno
CREATE TABLE Aluno (
    id_aluno SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    id_curso INT REFERENCES Curso(id_curso)
);

-- Tabela: Disciplina
CREATE TABLE Disciplina (
    id_disciplina SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    codigo VARCHAR(20) UNIQUE NOT NULL,
    id_departamento INT REFERENCES Departamento(id_departamento)
);

-- Tabela: HistoricoEscolar
CREATE TABLE HistoricoEscolar (
    id_historico SERIAL PRIMARY KEY,
    id_aluno INT REFERENCES Aluno(id_aluno),
    id_disciplina INT REFERENCES Disciplina(id_disciplina),
    semestre VARCHAR(10) NOT NULL,
    status VARCHAR(20) CHECK (status IN ('aprovado', 'reprovado')),
    id_professor INT REFERENCES Professor(id_professor)
);

-- Tabela: TCC
CREATE TABLE TCC (
    id_tcc SERIAL PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    id_orientador INT REFERENCES Professor(id_professor)
);

-- Tabela: Aluno_TCC
CREATE TABLE Aluno_TCC (
    id_aluno_tcc SERIAL PRIMARY KEY,
    id_tcc INT REFERENCES TCC(id_tcc),
    id_aluno INT REFERENCES Aluno(id_aluno),
    UNIQUE (id_tcc, id_aluno)
);
