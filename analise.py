from itertools import product
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker
import numpy as np
import pandas as pd
from scipy import stats

SEMENTE = 2026
ALFA = 0.05
N_GRUPO = 14

RAIZ = Path(__file__).resolve().parent
BRUTOS = RAIZ / "dados" / "brutos"
LIMPOS = RAIZ / "dados" / "limpos"
FIGURAS = RAIZ / "figuras"
LIMPOS.mkdir(parents=True, exist_ok=True)
FIGURAS.mkdir(parents=True, exist_ok=True)

saida = []


def relatar(texto=""):
    print(texto)
    saida.append(texto)


# 1. Reconstrução dos valores por participante a partir da Tabela 2 do artigo
VALOR_MAX = {"defeitos_encontrados": 3, "falsos_positivos": 6}  # 3 defeitos injetados


def distribuicoes_compativeis(linha, valor_max, tol_dp=0.01):
    candidatas = []
    n = int(linha["n"])
    total = int(linha["total"])

    def gerar(restante, k):
        if k == valor_max:
            yield (restante,)
            return
        for c in range(restante + 1):
            for resto in gerar(restante - c, k + 1):
                yield (c,) + resto

    for cont in gerar(n, 0):
        valores = np.repeat(np.arange(valor_max + 1), cont)
        if valores.sum() != total:
            continue
        if np.median(valores) != linha.mediana:
            continue
        if np.floor(valores.mean() * 100) / 100 != round(linha.media, 2):
            continue
        if abs(valores.std(ddof=0) - linha.dp) > tol_dp:
            continue
        candidatas.append(valores)
    return candidatas


tab2 = pd.read_csv(BRUTOS / "tabela2_rq1_resumo.csv")
reconstrucoes = {}
relatar("=== 1. Reconstrução a partir da Tabela 2 (di Biase et al., 2019) ===")
for (var, grupo), linha in tab2.set_index(["variavel", "grupo"]).iterrows():
    if var not in VALOR_MAX:
        continue
    cands = distribuicoes_compativeis(linha, VALOR_MAX[var])
    reconstrucoes[(var, grupo)] = cands
    relatar(f"{var:22s} {grupo:13s} distribuições compatíveis: {len(cands)}")
    for c in cands:
        relatar(f"    contagens por valor 0..: {np.bincount(c).tolist()}")

# 2. Funções de análise
def delta_cliff(a, b):
    """d = [#(a > b) - #(a < b)] / (n_a n_b). Positivo: valores maiores em A."""
    dif = np.subtract.outer(a, b)
    return (np.sum(dif > 0) - np.sum(dif < 0)) / (len(a) * len(b))


def ic_wilson(k, n, z=1.959964):
    p = k / n
    centro = (p + z**2 / (2 * n)) / (1 + z**2 / n)
    meia = z * np.sqrt(p * (1 - p) / n + z**2 / (4 * n**2)) / (1 + z**2 / n)
    return centro - meia, centro + meia


def ic_newcombe(k1, n1, k2, n2):
    """IC 95% de Newcombe (método 10, escores de Wilson) para p1 - p2."""
    p1, p2 = k1 / n1, k2 / n2
    l1, u1 = ic_wilson(k1, n1)
    l2, u2 = ic_wilson(k2, n2)
    d = p1 - p2
    return d - np.sqrt((p1 - l1) ** 2 + (u2 - p2) ** 2), d + np.sqrt((u1 - p1) ** 2 + (p2 - l2) ** 2)


def holm(p):
    """p-valores ajustados por Holm-Bonferroni (controle do erro familiar)."""
    ordem = np.argsort(p)
    ajust = np.maximum.accumulate((len(p) - np.arange(len(p))) * p[ordem])
    saida_p = np.empty_like(p)
    saida_p[ordem] = np.minimum(1, ajust)
    return saida_p


def descritiva(a, b, nome):
    df = pd.DataFrame({"A_emaranhada": pd.Series(a), "B_decomposta": pd.Series(b)})
    d = df.agg(["count", "sum", "mean", "std", "median", "min", "max"]).T.round(3)
    relatar(f"\nDescritiva: {nome}")
    relatar(d.to_string())
    return d


# 3. Hipótese principal (confirmatória): falsos positivos
#    H0: a distribuição de FP é igual em A e B; H1 (bilateral): difere. alfa = 0,05
relatar("\n=== 2. Hipótese principal: falsos positivos por revisor ===")
fp_a = reconstrucoes[("falsos_positivos", "A_emaranhada")]
fp_b = reconstrucoes[("falsos_positivos", "B_decomposta")]
assert len(fp_a) == 1 and len(fp_b) == 1, "reconstrução de FP deveria ser única"
fp_a, fp_b = fp_a[0], fp_b[0]

pd.DataFrame({
    "participante": [f"A{i+1:02d}" for i in range(N_GRUPO)] + [f"B{i+1:02d}" for i in range(N_GRUPO)],
    "grupo": ["A_emaranhada"] * N_GRUPO + ["B_decomposta"] * N_GRUPO,
    "falsos_positivos": np.concatenate([fp_a, fp_b]),
}).to_csv(LIMPOS / "falsos_positivos_por_revisor.csv", index=False)

