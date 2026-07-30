# Revisão de currículo — itens abertos

**Data:** 2026-07-30 (apenas o que está pendente; o trabalho concluído foi removido — o
diff está no histórico do git)
**Arquivos:** `resume-en_us.json`, `resume-pt_br.json` + artefatos gerados em `latest/`
**Alvo:** nenhuma vaga informada. O que é pontuado aqui vale contra **expectativas típicas
para um engenheiro de backend Senior/Staff em 2026**, não contra uma vaga.
**Original em inglês:** [`resume-review-2026-07-30.md`](resume-review-2026-07-30.md)

As frentes A, B e C estão **concluídas**: resumos enxugados (en 172→96 palavras, pt 217→113),
afirmações que expiram e editorialização removidas, paridade entre idiomas restaurada, URL do
LinkedIn extraível nos cinco formatos, cabeçalhos de seção do pt_BR localizados, `--cut-date`
não apaga mais os diplomas, e `mise run short` adicionado (3 páginas contra as 6 do mestre).

**Uma constatação da revisão original foi retirada por estar errada:** os "25 years" do
`meta.summaries.platform` não contradizem os "26 years" do `basics.summary` — medem a atuação
em build/release/GCS (desde `2001-10`, 24,8 anos) e o tempo de carreira (desde `2000-06`,
26,2 anos). Ambos corretos.

---

## Onde a pontuação realmente está

**Evidência de impacto continua em 9/25, sem alteração.** Nada nas frentes A–C mexeu nisso, e
era esperado — elas corrigiram redação, contradições e ferramental. Impacto mede resultados
quantificados, e o documento ainda tem exatamente um, de um cargo encerrado em **2005**
(`resume-en_us.json:115`, "…by approximately 20%").

Todo o trabalho recente ainda conta *artefatos construídos* — nove dashboards, cinco
repositórios, quatro apps, seis ferramentas — em vez de resultados. **Só P1–P4 mudam esse
número.** Todo o resto abaixo é secundário.

---

## Bloqueando — depende da sua resposta

### Métricas (maior alavancagem, em ordem)

| # | Pergunta | Onde entra |
|---|---|---|
| **P1** | A plataforma de onboarding substituiu um processo manual de nove etapas — quanto tempo levava o onboarding de uma pessoa **antes**, e quanto leva **agora**? | `:32` nos dois idiomas. Transforma sua entrega solo recente mais forte no único resultado recente quantificado. Responda esta primeiro. |
| **P2** | Ao longo daqueles nove anos de direção técnica de equipes Scrum: quantos engenheiros, em quantas equipes? | `:68` nos dois idiomas. Hoje é o bullet mais fraco do documento — nove anos de liderança descritos como uma lista de cerimônias. |
| **P3** | A plataforma de abrangência nacional: tráfego, usuários ou volume de requisições? | `:85` nos dois idiomas. "Nacional" é a maior palavra de escala do currículo e não carrega número nenhum. |
| **P4** | Cobertura de testes **antes → depois** nos cinco repositórios? | `:37` nos dois idiomas. Substituiria "milhares de testes", que soa como volume e não como resultado. |

### Fatos que eu não consigo inferir

| # | Pergunta | Por que importa |
|---|---|---|
| **P5** | Você já usou **Terraform**, ou outra ferramenta de IaC, em produção? | Ansible, Helm e Kustomize estão presentes; Terraform não aparece em lugar nenhum. Isso é uma lacuna do currículo (corrigível agora) ou uma lacuna de candidatura (que não se disfarça), e eu não tenho como saber qual. |
| **P6** | Você foi responsável por **observabilidade** — OpenTelemetry, Sentry? | Estão apenas em `skills.keywords` (en `:260`, pt `:250`) e nunca aparecem em um highlight. Parsers de ATS leem a prosa do documento, não o seu esquema de etiquetas, então como está hoje eles são efetivamente ausentes. Se foi você, merece um bullet; se era ambiente, provavelmente deveria sair das palavras-chave. |
| **P7** | Quem você **mentorou** desde 2009, e quantas pessoas aproximadamente? | `Mentoring` / `Mentoria` é palavra-chave (en `:270`, pt `:260`), mas o último bullet de liderança do documento é do cargo de 2005–2009. |

### Decisões

