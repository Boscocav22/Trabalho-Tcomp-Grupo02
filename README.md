ISSUE 1 -- Leitura do arquivo e tratamento de erros globais
Responsavel: Bosco Lourimar Bezerra de Lima Filho
==========================================================

Arquivos da Issue 1:
  erros.py    -> classe ErroXML + funcoes que geram as mensagens padrao
  entrada.py  -> ler_arquivo(caminho): lista de (numero_linha, texto)
  main.py     -> orquestra os modulos e imprime o resultado

Modulos das outras issues:
  raiz.py     -> Issue 2 (validar_raiz)
  registro.py -> Issue 3 (validar_registro)
  tipos.py    -> Issue 4 (validar_tipos)

Testes da Issue 1:
  acessos.xml                            -> XML valido (arquivo padrao do main)
  testes/valido.xml                      -> XML valido
  testes/valido_com_linhas_em_branco.xml -> valido; testa a numeracao das linhas
  testes/vazio.xml                       -> invalido: arquivo vazio
  testes/so_espacos.xml                  -> invalido: so espacos/linhas em branco
  test_issue1.py                         -> testes automaticos

Como testar:
  python main.py                          -> Sucesso: Arquivo XML valido.
  python main.py testes/vazio.xml         -> Erro: Arquivo xml vazio
  python main.py testes/so_espacos.xml    -> Erro: Arquivo xml vazio
  python main.py testes/nao_existe.xml    -> Erro: Arquivo ... nao encontrado
  python test_issue1.py                   -> roda todos os testes automaticos


ISSUE 2 -- Validacao Sintatica do Elemento Raiz <acessos>
==========================================================

Arquivos da Issue 2:
  raiz.py        -> validar_raiz(linhas): valida as tags externas de <acessos>
                    e devolve as linhas internas para validacao dos registros.
  test_issue2.py -> testes automaticos

A validacao verifica se o documento comeca com <acessos>, termina com
</acessos> e nao contem outras tags raiz no meio. Em caso de erro, levanta
ErroXML por meio de erro_sintatico(...).

Como testar:
  python main.py        -> valida o arquivo acessos.xml usando todas as issues
  python test_issue2.py -> roda os testes automaticos da Issue 2

ISSUE 3 -- Validacao Estrutural do Bloco <registro>
Responsavel: Arthur Pessoa Lira
==========================================================

Arquivos da Issue 3:
  registro.py    -> validar_registro(n, texto): dict {"id_cracha", "status", "hora"}
  test_issue3.py -> testes automaticos

Estrategia: Expressao Regular compilada (AFD equivalente).
  O <registro> tem estrutura plana e fixa (Linguagem Regular -- Tipo 3 de Chomsky),
  podendo ser reconhecida por AFD. Pelo Teorema de Kleene, toda LR tem ER
  equivalente, o que justifica formalmente o uso de re.compile.

Testes da Issue 3:
  acessos.xml    -> XML valido (arquivo padrao do main)
  test_issue3.py -> testes automaticos

Como testar:
  python main.py                    -> Sucesso: Arquivo XML valido.
  python main.py testes/vazio.xml   -> Erro: Arquivo xml vazio
  python test_issue3.py             -> roda todos os testes automaticos