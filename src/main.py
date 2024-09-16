import sqlite3

# Função para conectar ao banco e criar a tabela
def inicializar_banco():
    conn = sqlite3.connect('dados_aluno.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS alunos (
        matricula INTEGER PRIMARY KEY,
        nome TEXT NOT NULL,
        curso TEXT NOT NULL,
        av1 REAL CHECK (av1 >= 0 AND av1 <= 10),  -- Nota da Avaliação 1
        av2 REAL CHECK (av2 >= 0 AND av2 <= 10)   -- Nota da Avaliação 2
    )
    ''')
    
    conn.commit()
    return conn, cursor

# Funções para cadastrar Alunos
def cadastrar_aluno(cursor, conn):
    print("Opção 1 selecionada\n")
    matricula = input("Digite a Matricula do Aluno: ")
    nome = input("Digite o nome do Aluno: ")
    curso = input("Digite o curso do Aluno: ")
    av1 = float(input("Digite a nota da Av1: "))
    av2 = float(input("Digite a nota da Av2: "))
    print("\nAluno Cadastrado com Sucesso!\n")
    print("-------------------------------------------------------------")
    
    cursor.execute('''
    INSERT INTO alunos (matricula, nome, curso, av1, av2)
    VALUES (?, ?, ?, ?, ?)
    ''', (matricula, nome, curso, av1, av2))
    
    conn.commit()

def consultar_aluno(cursor, conn):
    print("Opção 2 selecionada\n")
    matricula = input("Digite a matrícula do aluno: ")
    
    cursor.execute('SELECT * FROM alunos WHERE matricula = ?', (matricula,))
    aluno = cursor.fetchone()
    
    if aluno:
        print(f"Dados do Aluno:\nMatrícula: {aluno[0]}\nNome: {aluno[1]}\nCurso: {aluno[2]}\nAv1: {aluno[3]}\nAv2: {aluno[4]}")
    else:
        print("Aluno não encontrado.")
    print("-------------------------------------------------------------")
   

def atualizar_aluno(cursor, conn):
    print("Opção 3 selecionada")
    

def excluir_aluno(cursor, conn):
    print("Opção 4 selecionada")
    
    
def listar_todos_alunos(cursor, conn):
    print("Opção 5 selecionada")
   
    
def ver_nota_aluno(cursor, conn):
    print("Opção 6 selecionada\n")
    matricula = input("Digite a matrícula do aluno: ")
    cursor.execute('SELECT nome, curso, av1, av2 FROM alunos WHERE matricula = ?', (matricula,))
    result = cursor.fetchone()
    
    if result:
        nome, curso, av1, av2 = result
        
        media = (av1 + av2) / 2
        
        print(f"O Aluno(a): {nome}")
        print(f"Curso: {curso}")
        print(f"Obteve na Av1: {av1}")
        print(f"Obteve na Av2: {av2}")
        print(f"O Aluno(a) obteve uma média final de {media:.2f} nas avaliações.\n")
        print("-------------------------------------------------------------")
    else:
        print("Aluno não encontrado.\n")
        print("-------------------------------------------------------------")
            

def opcao_7(cursor, conn):
    print("Saindo do sistema...")
    conn.close()  # Fechar a conexão ao sair
    exit() # Encerrar o programa
    
opcoes = {
    '1': cadastrar_aluno,
    '2': consultar_aluno,
    '3': atualizar_aluno,
    '4': excluir_aluno,
    '5': listar_todos_alunos,
    '6': ver_nota_aluno,
    '7': opcao_7,
}

def main():
    conn, cursor = inicializar_banco()
    
    while True:
        print("Bem-vindo ao Sistema de Cadastro e Gestão de Notas Acadêmicas\n")
        print("1. Cadastrar Aluno(a)")
        print("2. Consultar dados do Aluno(a)")
        print("3. Atualizar dados do Aluno(a)")
        print("4. Excluir Aluno(a)")
        print("5. Listar todos os Aluno(a)")
        print("6. Ver Nota de um Aluno(a)")
        print("7. Sair")
        opcao = input("\nEscolha uma Opção: ")
        
        if opcao in opcoes:
            if opcao == '7':
                opcoes[opcao](cursor, conn)
                break  # Termina o loop principal após a opção 'Sair'
            else:
                opcoes[opcao](cursor, conn)
        else:
            print("Opção inválida")
        
    # Fechar a conexão após sair do loop
    conn.close()

if __name__ == '__main__':
    main()