descritiva(fp_a, fp_b, "falsos positivos (contagem por revisor)")

valores_distintos = np.unique(np.concatenate([fp_a, fp_b]))
relatar(f"Valores distintos observados: {valores_distintos.tolist()} -> empates maciços; "
        "pelo protocolo, a decisão usa o teste exato (alternativo)")
assert set(valores_distintos) <= {0, 1}

# Teste previsto no artigo original (reprodução): aproximação normal com correção de empates
mw = stats.mannwhitneyu(fp_a, fp_b, alternative="two-sided", method="asymptotic")
# Teste alternativo do protocolo: com VD binária, a permutação exata de U equivale ao teste
# exato condicional de Fisher (U depende só de quantos "1" caem no grupo A).
k_a, k_b = int(fp_a.sum()), int(fp_b.sum())
fisher = stats.fisher_exact([[k_a, N_GRUPO - k_a], [k_b, N_GRUPO - k_b]])
# Conferência por Monte Carlo da permutação de U
perm = stats.permutation_test(
    (fp_a, fp_b),
    lambda x, y: stats.mannwhitneyu(x, y, alternative="two-sided", method="asymptotic").statistic,
    permutation_type="independent", alternative="two-sided",
    n_resamples=100_000, random_state=SEMENTE,
)
d_fp = delta_cliff(fp_a, fp_b)          # para VD binária, delta = p_A - p_B
ic_d = ic_newcombe(k_a, N_GRUPO, k_b, N_GRUPO)

# Conferência com os valores publicados na Tabela 2 (o artigo trunca em 2 casas).
# A coluna "IC 95%" da Tabela 2 é média ± 1,96 DP (limitada em 0), ou seja, um intervalo
# de valores individuais, não um intervalo de confiança da média; por isso o IC é calculado aqui.
truncar = lambda x: np.floor(x * 100) / 100
for v, g in ((fp_a, "A_emaranhada"), (fp_b, "B_decomposta")):
    pub = tab2.set_index(["variavel", "grupo"]).loc[("falsos_positivos", g)]
    assert truncar(v.mean()) == round(pub.media, 2), f"média de {g} não reproduz a Tabela 2"
    assert abs(v.std(ddof=0) - pub.dp) <= 0.01, f"DP de {g} não reproduz a Tabela 2"
    assert abs(v.mean() + 1.959964 * v.std(ddof=0) - pub.ic95_sup) <= 0.01, \
        f"limite superior do 'IC' de {g} não reproduz a Tabela 2"
assert round(d_fp, 2) == 0.36, "delta de Cliff não reproduz o artigo (0,36)"
assert truncar(mw.pvalue) == tab2.query("variavel == 'falsos_positivos'").p_valor_original.iloc[0], \
    "p-valor de Mann-Whitney não reproduz a Tabela 2"
relatar("Conferência com a Tabela 2: média, DP, limite do 'IC', delta de Cliff e p-valor reproduzidos")

relatar(f"\nMann-Whitney U (bilateral, aprox. normal c/ correção de empates): U = {mw.statistic:.1f}, p = {mw.pvalue:.4f}")
relatar(f"Teste exato (Fisher = permutação exata de U): OR = {fisher.statistic:.2f}, p = {fisher.pvalue:.4f}")
relatar(f"Conferência: permutação Monte Carlo de U (100000 reamostragens, semente {SEMENTE}): p = {perm.pvalue:.4f}")
relatar(f"Delta de Cliff (A vs. B) = {d_fp:.3f} (= diferença de proporções); "
        f"IC95% Newcombe = [{ic_d[0]:.3f}; {ic_d[1]:.3f}]")
# A de Vargha-Delaney (efeito do Mann-Whitney na Semana 11): A = U_A / (n_A n_B) = (delta + 1) / 2
A_vd = mw.statistic / (N_GRUPO * N_GRUPO)
assert abs(A_vd - (d_fp + 1) / 2) < 1e-12
relatar(f"A de Vargha-Delaney (A vs. B) = {A_vd:.3f} (probabilidade de um revisor de A ter mais FP que um de B, empate vale 1/2)")
sp = np.sqrt(((N_GRUPO - 1) * fp_a.var(ddof=1) + (N_GRUPO - 1) * fp_b.var(ddof=1)) / (2 * N_GRUPO - 2))
d_cohen = (fp_a.mean() - fp_b.mean()) / sp
relatar(f"d de Cohen (A - B) = {d_cohen:.3f} (sp = {sp:.3f})")
decisao = "rejeita H0" if fisher.pvalue < ALFA else "não rejeita H0"
relatar(f"Decisão com alfa = {ALFA} (teste exato): {decisao}")

# Figura 1: proporção de revisores com pelo menos um falso positivo, IC de Wilson
props, erros = [], []
for v in (fp_a, fp_b):
    k = int((v > 0).sum())
    p = k / len(v)
    lo, hi = ic_wilson(k, len(v))
    props.append(p)
    erros.append((p - lo, hi - p))
    relatar(f"Proporção com >=1 FP: {k}/{len(v)} = {p:.3f}; IC95% Wilson = [{lo:.3f}; {hi:.3f}]")

