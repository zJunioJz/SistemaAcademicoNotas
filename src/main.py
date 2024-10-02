import sqlite3

def inicializar_banco():
    # Conecta ao banco de dados 'dados_aluno.db' e cria a tabela 'alunos' se não existir.
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

def validar_matricula(cursor, matricula):
    # Verifica se a matrícula é um número inteiro e se existe no banco de dados.
    if not matricula.isdigit():
        print("A matrícula deve ser um número inteiro.")
        return False

    cursor.execute('SELECT * FROM alunos WHERE matricula = ?', (matricula,))
    if cursor.fetchone():
        return True

    print("Matrícula não encontrada.")
    return False

def cadastrar_aluno(cursor, conn):
    # Função para cadastrar um novo aluno no banco de dados.
    print("Opção 1 selecionada\n")
    matricula = input("Digite a Matricula do Aluno: ")

    if not validar_matricula(cursor, matricula):
        # Solicita os dados do aluno se a matrícula não estiver cadastrada.
        nome = input("Digite o nome do Aluno: ")
        curso = input("Digite o curso do Aluno: ")
        data_nascimento = input("Digite a data de nascimento do Aluno (DD/MM/YYYY): ")
        
        cursor.execute(''' 
        INSERT INTO alunos (matricula, nome, curso, data_nascimento)
        VALUES (?, ?, ?, ?)
        ''', (matricula, nome, curso, data_nascimento))
        
        conn.commit()
        print("\nAluno Cadastrado com Sucesso!\n")
    else:
        print("A matrícula já está cadastrada.")

    print("-------------------------------------------------------------")

def consultar_aluno(cursor, conn):
    # Função para consultar os dados de um aluno.
    print("Opção 2 selecionada\n")
    matricula = input("Digite a matrícula do aluno: ")
    
    if validar_matricula(cursor, matricula):
        cursor.execute('SELECT * FROM alunos WHERE matricula = ?', (matricula,))
        aluno = cursor.fetchone()
        
        if aluno:
            print(f"\nDados do Aluno:\nMatrícula: {aluno[0]}\nNome: {aluno[1]}\nCurso: {aluno[2]}\nData de Nascimento: {aluno[3]}")
        else:
            print("Aluno não encontrado.")
    print("-------------------------------------------------------------")

def atualizar_aluno(cursor, conn):
    # Função para atualizar os dados de um aluno existente.
    print("Opção 3 selecionada")
    matricula = input("Digite a matrícula do aluno a ser atualizada: ")

    if validar_matricula(cursor, matricula):
        cursor.execute('SELECT * FROM alunos WHERE matricula = ?', (matricula,))
        aluno = cursor.fetchone()
        
        if aluno:
            print(f"Dados atuais do aluno:\nMatrícula: {aluno[0]}\nNome: {aluno[1]}\nCurso: {aluno[2]}\nData de Nascimento: {aluno[3]}")
            print("\nDeixe em branco para manter o valor atual.")
            
            novo_nome = input(f"Novo nome [{aluno[1]}]: ") or aluno[1]
            novo_curso = input(f"Novo curso [{aluno[2]}]: ") or aluno[2]
            nova_data_nascimento = input(f"Nova data de nascimento (DD/MM/YYYY) [{aluno[3]}]: ") or aluno[3]
           
            cursor.execute(''' 
            UPDATE alunos
            SET nome = ?, curso = ?, data_nascimento = ?
            WHERE matricula = ?
            ''', (novo_nome, novo_curso, nova_data_nascimento, matricula))
           
            conn.commit()
            print("\nDados do aluno atualizados com sucesso!\n")
        else:
            print("\nAluno não encontrado.\n")
    print("-------------------------------------------------------------")

def excluir_aluno(cursor, conn):
    # Função para excluir um aluno do banco de dados.
    print("Opção 4 selecionada\n")
    
    matricula = input("Digite a matrícula do aluno a ser excluído: ")

    if validar_matricula(cursor, matricula):
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

def listar_todos_alunos(cursor, conn):
    # Função para listar todos os alunos cadastrados.
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

def menu_nota(cursor, conn):
    # Menu para gerenciar notas dos alunos.
    while True:
        print("Opção 6 selecionada\n")
        print("1. Adicionar/Atualizar notas")
        print("2. Ver notas do aluno")
        print("3. Voltar ao menu principal")

        opcao = input("\nEscolha uma opção: ")

        if opcao == '1':
            matricula = input("Digite a matrícula do aluno: ")
            if validar_matricula(cursor, matricula):
                av1 = float(input("Digite a nova nota da Av1: "))
                av2 = float(input("Digite a nova nota da Av2: "))

                cursor.execute('''UPDATE alunos SET av1 = ?, av2 = ? WHERE matricula = ?''', (av1, av2, matricula))
                conn.commit()
                print("\nNotas atualizadas com sucesso!")
            else:
                print("\nAluno não encontrado. Não é possível atualizar as notas.")

        elif opcao == '2':
            matricula = input("Digite a matrícula do aluno: ")
            if validar_matricula(cursor, matricula):
                cursor.execute('SELECT nome, curso, av1, av2 FROM alunos WHERE matricula = ?', (matricula,))
                result = cursor.fetchone()
                
                if result:
                    nome, curso, av1, av2 = result
                    media = (av1 + av2) / 2 if av1 is not None and av2 is not None else 0
                    print(f"O Aluno(a): {nome}")
                    print(f"Curso: {curso}")
                    print(f"Obteve na Av1: {av1}")
                    print(f"Obteve na Av2: {av2}")
                    print(f"O Aluno(a) obteve uma média final de {media:.2f} nas avaliações.\n")
                else:
                    print("Aluno não encontrado.\n")

        elif opcao == '3':
            break  # Sai do loop e volta ao menu principal

        else:
            print("Opção inválida. Tente novamente.")

        print("-------------------------------------------------------------")

def opcao_7(cursor, conn):
    # Função para sair do sistema.
    print("Saindo do sistema...")
    conn.close()  # Fechar a conexão ao sair
    exit()  # Encerrar o programa
    
opcoes = {
    '1': cadastrar_aluno,
    '2': consultar_aluno,
    '3': atualizar_aluno,
    '4': excluir_aluno,
    '5': listar_todos_alunos,
    '6': menu_nota,
    '7': opcao_7,
}

def main():
    # Função principal que inicializa o banco e exibe o menu do sistema.
    conn, cursor = inicializar_banco()
    
    while True:
        print("Bem-vindo ao Sistema de Cadastro e Gestão de Notas Acadêmicas\n")
        print("1. Cadastrar Aluno(a)")
        print("2. Consultar dados do Aluno(a)")
        print("3. Atualizar dados do Aluno(a)")
        print("4. Excluir Aluno(a)")
        print("5. Listar todos os Aluno(a)")
        print("6. Menu: Notas")
        print("7. Sair")
        
        opcao = input("\nEscolha uma opção: ")
        
        if opcao in opcoes:
            opcoes[opcao](cursor, conn)  # Chama a função correspondente da opção escolhida
        else:
            print("Opção inválida. Tente novamente.")

# Executa a função principal
if __name__ == "__main__":
    main()
