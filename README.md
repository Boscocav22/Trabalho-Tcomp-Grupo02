ISSUE 1 — Leitura do arquivo e tratamento de erros globais
Responsavel: Bosco Lourimar Bezerra de Lima Filho
==========================================================

Arquivos da Issue 1:
  erros.py    -> classe ErroXML + funções que geram as mensagens padrão
  entrada.py  -> ler_arquivo(caminho): lista de (numero_linha, texto)
  main.py     -> orquestra os módulos e imprime o resultado

Versões provisórias (stubs) das outras issues, só para o main rodar:
  raiz.py     -> Issue 2 (validar_raiz)
  registro.py -> Issue 3 (validar_registro)
  tipos.py    -> Issue 4 (validar_tipos)
  Ao enviar a sua parte, substitua o arquivo correspondente mantendo
  o nome da função e o contrato descrito nos comentários dele.

Testes da Issue 1:
  acessos.xml                            -> XML válido (arquivo padrão do main)
  testes/valido.xml                      -> XML válido
  testes/valido_com_linhas_em_branco.xml -> válido; testa a numeração das linhas
  testes/vazio.xml                       -> inválido: arquivo vazio
  testes/so_espacos.xml                  -> inválido: só espaços/linhas em branco
  test_issue1.py                         -> testes automáticos

Como testar:
  python main.py                          -> Sucesso: Arquivo XML válido.
  python main.py testes/vazio.xml         -> Erro: Arquivo xml vazio
  python main.py testes/so_espacos.xml    -> Erro: Arquivo xml vazio
  python main.py testes/nao_existe.xml    -> Erro: Arquivo ... não encontrado
  python test_issue1.py                   -> roda todos os testes automáticos