fig, ax = plt.subplots(figsize=(3.4, 2.4), dpi=300)
ax.bar(["A: emaranhada\n(1 PR)", "B: decomposta\n(2 PRs)"], props,
       yerr=np.array(erros).T, capsize=6, color=["#b8475d", "#4a6fa5"], width=0.55)
for i, v in enumerate((fp_a, fp_b)):
    ax.text(i + 0.06, props[i] + 0.02, f"{int((v > 0).sum())}/14", ha="left", va="bottom", fontsize=7)
ax.set_ylim(0, 1)
ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda y, _: f"{y:.1f}".replace(".", ",")))
ax.set_ylabel("Revisores com ≥ 1 falso positivo\n(proporção, IC 95% Wilson)", fontsize=7)
ax.tick_params(labelsize=7)
ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout()
fig.savefig(FIGURAS / "fig1_falsos_positivos.png")

# Poder do teste exato (simulação), supondo as proporções observadas como verdadeiras.
# Serve para planejar a replicação (próximos passos), não para reinterpretar o p-valor.
rng = np.random.default_rng(SEMENTE)
p_a, p_b = k_a / N_GRUPO, k_b / N_GRUPO


def poder_fisher(n, reps=2000):
    xa = rng.binomial(n, p_a, reps)
    xb = rng.binomial(n, p_b, reps)
    return np.mean([stats.fisher_exact([[a, n - a], [b, n - b]]).pvalue < ALFA for a, b in zip(xa, xb)])


relatar(f"Poder simulado do teste exato com n = {N_GRUPO} por grupo: {poder_fisher(N_GRUPO):.2f}")
n_80 = next(n for n in range(N_GRUPO, 101) if poder_fisher(n) >= 0.80)
relatar(f"Menor n por grupo com poder >= 0,80 (passo 1): {n_80}")

# 4. Hipótese secundária (confirmatória, análise de sensibilidade): defeitos
#    A Tabela 2 admite mais de uma distribuição; testa-se cada combinação.
relatar("\n=== 3. Hipótese secundária: defeitos encontrados (todas as reconstruções compatíveis) ===")
linhas = []
for va, vb in product(reconstrucoes[("defeitos_encontrados", "A_emaranhada")],
                      reconstrucoes[("defeitos_encontrados", "B_decomposta")]):
    r = stats.mannwhitneyu(va, vb, alternative="two-sided", method="asymptotic")
    linhas.append({"A_contagens_0a3": np.bincount(va, minlength=4).tolist(),
                   "B_contagens_0a3": np.bincount(vb, minlength=4).tolist(),
                   "U": r.statistic, "p": round(r.pvalue, 4), "delta_cliff": round(delta_cliff(va, vb), 3)})
sens = pd.DataFrame(linhas)
sens.to_csv(LIMPOS / "defeitos_sensibilidade.csv", index=False)
relatar(sens.to_string(index=False))
relatar(f"Faixa de p: [{sens.p.min():.3f}; {sens.p.max():.3f}]; faixa de delta: [{sens.delta_cliff.min():.3f}; {sens.delta_cliff.max():.3f}]")

# 5. Análises exploratórias: questionário Likert (Figura 2 do artigo), 12 testes
relatar("\n=== 4. Exploratório: questionário pós-revisão Q1-Q12 (Likert 1-5) ===")
lik = pd.read_csv(BRUTOS / "figura2_rq3_likert.csv")
colunas = [c for c in lik.columns if c[-1].isdigit()]
assert (lik[colunas].sum(axis=1) == N_GRUPO).all(), "cada linha da Figura 2 deve somar 14"
longo = []
res = []
for q, g in lik.groupby("questao", sort=False):
    vals = {}
    for _, linha in g.iterrows():
        v = np.repeat(np.arange(1, 6), linha[colunas].to_numpy(dtype=int))
        vals[linha.grupo] = v
        longo += [{"questao": q, "grupo": linha.grupo, "resposta": x} for x in v]
    a, b = vals["A_emaranhada"], vals["B_decomposta"]
    r = stats.mannwhitneyu(a, b, alternative="two-sided", method="asymptotic")
    res.append({"questao": q, "mediana_A": np.median(a), "mediana_B": np.median(b),
                "U": r.statistic, "p": r.pvalue, "delta_cliff_A_vs_B": round(delta_cliff(a, b), 3)})
pd.DataFrame(longo).to_csv(LIMPOS / "likert_por_resposta.csv", index=False)
res = pd.DataFrame(res)
res["p_holm"] = holm(res.p.to_numpy())
res["p"] = res.p.round(4)
res["p_holm"] = res.p_holm.round(4)
res.to_csv(LIMPOS / "likert_testes.csv", index=False)
relatar(res.to_string(index=False))

(RAIZ / "resultados.txt").write_text("\n".join(saida) + "\n", encoding="utf-8")
