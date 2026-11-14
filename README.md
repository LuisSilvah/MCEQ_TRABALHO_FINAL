# Decomposição de pull requests e falsos positivos na revisão de código

Projeto Final de MCEQ 12576 (Métodos de Computação Experimental e Quantitativa), PUC-Campinas, 2º semestre de 2026.

Equipe: Hugo Silva Pinheiro (24012527), Leticia Akemi Sumida (24008474), Luis Gustavo Oliveira da Silva (24011554).

## Pergunta de pesquisa

Em revisões de código com pull requests, apresentar a mesma mudança decomposta em duas PRs (B) altera o número de falsos positivos por revisor, em comparação com a mudança emaranhada em uma única PR (A)?

- H0: μA = μB
- H1 (bilateral): μA ≠ μB
- α = 0,05

## Origem dos dados

| Item | Valor |
|---|---|
| Artigo | di Biase, Bruntink, van Deursen, Bacchelli (2019). The effects of change decomposition on code review: a controlled experiment. PeerJ Computer Science 5:e193 |
| DOI | https://doi.org/10.7717/peerj-cs.193 (https://peerj.com/articles/cs-193/) |
| Licença | CC BY 4.0 (uso acadêmico e redistribuição com atribuição) |
| Dados usados | Tabela 2 (RQ1) e contagens da Figura 2 (RQ3); Tabela 3 (RQ2) transcrita só como registro |
| Data de acesso | 01/11/2026 |
| Pacote complementar | 4TU.ResearchData, DOI 10.4121/uuid:826f7051-35f6-4696-b648-8e56d3ea5931, versão 1. Não respondeu em 01/11/2026; por isso a análise usa as informações publicadas no artigo (detalhes na Ficha de Proveniência) |

Arquivos em `dados/brutos/` (transcritos do artigo, sem nenhuma edição posterior):

- `tabela2_rq1_resumo.csv`: Tabela 2 do artigo (n, total, mediana, média, DP, coluna "IC 95%" e p-valor por grupo).
- `tabela3_rq2_tempos.csv`: Tabela 3 do artigo (tempo líquido de revisão e tempo de vida do 1º e do 2º defeito, em segundos). Fica fora da hipótese principal.
- `figura2_rq3_likert.csv`: contagem de respostas por nível Likert (1 a 5), por questão e grupo, lida da Figura 2. Cada linha soma 14 (verificado pelo script).

A pasta `data/` traz o pacote complementar dos autores, baixado em 10/11/2026, **sem a máquina virtual** (6,1 GB, não incluída no repositório): README, `Instructions_for_the_experiment.pdf`, `source_code_with_patches/` (jpacman e patches das PRs, licença Apache 2.0) e `Other_suggested_improvements_in_reviews.xlsx`. Esse pacote não tem resultados por revisor e não é usado pelo script.

## Ficha de Proveniência e Medição (Marco 2)

Base: dados publicados em di Biase et al. (2019), um experimento controlado sobre decomposição de pull requests (dados secundários: coletados por outras pessoas, para a pergunta delas). O documento entregue está em `docs/marco2/MCEQ_ProjetoFinal_Marco2.pdf`.

