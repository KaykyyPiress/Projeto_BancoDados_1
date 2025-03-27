import java.util.*;
import java.io.*;

public class GeradorUniversidade {
    private static Random random = new Random();
    private static String[] nomes = new String[100];
    private static String[] departamentos = new String[20];
    private static String[] cursos = new String[20];
    private static String[] disciplinas = new String[50];

    private static Scanner abrirArquivo(String nomeArquivo) {
        try {
            return new Scanner(new FileInputStream(nomeArquivo));
        } catch (FileNotFoundException e) {
            System.out.println("Erro ao abrir o arquivo: " + nomeArquivo);
            System.exit(0);
        }
        return null;
    }

    private static void carregarDados() {
        Scanner in;

        in = abrirArquivo("nomes.txt");
        int i = 0;
        while (in.hasNextLine() && i < nomes.length) {
            nomes[i++] = in.nextLine();
        }
        in.close();

        in = abrirArquivo("departamentos.txt");
        i = 0;
        while (in.hasNextLine() && i < departamentos.length) {
            departamentos[i++] = in.nextLine();
        }
        in.close();

        in = abrirArquivo("cursos.txt");
        i = 0;
        while (in.hasNextLine() && i < cursos.length) {
            cursos[i++] = in.nextLine();
        }
        in.close();

        in = abrirArquivo("disciplinas.txt");
        i = 0;
        while (in.hasNextLine() && i < disciplinas.length) {
            disciplinas[i++] = in.nextLine();
        }
        in.close();
    }

    private static String aspas(String texto) {
        return "'" + texto + "'";
    }

    public static void main(String[] args) {
        carregarDados();

        try {
            PrintWriter out = new PrintWriter(new FileOutputStream("inserts_universidade.sql"));

            // Insere departamentos
            int qtdDepartamentos = 5;
            for (int i = 0; i < qtdDepartamentos; i++) {
                out.println("INSERT INTO Departamento (nome) VALUES (" + aspas(departamentos[i]) + ");");
            }

            // Insere professores
            int qtdProfessores = 10;
            for (int i = 0; i < qtdProfessores; i++) {
                String nome = nomes[random.nextInt(nomes.length)];
                int idDepartamento = random.nextInt(qtdDepartamentos) + 1;
                boolean chefe = random.nextBoolean();
                out.println("INSERT INTO Professor (nome, id_departamento, chefe_departamento) VALUES (" +
                    aspas(nome) + ", " + idDepartamento + ", " + chefe + ");");
            }

            // Insere cursos
            int qtdCursos = 4;
            for (int i = 0; i < qtdCursos; i++) {
                String nome = cursos[i];
                int idDepartamento = random.nextInt(qtdDepartamentos) + 1;
                int idCoordenador = random.nextInt(qtdProfessores) + 1;
                out.println("INSERT INTO Curso (nome, id_departamento, id_coordenador) VALUES (" +
                    aspas(nome) + ", " + idDepartamento + ", " + idCoordenador + ");");
            }

            // Insere alunos
            int qtdAlunos = 100;
            for (int i = 0; i < qtdAlunos; i++) {
                String nome = nomes[random.nextInt(nomes.length)];
                int idCurso = random.nextInt(qtdCursos) + 1;
                out.println("INSERT INTO Aluno (nome, id_curso) VALUES (" +
                    aspas(nome) + ", " + idCurso + ");");
            }

            // Insere disciplinas
            int qtdDisciplinas = 10;
            for (int i = 0; i < qtdDisciplinas; i++) {
                String nome = disciplinas[i];
                String codigo = "D" + (100 + i);
                int idDepartamento = random.nextInt(qtdDepartamentos) + 1;
                out.println("INSERT INTO Disciplina (nome, codigo, id_departamento) VALUES (" +
                    aspas(nome) + ", " + aspas(codigo) + ", " + idDepartamento + ");");
            }

            // Semestres em ordem cronológica
            String[] semestresValidos = {
                "2020/1", "2020/2", "2021/1", "2021/2",
                "2022/1", "2022/2", "2023/1", "2023/2"
            };

            // Para cada aluno, gera histórico em ordem cronológica
            for (int alunoId = 1; alunoId <= qtdAlunos; alunoId++) {
                // Quantidade de semestres para esse aluno: de 4 a 8
                int qtdSemestres = 4 + random.nextInt(5);

                // Escolhe semestres de forma aleatória, mas manteremos ORDEM
                // 1) Seleciona índices únicos
                Set<Integer> indices = new HashSet<>();
                while (indices.size() < qtdSemestres) {
                    indices.add(random.nextInt(semestresValidos.length));
                }
                // 2) Ordena esses índices
                List<Integer> listaIndices = new ArrayList<>(indices);
                Collections.sort(listaIndices);

                // Mapeia disciplina -> status final (pra saber se já foi aprovado)
                Map<Integer, String> disciplinaStatus = new HashMap<>();

                // Percorre semestres em ordem cronológica
                for (Integer idxSemestre : listaIndices) {
                    String semestre = semestresValidos[idxSemestre];

                    // Escolhe quantas disciplinas nesse semestre (1 ou 2)
                    int qtdDisciplinasSemestre = 1 + random.nextInt(2);

                    for (int d = 0; d < qtdDisciplinasSemestre; d++) {
                        int idDisciplina = random.nextInt(qtdDisciplinas) + 1;

                        // Se aluno já aprovou essa disciplina em semestre anterior, pula
                        if ("aprovado".equals(disciplinaStatus.get(idDisciplina))) {
                            continue;
                        }

                        // Caso contrário, define status aleatório
                        // (pode ser "aprovado" ou "reprovado")
                        String status = random.nextBoolean() ? "aprovado" : "reprovado";

                        // Atualiza status da disciplina
                        disciplinaStatus.put(idDisciplina, status);

                        // Define professor
                        int idProfessor = random.nextInt(qtdProfessores) + 1;

                        // Gera INSERT
                        out.println("INSERT INTO HistoricoEscolar (id_aluno, id_disciplina, semestre, status, id_professor) VALUES (" +
                            alunoId + ", " + idDisciplina + ", " + aspas(semestre) + ", " + aspas(status) + ", " + idProfessor + ");");
                    }
                }
            }

            // TCC
            int qtdTCCs = 5;
            for (int tccId = 1; tccId <= qtdTCCs; tccId++) {
                String titulo = "TCC " + tccId;
                int idOrientador = random.nextInt(qtdProfessores) + 1;
                out.println("INSERT INTO TCC (titulo, id_orientador) VALUES (" +
                    aspas(titulo) + ", " + idOrientador + ");");

                // Escolhe 2 alunos para esse TCC
                List<Integer> grupo = new ArrayList<>();
                while (grupo.size() < 2) {
                    int alunoId = random.nextInt(qtdAlunos) + 1;
                    if (!grupo.contains(alunoId)) {
                        grupo.add(alunoId);
                    }
                }
                for (Integer idAluno : grupo) {
                    out.println("INSERT INTO Aluno_TCC (id_tcc, id_aluno) VALUES (" +
                        tccId + ", " + idAluno + ");");
                }
            }

            out.close();
            System.out.println("Arquivo 'inserts_universidade.sql' gerado com sucesso.");
        } catch (IOException e) {
            System.out.println("Erro ao gerar o arquivo SQL.");
        }
    }
}
