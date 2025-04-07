# Sistema de Banco de Dados para Universidade

## 📚 Objetivo do Projeto
O objetivo deste projeto é implementar um sistema robusto de banco de dados para uma universidade. O sistema permite armazenar e gerenciar informações detalhadas sobre:

- **Alunos**
- **Professores**
- **Departamentos**
- **Cursos**
- **Disciplinas**
- **Históricos Escolares** (incluindo reprovações e aprovações subsequentes)
- **Histórico de Disciplinas Lecionadas por Professores**
- **Trabalhos de Conclusão de Curso (TCCs)**, considerando grupos de alunos e professores orientadores

---

## 🛠️ Estrutura do Projeto

O projeto contempla:
- Modelo Entidade-Relacionamento (ER)
- Modelo relacional em Terceira Forma Normal (3FN)
- Scripts SQL para criação (DDL) e manipulação dos dados
- Queries SQL específicas para testes funcionais
- Geração de dados fictícios para testes

---

## 📷 MER e ME
![ME](https://github.com/user-attachments/assets/142ceb4a-066a-4062-b6b2-f71e28e8fb9f)

![MER](https://github.com/user-attachments/assets/2e5983a9-1eec-4828-837a-d451f9072eac)

---

## ⚙️ Queries Implementadas

Foram implementadas queries SQL específicas para validar a integridade e funcionalidade do sistema:

1. **Histórico Escolar com Reprovação:**
   - Exibe o histórico completo de um aluno que foi reprovado em uma disciplina, mostrando reprovação e posterior aprovação.

2. **TCCs Orientados por Professor:**
   - Exibe todos os TCCs orientados por um professor específico, juntamente com os nomes dos alunos envolvidos.

3. **Matriz Curricular de Cursos com Disciplinas em Comum:**
   - Duas queries separadas, mostrando as matrizes curriculares de pelo menos dois cursos diferentes que compartilham disciplinas (ex.: Ciência da Computação e Ciência de Dados).

4. **Histórico das Disciplinas Cursadas por Aluno:**
   - Para um aluno específico, exibe os códigos e nomes das disciplinas já cursadas, acompanhados pelos nomes dos professores que as lecionaram.

5. **Chefes de Departamento e Coordenadores de Curso:**
   - Lista em uma única query todos os chefes de departamentos e coordenadores de cursos, substituindo campos vazios pelo texto "nenhum".

---

## 📂 Organização dos Arquivos

```
Projeto_Universidade/
├── docs/
│   ├── modelo_ER.png
│   └── modelo_relacional.png
├── sql/
│   ├── create_tables.sql
│   ├── insert_data.sql
│   └── queries.sql
├── data_generator/
│   └── generator.java
└── README.md
```

---

## 🚀 Como Executar

1. Clone o repositório.
2. Execute os scripts em ordem:
   - `create_tables.sql` (Criação do banco)
   - `insert_data.sql` (Popular o banco com dados fictícios)
   - `queries.sql` (Execução das queries específicas)

---

## 📝 Autor

- [Kayky Pires de Paula R.A.: 22.222.040-2](https://github.com/KaykyyPiress)
- [Mariane de Sousa Carvalho R.A.: 22.123.105-3](https://github.com/carvalhosmari)
- [Rafael Dias Silva Costa R.A.: 22.222.039-4](https://github.com/rafadias008)

---

📌 **Observação:** Projeto desenvolvido para fins acadêmicos, podendo ser adaptado para uso em cenários reais.

