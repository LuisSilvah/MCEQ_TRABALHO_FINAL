# Protocolo do Projeto Final (1 página)

| Campo | Conteúdo |
|---|---|
| EQUIPE / MEMBROS | Hugo Silva Pinheiro (24012527), Leticia Akemi Sumida (24008474), Luis Gustavo Oliveira da Silva (24011554) |
| **Campos herdados da Ficha de Hipótese (Semana 4), atualizados** | |
| PROBLEMA (lacuna) | Estudos qualitativos sugerem que PRs "emaranhadas" (refatoração + funcionalidade) prejudicam a revisão de código, mas a evidência quantitativa controlada é escassa e vem de um único experimento com amostra pequena. |
| PERGUNTA DE PESQUISA | Em revisões de código com pull requests (contexto), apresentar a mesma mudança decomposta em duas PRs (intervenção) altera o número de falsos positivos por revisor (métrica) em comparação com a mudança emaranhada em uma única PR (comparação)? |
| H0 | μA = μB (μ = número médio de falsos positivos por revisor) |
| H1 | [ ] unilateral  [X] bilateral: μA ≠ μB |
| VI (fator) e níveis | Forma de apresentação da mudança: A = emaranhada (1 PR); B = decomposta (2 PRs) |
| VD e unidade | Falsos positivos por revisor (contagem de comentários que apontam problema inexistente) |
| CONTROLE / MODERADORA | Controle: mesma mudança, 3 defeitos injetados, mesma VM, fase de treino, alocação aleatória estratificada por experiência e conhecimento do sistema. Moderadora: não analisada (dados por participante indisponíveis). |
| O QUE MUDOU EM RELAÇÃO À FICHA | (1) VD: de "defeitos encontrados" para "falsos positivos", porque os defeitos por revisor não são identificáveis nos dados publicados (2 distribuições compatíveis em A e 3 em B), enquanto os falsos positivos têm reconstrução única. Defeitos viram hipótese secundária, testada em todas as combinações compatíveis. (2) H1: de unilateral para bilateral, alinhada ao teste do artigo original. Declaração: o resultado original para falsos positivos já era conhecido pela equipe; a análise é uma reprodução crítica. |
| **Campos novos** | |
| BASE ESCOLHIDA | di Biase et al. (2019), PeerJ Comput. Sci. 5:e193, DOI 10.7717/peerj-cs.193; dados agregados da Tabela 2 (RQ1) e contagens da Figura 2 (RQ3); Tabela 3 (RQ2) transcrita só como registro; acesso 01/11/2026; licença CC BY 4.0. Pacote complementar: 4TU.ResearchData, DOI 10.4121/uuid:826f7051-35f6-4696-b648-8e56d3ea5931, versão 1, que não respondeu em 01/11/2026; por isso a equipe usou as informações publicadas no artigo. (Baixado depois, em 10/11/2026: sem dados por revisor; licença do registro CC BY-SA 4.0 e do README CC BY 4.0, inconsistência anotada no README.) |
| JUSTIFICATIVA DA BASE | Proveniência: artigo revisado por pares com DOI. Documentação: variáveis definidas no artigo (seção Outcome measurements). Licença: CC BY 4.0. Tamanho: 14 por grupo (6 desenvolvedores, 3 doutorandos e 5 mestrandos em cada; pequeno, declarado como limitação). Variáveis: VI e VD presentes. Medição: classificação manual dos comentários pelo primeiro autor, com os 3 defeitos injetados como referência; só experimentos-piloto do ambiente, sem medida de concordância entre avaliadores. |
| TIPO DE ESTUDO | [X] experimento publicado  [ ] observacional |
| DESENHO | [X] 2 grupos independentes  [ ] pareado  [ ] blocos  [ ] k tratamentos |
| UNIDADE DE ANÁLISE e n | Revisor; nA = nB = 14 |
| TESTE PREVISTO, α e estatística | Mann-Whitney U bilateral, α = 0,05, estatística U (mesmo teste do artigo original). Welch não usado: VD de contagem com poucos valores, sem normalidade aproximada das médias com n = 14 |
| TESTE ALTERNATIVO | Se a VD tiver poucos valores distintos e muitos empates: teste exato de permutação de U (com VD binária, equivale ao teste exato de Fisher), usado para a decisão |
| TAMANHO DE EFEITO E IC | δ de Cliff como principal, A de Vargha-Delaney (A = (δ + 1)/2, efeito associado ao Mann-Whitney; complemento acrescentado em 10/11/2026, antes de qualquer nova análise) e d de Cohen como complementar (Kampenes et al., 2007); δ de Cliff (limiares de Romano et al., 2006); IC 95% de Newcombe para diferença de proporções quando a VD for binária; IC de Wilson por grupo na figura |
| AMEAÇAS À VALIDADE INICIAIS | Conclusão: n pequeno, baixo poder, dependência da escolha aproximação × exato. Interna: execução assíncrona; reconstrução a partir de dados agregados. Construção: classificação dos comentários por um só pesquisador, sem concordância entre avaliadores; transcrição visual da Figura 2. Externa: um sistema Java pequeno, uma mudança de ~100 linhas, amostra por conveniência. |
| DECISÕES DE LIMPEZA | Transcrição das Tabelas 2 e 3 e da Figura 2 para `dados/brutos/` (CSV), conferida por dois membros, sem edição posterior; reconstrução por revisor no script com tolerância de 0,01; `assert` de média, DP, limite do "IC", δ de Cliff e p-valor publicados; coluna "IC 95%" da Tabela 2 não usada como intervalo de confiança (IC calculado no script); defeitos testados em todas as combinações compatíveis; nenhuma exclusão de participantes. |
| ANÁLISES EXPLORATÓRIAS | Questionário Likert Q1 a Q12 (Figura 2), Mann-Whitney com ajuste de Holm (12 testes), rotuladas como exploratórias. |
