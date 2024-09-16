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
        data_nascimento TEXT NOT NULL,
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
    data_nascimento = input("Digite a data de nascimento do Aluno (DD/MM/YYYY): ")
    print("\nAluno Cadastrado com Sucesso!\n")
    print("-------------------------------------------------------------")
    
    cursor.execute('''
    INSERT INTO alunos (matricula, nome, curso, data_nascimento)
    VALUES (?, ?, ?, ?)
    ''', (matricula, nome, curso, data_nascimento))
    
    conn.commit()

def consultar_aluno(cursor, conn):
    print("Opção 2 selecionada\n")
    matricula = input("Digite a matrícula do aluno: ")
    
    cursor.execute('SELECT * FROM alunos WHERE matricula = ?', (matricula,))
    aluno = cursor.fetchone()
    
    if aluno:
        print(f"\nDados do Aluno:\nMatrícula: {aluno[0]}\nNome: {aluno[1]}\nCurso: {aluno[2]}\nData de Nascimento: {aluno[3]}")
    else:
        print("Aluno não encontrado.")
    print("-------------------------------------------------------------")
   

def atualizar_aluno(cursor, conn):
    print("Opção 3 selecionada")
    

# Função para excluir alunos
def excluir_aluno(cursor, conn):
    print("Opção 4 selecionada\n")
    
    matricula = input("Digite a matrícula do aluno a ser excluído: ")
    
    cursor.execute('SELECT * FROM alunos WHERE matricula = ?', (matricula,))
    aluno = cursor.fetchone()
    
    if aluno:
        print(f"Confirma exclusão do aluno:\nMatrícula: {aluno[0]}\nNome: {aluno[1]}\nCurso: {aluno[2]}")
        confirmacao = input("Digite 'S' para confirmar, ou qualquer outra tecla para cancelar: ").upper()
        
        if confirmacao == 'S':
            cursor.execute('DELETE FROM alunos WHERE matricula = ?', (matricula,))
            conn.commit()
            print(f"\nAluno com matrícula {matricula} excluído com sucesso.\n")
        else:
            print("\nOperação cancelada.\n")
    else:
        print("\nAluno não encontrado.\n")
    
    print("-------------------------------------------------------------") 
    
# Função para listar alunos  
def listar_todos_alunos(cursor, conn):
    print("Opção 5 selecionada\n")
    
    cursor.execute('SELECT * FROM alunos')
    alunos = cursor.fetchall()
    
    if alunos:
        print("Lista de Alunos Cadastrados:\n")
        for aluno in alunos:
            print(f"Matrícula: {aluno[0]}, Nome: {aluno[1]}, Curso: {aluno[2]}, Data de Nascimento: {aluno[3]}")
            if aluno[4] is not None and aluno[5] is not None:
                print(f"Nota Av1: {aluno[4]}, Nota Av2: {aluno[5]}")
            print("-------------------------------------------------------------")
    else:
        print("Nenhum aluno cadastrado.\n")
    
    
def atualizar_nota(cursor, conn):
    print("Opção 6 selecionada\n")
    
    matricula = input("Digite a matrícula do aluno: ")
    av1 = float(input("Digite a nova nota da Av1: "))
    av2 = float(input("Digite a nova nota da Av2: "))
    
    cursor.execute('''
    UPDATE alunos
    SET av1 = ?, av2 = ?
    WHERE matricula = ?
    ''', (av1, av2, matricula))
    
    if cursor.rowcount == 0:
        print("\nAluno não encontrado. Cadastrando novo aluno...")
        nome = input("\nDigite o nome do Aluno: ")
        curso = input("Digite o curso do Aluno: ")
        data_nascimento = input("Digite a data de nascimento do Aluno (DD/MM/YYYY): ")
        
        
        cursor.execute('''
        INSERT INTO alunos (matricula, nome, curso, data_nascimento, av1, av2)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (matricula, nome, curso, data_nascimento, av1, av2))
        print("\nAluno cadastrado com sucesso!")
    else:
        print("\nNotas atualizadas com sucesso!")
    
    conn.commit()
    print("-------------------------------------------------------------")


def ver_nota_aluno(cursor, conn):
    print("Opção 7 selecionada\n")
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
            

def opcao_8(cursor, conn):
    print("Saindo do sistema...")
    conn.close()  # Fechar a conexão ao sair
    exit() # Encerrar o programa
    
opcoes = {
    '1': cadastrar_aluno,
    '2': consultar_aluno,
    '3': atualizar_aluno,
    '4': excluir_aluno,
    '5': listar_todos_alunos,
    '6': atualizar_nota,
    '7': ver_nota_aluno,
    '8': opcao_8,
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
        print("6. Adicionar ou Atualizar a Nota de um Aluno(a)")
        print("7. Ver Nota de um Aluno(a)")
        print("8. Sair")
        opcao = input("\nEscolha uma Opção: ")
        
        if opcao in opcoes:
            if opcao == '8':
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