| Campo | Resposta da equipe |
|---|---|
| **Origem, versão/DOI, data de acesso, licença** | A base foi obtida do artigo de di Biase et al. (2019), *The effects of change decomposition on code review: a controlled experiment*, PeerJ Computer Science, volume 5, artigo e193. DOI: https://doi.org/10.7717/peerj-cs.193. Foram utilizados os dados agregados da Tabela 2 (RQ1) e as contagens da Figura 2 (RQ3). Acesso em 01/11/2026. Licença: CC BY 4.0. O pacote de dados associado, hospedado no 4TU.ResearchData (DOI 10.4121/uuid:826f7051-35f6-4696-b648-8e56d3ea5931), não respondeu às tentativas de acesso realizadas em 01/11/2026; por isso, a equipe utilizou as informações publicadas no artigo. Registro posterior: em 10/11/2026 o pacote foi baixado e inspecionado; ele não tem tabela de resultados por revisor (só a planilha de 26 sugestões de melhoria, 7 em A e 19 em B, sem identificador de participante, que confirma essa linha da Tabela 2) e a licença é inconsistente (CC BY-SA 4.0 no registro, CC BY 4.0 no README do pacote). |
| **Como a VD foi medida** (instrumento, escala, período) | Falso positivo = comentário na PR (discussão ou em linha) que não aponta um problema real. **Instrumento:** classificação manual feita pelo primeiro autor a partir do texto do comentário, tendo como referência os 3 defeitos funcionais injetados de propósito. **Escala:** contagem de comentários por revisor. **Período:** não informado; a coleta terminou antes de 03/05/2018, data de publicação do apêndice. Revisão assíncrona, sem limite de tempo, em máquina virtual com gravação de tela, sobre o JPacman (Java, cerca de 3.000 linhas; mudança de cerca de 100 linhas em 7 arquivos). |
| **Como a VI foi definida** (quem formou os grupos) | VI = forma de apresentação da mudança para revisão. Grupo A: uma única pull request, com as mudanças agrupadas. Grupo B: duas pull requests, separando a refatoração da implementação da nova funcionalidade. 28 participantes, 14 em cada grupo (6 desenvolvedores, 3 doutorandos e 5 mestrandos em cada). Segundo o artigo, a alocação foi aleatória e estratificada pela experiência dos participantes e pelo conhecimento prévio do JPacman. Os grupos revisaram a mesma mudança, com cerca de 100 linhas em 7 arquivos e 3 defeitos funcionais inseridos. |
| **Há estudo de validação da medida?** | O artigo relata experimentos-piloto para verificar o ambiente e os procedimentos. Não foi identificada validação independente da classificação dos comentários nem medida de concordância entre avaliadores; a classificação foi feita pelo primeiro autor. Na reanálise, a equipe verificou que cada linha de contagens transcrita da Figura 2 totaliza 14 respostas e que a reconstrução dos falsos positivos a partir da Tabela 2 é única. |
| **Fonte provável de erro sistemático** | A classificação manual dos comentários por um único pesquisador pode introduzir subjetividade na identificação de defeitos, falsos positivos e sugestões. Além disso, a equipe trabalhou com dados agregados publicados no artigo, e não com os registros individuais originais, o que limita a conferência participante a participante. A transcrição visual das contagens da Figura 2 também pode gerar erros de leitura. |
| **Dados ausentes ou duplicados? Quantos?** | Não há valores por participante, só agregados. Os falsos positivos têm reconstrução única (A: 8 revisores com 0 e 6 com 1; B: 13 com 0 e 1 com 1); os defeitos não (2 soluções em A e 3 em B, ver `resultados.txt`). Nenhum participante ausente na Tabela 2 (14 + 14). Na Tabela 3, os tempos de vida dos defeitos só existem para quem achou cada defeito (11 por grupo no 1º e 6 por grupo no 2º), e o 3º defeito foi excluído pelos autores (achado por 1 participante). Duplicados: não aplicável, pois os dados são agregados. |
| **Decisões de limpeza previstas no protocolo** | Ver o diário de limpeza abaixo. Nenhuma exclusão de participantes; tempos e questionários ficam fora da hipótese principal. |

### Desenho identificado

| Pergunta | Resposta da equipe |
|---|---|
| Quantos níveis tem a VI? | 2: A = mudança emaranhada (1 PR) e B = mudança decomposta (2 PRs) |
| Cada unidade recebeu os dois? | Não. Cada revisor recebeu um só tratamento, por sorteio estratificado |
| Desenho | 2 grupos independentes. Linha do mapa de decisão: t de Welch ou Mann-Whitney |
| Tipo de estudo | Experimento publicado (alocação aleatória estratificada por experiência e conhecimento prévio); a linguagem causal fica restrita ao contexto original |
| Unidade de análise | Revisor (participante do experimento) |
| n por grupo | nA = nB = 14 (28 participantes) |
| VD e teste previsto | Falsos positivos por revisor. Mann-Whitney U bilateral, α = 0,05, com teste exato de permutação como alternativo (`PROTOCOLO.md`) |

### Diário de limpeza

