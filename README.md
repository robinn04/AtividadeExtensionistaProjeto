Com certeza! Vou estruturar um `README.md` profissional e organizado para o seu projeto, focado na experiência do usuário e do desenvolvedor.

---

# Atividade Extensionista: Jogo Matemático

Este projeto é um jogo educativo desenvolvido em Python para o projeto extensionista da Uninter. O objetivo é desafiar o raciocínio rápido através de cálculos matemáticos divididos por níveis de dificuldade e categorias.

## 🎮 Sobre o Jogo

O jogo consiste em resolver expressões matemáticas para avançar de nível e acumular pontos. São **20 níveis** no total, divididos em blocos de 5 para cada operação aritmética fundamental.

### Sistema de Pontuação e Níveis

A pontuação é progressiva de acordo com a dificuldade da operação:

| Níveis | Operação | Pontos por Acerto |
| --- | --- | --- |
| **1 ao 5** | Adição (+) | +1 ponto |
| **6 ao 10** | Subtração (-) | +2 pontos |
| **11 ao 15** | Multiplicação (×) | +3 pontos |
| **16 ao 20** | Divisão (÷) | +4 pontos |

O jogo conta com um **sistema de ranking**, onde as melhores pontuações são salvas localmente no arquivo `scores.json`.

---

## 🚀 Como Rodar a Versão Compilada (Pasta `dist`)

Se você deseja apenas jogar sem precisar instalar o Python ou abrir o código, utilize a versão executável:

1. Acesse a pasta `dist` no diretório do projeto.
2. Localize o arquivo executável (geralmente `main.exe` no Windows).
3. **Importante:** Certifique-se de que a pasta `sons` (se houver dependência de áudio externa) e o arquivo `scores.json` estejam no mesmo diretório ou conforme a estrutura original para que o jogo funcione corretamente.
4. Dê um clique duplo no executável e divirta-se!

---

## 💻 Como Abrir e Rodar no PyCharm (Desenvolvedor)

Se você deseja visualizar o código ou fazer alterações, siga estes passos:

### 1. Pré-requisitos

Certifique-se de ter o **Python 3.x** instalado em sua máquina.

### 2. Abrindo o Projeto

1. Abra o **PyCharm**.
2. Vá em `File > Open...` e selecione a pasta raiz do projeto (`AtividadeExtensionistaProjeto`).
3. O PyCharm pode perguntar se você deseja criar um ambiente virtual (venv). Clique em **OK** ou **Create**.

### 3. Instalando Dependências

O jogo utiliza bibliotecas padrão e possivelmente bibliotecas externas para a interface ou áudio. No terminal do PyCharm, verifique se precisa instalar algo (exemplo comum para jogos simples):

```bash
pip install pygame

```

*(Caso você tenha usado apenas bibliotecas nativas como `tkinter`, `json` ou `random`, ignore este passo).*

### 4. Executando

1. No painel esquerdo (Project), localize o arquivo `main.py`.
2. Clique com o botão direito sobre ele e selecione **Run 'main'**.

---

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python
* **Persistência de Dados:** JSON (para o ranking de scores)
* **Interface:** (Exemplo: Tkinter / Pygame / Console)
* **Compilação:** PyInstaller (usado para gerar a pasta `dist`)

---

**Desenvolvido por:** Robinson - Projeto Uninter.

---

Você gostaria que eu adicionasse mais algum detalhe específico sobre as regras do jogo ou talvez uma seção de "créditos" com o seu RU?