| # | Decisão | Observações |
|---|---|---|
| **P8** | Títulos de cargo duplicados em entradas adjacentes: **fundir** cada par em uma entrada só, ou **diferenciar** os títulos por escopo? | Três dos quatro pares adjacentes têm `position` idêntico — entradas 1&2 "Senior Backend Software Engineer", 3&4 "Senior Full-Stack Software Engineer", 7&8 "Junior Software Engineer". Quem bate o olho e lê o mesmo título duas vezes seguidas entende *enchimento*, quando a história real é 26 anos de progressão. Diferenciar exige fatos que eu não tenho. **Esta é a alavanca real de páginas.** |
| **P9** | Tempo verbal do cargo atual: manter a convenção da casa (passado) ou usar presente no cargo em andamento? | `work[0]` corretamente não tem `endDate`, mas os highlights em en_US dizem "Built solo", "Shipped", "Delivered". O `SKILL.md` documenta o passado como convenção; um gestor lê o presente como "ainda faz isso". É um trade-off real, não um bug. |
| **P10** | `https://shorturl.at/p0ZhO` no resumo da formação (`:157` nos dois idiomas): qual a URL canônica da dissertação, remover o parêntese, ou deixar como está? | Encurtadores passam sensação de link quebrado e alguns parsers os descartam. Posso resolver o redirecionamento e achar a URL real, se preferir. |
| **P11** | `awards[0].links` — **veja o aviso abaixo.** Ensinar os renderers, dobrar no `summary`, ou remover? | Quebra de paridade ativa, e dado morto. |
| **P12** | Grade de competências em duas colunas: aceitar e enviar `txt`/`docx` para portais rigorosos, ou tornar o layout de impressão de coluna única? | No `pdftotext` puro (como a maioria dos parsers de ATS lê um PDF) as colunas se intercalam, os níveis "Expert"/"Advanced" se desprendem das categorias e invertem, e `Multi-arch builds` se quebra em `Multi-` / `arch builds`. **Sugestão: aceitar e documentar** — a rubrica recomenda não redesenhar o tema, e `txt`/`docx` já são de coluna única e seguros para ATS. |
| **P13** | `basics.label` é "Engenheiro de Software Sênior" (`:5` nos dois idiomas) — mudar o título? | O escopo descrito é Staff+: equipe de 10 engenheiros, padrões corporativos, uma avaliação CMMI Nível 3 como avaliador SCAMPI treinado, quatro plataformas construídas sozinho. Você subestima o próprio escopo. A decisão é sua; não vou inventar um título que você não tem. |
| **P14** | Três das quatro publicações continuam **sem URL verificável**. Você tem os PDFs, ou uma página pessoal/institucional que você controle? | O KSACI já está ligado ao capítulo dele na Springer. Os outros três são artigos de 2001–2008 de eventos pequenos (um workshop da SBC, um workshop satélite do AAMAS, um grupo de interesse da BCS) que parecem nunca ter recebido DOI. O KEOPS só é localizável como citação dentro da bibliografia de terceiros; os artigos do WJOGOS e da BCS-CMSG retornam zero resultados em todos os índices acessíveis. Uma página sua é um link mais durável do que um registro de editora que não existe. |
| **P15** | O `releaseDate` do KSACI é `2001`, mas a Springer publica o volume como **2002** (o ATAL foi em agosto de 2001; o *Intelligent Agents VIII* saiu em 21 de junho de 2002). Manter o ano da conferência ou usar o ano de publicação? | As duas convenções de citação se defendem. Deixei em `2001`; se preferir, eu troco. |
| **P16** | A Springer lista o terceiro autor como **"Gustavo E. de Paula"**; seus dados traziam "G. Eliano de Paula". | Só importa se você quiser os nomes dos coautores de volta nos resumos (foram removidos — veja a nota da §7). Registrando para o dado não se perder. |

---

## ⚠ Problema novo, surgido depois da revisão

**`awards[0].links` é dado morto e quebra a paridade entre idiomas.**

Dois objetos de link foram adicionados ao `resume-en_us.json` (vídeo de gameplay do Sea
Hunter, download do JAR). Verificado: o campo renderiza em **zero dos cinco formatos**.

```
$ grep -ciE 'youtube|phoneky|gameplay' resume.md resume.txt resume.html   → 0 0 0
$ pdftotext resume.pdf - | grep -ciE 'youtube|phoneky|gameplay'           → 0
$ unzip -p resume.docx word/document.xml | grep -ciE 'youtube|phoneky'    → 0
```

Todos os renderers leem apenas `title` / `date` / `awarder` / `summary` / `url` de um prêmio,
e campos desconhecidos são ignorados silenciosamente. Mais dois problemas:

- **O pt_BR não tem o campo** — uma edição só em en_US é uma edição inacabada.
- **A validação de schema pode rejeitar** quando a validação via rede rodar de fato (ela foi
  pulada offline nos meus builds), dependendo de o schema do JSON Resume permitir
  propriedades extras em um prêmio.

Três saídas (**P11**): ensinar os renderers a emitir `links` — mexe nos quatro renderers
Python mais o tema, o mesmo trabalho de cinco caminhos da correção do LinkedIn; dobrar as duas
URLs no `summary` do prêmio, onde elas de fato aparecem; ou remover o campo. Vale notar que
`awards[0].url` já aponta para o release da Optus e esse sim renderiza.

---

## Conhecido, não corrigido, não bloqueia

| Item | Situação |
|---|---|
| **O mestre continua com 6 páginas**, nos dois idiomas | Enxugar o resumo liberou ~⅓ de página; a divisão de bullet e o bullet mais longo (e melhor) de `work[2]` consumiram esse espaço de volta. Resolvido para submissões pelo `mise run short` (**3 páginas**, diplomas preservados). Encolher o *mestre* depende de **P8**. |
| **Competências caem na página 4 de 6** no PDF do mestre | Consequência da contagem de páginas. Na variante enxuta elas ficam na página 1. |
| **A ordem das seções difere entre formatos** | `md`/`txt`: Work → Education → Skills → Awards → Certifications → Publications → Languages. `pdf`/`html`: Experience → Skills → Education → Publications → Awards → Languages → Certificates. Nenhuma está errada, mas "o que o recrutador vê primeiro" precisa ser ajustado duas vezes. Unificar é uma mudança pequena, se você quiser. |

---

## Ordem recomendada

1. **P1** — uma resposta, o maior movimento isolado na pontuação.
2. **P2–P4** — o resto das métricas. Juntas, são a única coisa que tira o impacto de 9/25.
3. **P11** — pequeno, e é uma quebra de paridade ativa mais uma possível falha de validação.
4. **P5–P7** — definir, para cada um, se é lacuna do currículo ou de candidatura.
5. **P8** — estrutural; medir a contagem de páginas uma única vez, depois dele.
6. **P9, P10, P12, P13** — polimento e decisões de julgamento.