| # | Decisão | Efeito |
|---|---|---|
| 1 | Transcrever as Tabelas 2 e 3 e as contagens da Figura 2 para `dados/brutos/` (CSV), com conferência por dois membros; o arquivo bruto nunca é editado | Todo valor derivado está em `dados/limpos/`, gerado por `analise.py` |
| 2 | Reconstruir os vetores por revisor no script, enumerando todas as contagens compatíveis com n, total, mediana, média e DP, com tolerância de 0,01 (o artigo trunca as casas decimais: 6/14 = 0,4286 publicado como 0,42) | Só entram distribuições que reproduzem a Tabela 2 |
| 3 | `assert` exigindo que o vetor de falsos positivos reproduza média, DP, limite do "IC", δ de Cliff (0,36) e p-valor (0,03) publicados; `assert` de 14 respostas por linha da Figura 2 e de solução única para falsos positivos | Falha interrompe o script |
| 4 | Não usar a coluna "IC 95%" da Tabela 2 como intervalo de confiança: ela é média ± 1,96 DP, limitada em 0 (intervalo de valores individuais). O IC é calculado no script | IC 95% de Newcombe para δ e de Wilson por grupo |
| 5 | Defeitos (hipótese secundária): rodar o teste em todas as combinações de soluções e relatar a faixa de resultados (análise de sensibilidade) | 6 combinações, p entre 0,27 e 0,74, sem efeito detectável |
| 6 | Teste exato (Fisher) para a decisão, por a VD ter só os valores 0 e 1; Mann-Whitney assintótico mantido para comparar com o artigo | p = 0,077 (exato) contra 0,035 (aproximado): a conclusão depende dessa escolha, relatada nos dois |
| 7 | Nenhuma exclusão de participantes; tempos (Tabela 3) e questionário ficam fora da hipótese principal. Questionário Likert analisado como exploratório, com ajuste de Holm (12 testes) | Só Q8 e Q12 permanecem significativas após o ajuste |

Declaração: o resultado original do artigo para falsos positivos já era conhecido pela equipe quando a VD foi trocada (de defeitos para falsos positivos, por ser a única com reconstrução única); a análise é uma reprodução crítica, não um teste independente. A troca e a mudança de H1 para bilateral estão registradas em `PROTOCOLO.md`.

## Como reexecutar

```bash
python -m venv .venv
source .venv/bin/activate        # no Windows: .venv\Scripts\activate
pip install -r requirements.txt
python analise.py
```

O script é determinístico (semente 2026) e gera:

- `dados/limpos/falsos_positivos_por_revisor.csv`: valores por revisor reconstruídos (solução única).
- `dados/limpos/defeitos_sensibilidade.csv`: testes nas 6 combinações compatíveis para defeitos.
- `dados/limpos/likert_por_resposta.csv` e `likert_testes.csv`: análise exploratória.
- `figuras/fig1_falsos_positivos.png`: Figura 1 do artigo.
- `resultados.txt`: todos os números citados no artigo.

## Passos da análise

1. Reconstrução: enumera todas as distribuições de contagens com n = 14 que reproduzem total, mediana, média e desvio-padrão da Tabela 2. Para falsos positivos a solução é única; para defeitos há 2 (grupo A) e 3 (grupo B).
2. Conferência: o vetor de falsos positivos reproduz média, DP, limite do "IC", δ de Cliff e p-valor publicados (`assert`).
3. Hipótese principal (confirmatória): Mann-Whitney U bilateral (teste original) e, como a VD só assume 0 e 1, teste exato (Fisher, equivalente à permutação exata de U) para a decisão. Tamanho de efeito: δ de Cliff com IC 95% de Newcombe e A de Vargha-Delaney (A = (δ + 1)/2). Poder simulado.
4. Hipótese secundária: defeitos encontrados em todas as reconstruções compatíveis.
5. Exploratório: 12 questões Likert, Mann-Whitney com ajuste de Holm.

## Resultado principal

Em A, 6 de 14 revisores relataram ao menos um falso positivo; em B, 1 de 14. Mann-Whitney assintótico p = 0,035 (reproduz o original), teste exato p = 0,077: H0 não rejeitada com α = 0,05. δ de Cliff = 0,36, IC 95% [0,03; 0,61]; A de Vargha-Delaney = 0,68.
