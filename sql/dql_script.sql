-- histórico escolar de um aluno que teve reprovação em uma disciplina, retornando inclusive a reprovação em um semestre e a aprovação no semestre seguinte
SELECT * 
FROM historico_aluno 
WHERE id_aluno = 55 -- pode substituir por outro id_aluno para testar
ORDER BY id_aluno, id_disciplina, semestre 


-- todos os TCCs orientados por um professor junto com os nomes dos alunos que fizeram o projeto
WITH tccs_prof AS (
	SELECT id_orientador, COUNT(DISTINCT id_tcc) 
	FROM tcc 
	GROUP BY id_orientador 
	ORDER BY COUNT(DISTINCT id_tcc) DESC 
	LIMIT 1
)

SELECT tcc.id_tcc, tcc.titulo, tcc.id_orientador, p.nome as nome_prof, a.id_aluno, a.nome as nome_aluno 
FROM tcc 
INNER JOIN tccs_prof ON tcc.id_orientador = tccs_prof.id_orientador
LEFT JOIN professor p ON tcc.id_orientador = p.id_professor
LEFT JOIN aluno_tcc atcc ON tcc.id_tcc = atcc.id_tcc
LEFT JOIN aluno a ON atcc.id_aluno = a.id_aluno


-- matriz curicular de pelo menos 2 cursos diferentes que possuem disciplinas em comum
WITH disc_curso AS (
	SELECT DISTINCT id_disciplina, COUNT(DISTINCT id_curso)
	FROM grade_curso
	GROUP BY id_disciplina
	ORDER BY COUNT(DISTINCT id_curso) DESC
	LIMIT 1
),

cur_dist as (
	SELECT DISTINCT id_curso FROM grade_curso gc
	INNER JOIN disc_curso dc ON gc.id_disciplina = dc.id_disciplina
)

SELECT c.id_curso, c.nome as nom_curso, d.id_disciplina, d.nome as nom_disciplina 
FROM curso c
INNER JOIN cur_dist cd ON c.id_curso = cd.id_curso
LEFT JOIN grade_curso gc ON c.id_curso = gc.id_curso
LEFT JOIN disciplina d ON gc.id_disciplina = d.id_disciplina
LEFT JOIN disc_curso dc ON d.id_disciplina = dc.id_disciplina
ORDER BY c.id_curso, d.id_disciplina

-- Para um determinado aluno, mostre os códigos e nomes das diciplinas já cursadas junto com os nomes dos professores que lecionaram a disciplina para o aluno
SELECT ha.id_aluno, ha.semestre, d.id_disciplina, d.codigo, d.nome, p.id_professor, p.nome as nom_prof 
FROM historico_aluno ha 
LEFT JOIN disciplina d ON ha.id_disciplina = d.id_disciplina
LEFT JOIN professor p ON ha.id_professor = p.id_professor
WHERE id_aluno = 12 -- pode substituir por outro id_aluno para testar
ORDER BY id_aluno, ha.id_disciplina, semestre 


-- Liste todos os chefes de departamento e coordenadores de curso
SELECT p.nome as nom_prof, COALESCE(d.nome, 'nenhum') as chefe_dpto, COALESCE(c.nome, 'nenhum') as coord_curso 
FROM professor p
LEFT JOIN departamento d ON p.id_professor = d.id_chefe_departamento
LEFT JOIN curso c ON p.id_professor = c.id_coordenador


--Encontre os nomes de todos os estudantes.
SELECT nome
FROM Aluno;

--Liste os IDs e nomes de todos os professores.
SELECT id_professor, nome
FROM Professor;

--Encontre os nomes de todos os estudantes que cursaram "Engenharia Civil"
SELECT a.nome AS NomeEstudante,
       c.nome AS NomeCurso
FROM Aluno a
JOIN Curso c ON a.id_curso = c.id_curso
WHERE c.nome = 'Engenharia Civil';

-- Encontre o número total de estudantes que cursaram "Engenharia Civil"
SELECT COUNT(*) AS total_estudantes
FROM Aluno a
JOIN Curso c ON a.id_curso = c.id_curso
WHERE c.nome = 'Engenharia Civil';

--Liste os professores que ministraram cursos com mais de 20 alunos matriculados
SELECT p.id_professor, p.nome
FROM Professor p
JOIN Curso c ON p.id_professor = c.id_coordenador
JOIN Aluno a ON c.id_curso = a.id_curso
GROUP BY p.id_professor, p.nome
HAVING COUNT(a.id_aluno) > 20;

--encontre os nomes dos professores que ministraram cursos nos quais todos os alunos receberam nota '10'.
SELECT DISTINCT p.nome
FROM Professor p
JOIN (
    SELECT ha.id_professor, ha.id_disciplina, ha.semestre
    FROM Historico_Aluno ha
    GROUP BY ha.id_professor, ha.id_disciplina, ha.semestre
    HAVING MIN(ha.nota) = 10 AND MAX(ha.nota) = 10
) AS cursos_com_10
ON p.id_professor = cursos_com_10.id_professor;


