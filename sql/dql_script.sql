-- histórico escolar de um aluno que teve reprovação em uma disciplina, retornando inclusive a reprovação em um semestre e a aprovação no semestre seguinte
SELECT 
    ha.id_aluno,
    a.nome AS nome_aluno,
	d.id_disciplina,
    d.nome AS nome_disciplina,
    ha.semestre,
    ha.nota,
    ha.situacao

FROM Historico_Aluno ha

LEFT JOIN Aluno a ON ha.id_aluno = a.id_aluno
LEFT JOIN Disciplina d ON ha.id_disciplina = d.id_disciplina

WHERE ha.id_aluno IN (
	SELECT distinct r.id_aluno FROM Historico_Aluno r
    LEFT JOIN Historico_Aluno a ON r.id_aluno = a.id_aluno AND r.id_disciplina = a.id_disciplina
    WHERE r.situacao = 'reprovado' AND a.situacao = 'aprovado' AND a.semestre > r.semestre
	LIMIT 1
)

ORDER BY ha.id_aluno, d.id_disciplina, ha.semestre;


-- todos os TCCs orientados por um professor junto com os nomes dos alunos que fizeram o projeto
SELECT 
	tcc.id_tcc, 
	tcc.titulo, 
	tcc.id_orientador, 
	p.nome as nome_prof, 
	a.id_aluno, 
	a.nome as nome_aluno 

FROM tcc 

LEFT JOIN professor p ON tcc.id_orientador = p.id_professor
LEFT JOIN aluno_tcc atcc ON tcc.id_tcc = atcc.id_tcc
LEFT JOIN aluno a ON atcc.id_aluno = a.id_aluno

WHERE tcc.id_orientador IN (SELECT DISTINCT id_orientador FROM tcc LIMIT 1)

ORDER BY tcc.id_orientador, tcc.id_tcc


-- matriz curicular de pelo menos 2 cursos diferentes que possuem disciplinas em comum

-- Ciencia da computação
SELECT 
    c.nome AS nome_curso,
    d.nome AS nome_disciplina,
    d.codigo

FROM grade_curso gc

LEFT JOIN curso c ON gc.id_curso = c.id_curso
LEFT JOIN disciplina d ON gc.id_disciplina = d.id_disciplina

WHERE c.nome = 'Ciencia da Computacao' AND gc.id_disciplina IN (
      SELECT id_disciplina
      FROM Grade_Curso
      WHERE id_curso IN (SELECT id_curso FROM Curso WHERE nome IN ('Ciencia da Computacao', 'Engenharia Civil'))
      GROUP BY id_disciplina
      HAVING COUNT(DISTINCT id_curso) >= 2
  )
  
ORDER BY d.nome;

-- Engenharia Civil
SELECT 
    c.nome AS nome_curso,
    d.nome AS nome_disciplina,
    d.codigo

FROM grade_curso gc

LEFT JOIN curso c ON gc.id_curso = c.id_curso
LEFT JOIN disciplina d ON gc.id_disciplina = d.id_disciplina

WHERE c.nome = 'Engenharia Civil' AND gc.id_disciplina IN (
      SELECT id_disciplina
      FROM Grade_Curso
      WHERE id_curso IN (SELECT id_curso FROM Curso WHERE nome IN ('Ciencia da Computacao', 'Engenharia Civil'))
      GROUP BY id_disciplina
      HAVING COUNT(DISTINCT id_curso) >= 2
  )
  
ORDER BY d.nome;


-- Para um determinado aluno, mostre os códigos e nomes das diciplinas já cursadas junto com os nomes dos professores que lecionaram a disciplina para o aluno
SELECT 
	ha.id_aluno, 
	ha.semestre, 
	d.id_disciplina, 
	d.codigo, 
	d.nome, 
	p.id_professor, 
	p.nome as nom_prof 

FROM historico_aluno ha 

LEFT JOIN disciplina d ON ha.id_disciplina = d.id_disciplina
LEFT JOIN professor p ON ha.id_professor = p.id_professor

WHERE id_aluno = 12 -- pode substituir por outro id_aluno para testar

ORDER BY id_aluno, ha.id_disciplina, semestre 


-- Liste todos os chefes de departamento e coordenadores de curso
SELECT 
	p.nome as nom_prof, 
	COALESCE(d.nome, 'nenhum') as chefe_dpto, 
	COALESCE(c.nome, 'nenhum') as coord_curso 

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



--Encontre os estudantes que estão matriculados em cursos oferecidos pelo departamento de "Tecnologia da Informação".

SELECT 
	aluno.nome
FROM aluno 
LEFT JOIN curso ON aluno.id_curso = curso.id_curso
LEFT JOIN departamento ON departamento.id_departamento = curso.id_departamento
WHERE departamento.nome = 'Tecnologia da Informacao'


--Recupere os IDs dos estudantes que não estão matriculados em nenhum curso do departamento de "Tecnologia da Informação".

SELECT 
	aluno.id_aluno
FROM aluno
LEFT JOIN curso ON aluno.id_curso = curso.id_curso
LEFT JOIN departamento ON departamento.id_departamento = curso.id_departamento
WHERE departamento.nome NOT IN ('Tecnologia da Informacao')

--Encontre o número de alunos matriculados em cada curso e liste-os por título de curso.

SELECT 
	curso.nome,
	COUNT(id_aluno)
FROM aluno
LEFT JOIN curso ON aluno.id_curso = curso.id_curso
GROUP BY curso.nome
