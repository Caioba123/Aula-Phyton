import sqlite3
import time

# =============================
# CONFIGURAÇÃO DO BANCO DE DADOS
# =============================
conn = sqlite3.connect("quiz.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    locked INTEGER DEFAULT 0
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS scores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    score INTEGER,
    FOREIGN KEY(user_id) REFERENCES users(id)
)
""")

conn.commit()


# =============================
# SISTEMA DE USUÁRIOS
# =============================
def criar_usuario():
    print("\n=== Criar nova conta ===")
    username = input("Escolha um nome de usuário: ")
    password = input("Escolha uma senha: ")

    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        print("Usuário criado com sucesso!")
    except:
        print("Erro: nome de usuário já existe.")


def login():
    print("\n=== Tela de Login ===")

    tentativas = 0
    while tentativas < 3:
        username = input("Usuário: ")
        password = input("Senha: ")

        cursor.execute("SELECT id, password, locked FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()

        if not user:
            print("Usuário não existe.\n")
            tentativas += 1
            continue

        user_id, correct_pass, locked = user

        if locked == 1:
            print("Conta bloqueada! Reinicie o programa ou aguarde.")
            return None

        if password == correct_pass:
            print("Login bem-sucedido!\n")
            return user_id

        else:
            print("Senha incorreta.\n")
            tentativas += 1

    print("Muitas tentativas! Conta bloqueada.")
    cursor.execute("UPDATE users SET locked = 1 WHERE username = ?", (username,))
    conn.commit()
    return None


# =============================
# QUIZ (20 perguntas)
# =============================

perguntas = [
    {
        "q": "Qual civilização construiu as pirâmides?",
        "a": ["A) Maias", "B) Egípcios", "C) Romanos", "D) Persas", "E) Gregos"],
        "c": "B"
    },
    {
        "q": "Quem foi o primeiro imperador romano?",
        "a": ["A) Nero", "B) Júlio César", "C) Augusto", "D) Trajano", "E) Tibério"],
        "c": "C"
    },
    {
        "q": "Em que ano ocorreu a queda do Império Romano do Ocidente?",
        "a": ["A) 395", "B) 410", "C) 476", "D) 509", "E) 612"],
        "c": "C"
    },
    {
        "q": "Quem foi o líder da Revolução Cubana?",
        "a": ["A) Fidel Castro", "B) Che Guevara", "C) Hugo Chávez", "D) Batista", "E) Stalin"],
        "c": "A"
    },
    {
        "q": "A Primeira Guerra Mundial começou em:",
        "a": ["A) 1912", "B) 1914", "C) 1918", "D) 1920", "E) 1930"],
        "c": "B"
    },
    {
        "q": "Onde surgiram as primeiras cidades da humanidade?",
        "a": ["A) Grécia", "B) Egito", "C) Mesopotâmia", "D) Roma", "E) Índia"],
        "c": "C"
    },
    {
        "q": "A Revolução Francesa começou em:",
        "a": ["A) 1776", "B) 1789", "C) 1804", "D) 1815", "E) 1750"],
        "c": "B"
    },
    {
        "q": "Quem descobriu o Brasil?",
        "a": ["A) Colombo", "B) Cabral", "C) Vasco da Gama", "D) Cortez", "E) Magalhães"],
        "c": "B"
    },
    {
        "q": "Que muralha famosa fica na China?",
        "a": ["A) Hadrian", "B) Górdia", "C) Grande Muralha", "D) Qinhu", "E) Sian"],
        "c": "C"
    },
    {
        "q": "Quem pintou a Mona Lisa?",
        "a": ["A) Michelangelo", "B) Raphael", "C) Da Vinci", "D) Donatello", "E) Botticelli"],
        "c": "C"
    },
    {
        "q": "A Segunda Guerra Mundial terminou em:",
        "a": ["A) 1942", "B) 1943", "C) 1944", "D) 1945", "E) 1946"],
        "c": "D"
    },
    {
        "q": "O Egito antigo se organizava às margens de qual rio?",
        "a": ["A) Tigre", "B) Eufrates", "C) Nilo", "D) Danúbio", "E) Indo"],
        "c": "C"
    },
    {
        "q": "Quem foi o autor de 'A República'?",
        "a": ["A) Sócrates", "B) Aristóteles", "C) Platão", "D) Pitágoras", "E) Heráclito"],
        "c": "C"
    },
    {
        "q": "A Guerra Fria envolveu principalmente:",
        "a": ["A) EUA x Alemanha", "B) EUA x URSS", "C) China x Japão", "D) França x Inglaterra", "E) EUA x China"],
        "c": "B"
    },
    {
        "q": "A Idade Média começou após a queda de qual império?",
        "a": ["A) Grego", "B) Babilônico", "C) Romano", "D) Persa", "E) Otomano"],
        "c": "C"
    },
    {
        "q": "Quem foi Napoleão Bonaparte?",
        "a": ["A) Rei francês", "B) Filósofo francês", "C) Militar e imperador", "D) Papa", "E) Explorador"],
        "c": "C"
    },
    {
        "q": "Em qual país surgiu a Revolução Industrial?",
        "a": ["A) Alemanha", "B) França", "C) EUA", "D) Inglaterra", "E) Rússia"],
        "c": "D"
    },
    {
        "q": "O muro de Berlim caiu em:",
        "a": ["A) 1985", "B) 1987", "C) 1988", "D) 1989", "E) 1991"],
        "c": "D"
    },
    {
        "q": "Qual era a capital do Império Bizantino?",
        "a": ["A) Roma", "B) Istambul", "C) Constantinopla", "D) Atenas", "E) Alexandria"],
        "c": "C"
    },
    {
        "q": "Quem foi o primeiro homem a pisar na Lua?",
        "a": ["A) Yuri Gagarin", "B) Neil Armstrong", "C) Buzz Aldrin", "D) Alan Shepard", "E) Collins"],
        "c": "B"
    }
]


def iniciar_quiz(user_id):
    print("\n=== Início do Quiz ===")
    pontos = 0

    for i, p in enumerate(perguntas):
        print(f"\nPergunta {i+1}: {p['q']}")
        for alt in p['a']:
            print(alt)
        resp = input("Resposta: ").upper()

        if resp == p['c']:
            pontos += 1

    print("\n=== Resultado Final ===")
    print(f"Sua pontuação: {pontos}/20")

    if pontos == 20:
        print("Perfeito! Parabéns!")
    elif pontos >= 15:
        print("Excelente desempenho!")
    elif pontos >= 10:
        print("Bom trabalho, continue estudando!")
    else:
        print("Precisa melhorar, continue praticando!")

    cursor.execute("INSERT INTO scores (user_id, score) VALUES (?, ?)", (user_id, pontos))
    conn.commit()


# =============================
# MENU DO SISTEMA
# =============================
def ver_placar(user_id):
    cursor.execute("SELECT score FROM scores WHERE user_id = ?", (user_id,))
    resultados = cursor.fetchall()

    print("\n=== Placar do Usuário ===")
    if not resultados:
        print("Nenhum jogo realizado ainda.")
    else:
        for i, r in enumerate(resultados):
            print(f"Partida {i+1}: {r[0]} pontos")


def menu_principal(user_id):
    while True:
        print("\n=== MENU ===")
        print("1 - Iniciar Quiz")
        print("2 - Ver Placar")
        print("3 - Logout")

        op = input("Escolha: ")

        if op == "1":
            iniciar_quiz(user_id)
        elif op == "2":
            ver_placar(user_id)
        elif op == "3":
            print("Saindo...")
            break
        else:
            print("Opção inválida!")


# =============================
# PROGRAMA PRINCIPAL
# =============================
def main():
    print("=== SISTEMA DE QUIZ COM LOGIN ===")

    while True:
        print("\n1 - Criar Usuário")
        print("2 - Login")
        print("3 - Sair")
        op = input("Escolha: ")

        if op == "1":
            criar_usuario()
        elif op == "2":
            user_id = login()
            if user_id:
                menu_principal(user_id)
        elif op == "3":
            print("Encerrando programa.")
            break
        else:
            print("Opção inválida!")

main()
conn.close()