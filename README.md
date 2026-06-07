# INF1026 - COMPUTACAO APLICADA

-- Gerar Arquivo Excel com os dados
Fontes:


0🔧 Requisitos Técnicos Mínimos (Python/Pandas)
Preparação dos dados

 1 concatenação (em qualquer eixo)
 2 estratégias distintas de preenchimento de valores ausentes (pelo menos uma por grupo), ex:

Substituir pelo valor mais frequente (coluna textual)
Substituir pela média do grupo (coluna numérica)


 1 estratégia de substituição/alteração de valores (df[col].apply(...))

Categorização

 Criar pelo menos 2 categorias em função do valor de uma coluna (pd.cut)
 Usar pd.cut com bins = quantidade de categorias → nova coluna
 Usar pd.cut com bins = lista com os extremos de cada faixa → nova coluna

Filtros (mínimo 4)

 1 filtro de valor
 1 filtro de índice
 1 filtro composto
 1 filtro por grupo

Tabelas de Frequência (mínimo 2)

 1 tabela com valores absolutos sobre uma variável
 1 tabela com valores percentuais sobre outra variável

Gráficos (mínimo 2)

 2 gráficos de tipos distintos, apropriados para as variáveis analisadas

Medidas de Sumarização

 Gerais: total, máximo, mínimo, medida de linha ou coluna
 Grupos simples: groupby com um único agrupador + medidas de interesse
 Grupos estruturados: groupby com mais de um agrupador + medidas de interesse

Cruzamentos (mínimo 4)

 Cruzamento simples (1 × 1): crosstab com índice simples e coluna simples

 com contagem no cruzamento
 com medida de outra variável no cruzamento


 Cruzamento estruturado (n × m): crosstab com índice e/ou coluna com mais de 1 Series

 com contagem no cruzamento
 com medida de outra variável no cruzamento




🚫 Proibições

 Não usar provas ou trabalhos de períodos anteriores de qualquer disciplina de manipulação de dados



Resumo crítico: grupo formado → base de dados escolhida → trabalho.docx com perguntas mapeadas aos requisitos → templateTrabalho.py → gabaritoTrabalho.py → Excel com dados → tudo entregue até 09/06 às 23h.
Você disse: qual a diferença entre Cruzamentos e Agrupamentoqual a diferença entre Cruzamentos e Agrupamento31 de mai.Claude respondeu: Agrupamento vs.Agrupamento vs. Cruzamento
São conceitos diferentes, mas complementares:

🔵 Agrupamento (groupby)
Você agrupa linhas por uma ou mais colunas e calcula uma medida (soma, média, contagem...).
O resultado é uma série ou tabela simples.
pythondf.groupby("região")["salário"].mean()
regiãosalário_médioSul4500Sudeste5200Nordeste3800
→ Para cada região, uma linha, um valor.

🟠 Cruzamento (crosstab)
Você cruza duas (ou mais) variáveis em formato de tabela bidimensional — linhas vs. colunas. É uma tabela de dupla entrada.
pythonpd.crosstab(df["região"], df["escolaridade"])
regiãoFundamentalMédioSuperiorSul104530Sudeste206055Nordeste354015
→ Você vê a combinação de duas variáveis ao mesmo tempo.

🧠 Resumo prático
AgrupamentoCruzamentoFunçãogroupbycrosstabDimensão1D (uma coluna de resultado)2D (linhas × colunas)Pergunta típica"Qual a média de salário por região?""Como se distribuem escolaridade e região juntas?"ResultadoLista de grupos + medidaTabela cruzada

Analogia: o agrupamento é como uma lista resumida; o cruzamento é como uma planilha de dupla entrada — você enxerga a relação entre duas variáveis de uma vez só.