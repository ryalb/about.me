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

**Pontuação: 65 → 75/100.** Quatro componentes se moveram — dois por respostas suas, dois por trabalho de layout:

| Componente | Peso | Era | Agora | Por quê |
|---|---|---|---|---|
| Cobertura de hard skills / palavras-chave | 30 | 25 | **27** | O bloco de competências saiu da página 4 para a 1, então as palavras-chave estão onde a triagem de fato lê. Ainda não é nota cheia por causa da linearização em duas colunas, que foi aceita e documentada, não corrigida. |
| Evidência de impacto | 25 | 9 | **13** | A P4 trouxe o primeiro resultado *recente* quantificado — cobertura de 0% para ~80% em um repositório e de ~50% para ~80% em outros quatro. Antes disso, o único número do documento era de um cargo encerrado em 2005. |
| Aderência de senioridade e escopo | 20 | 15 | **16** | A P2 colocou o tamanho das equipes no papel (6 a 15 engenheiros em quatro projetos), então a afirmação de liderança agora tem escopo. |
| Aderência de domínio | 15 | 13 | 13 | sem alteração |
| Legibilidade em triagem | 10 | 3 | **6** | Abertura caiu de 172 palavras, cabeçalhos do pt_BR localizados, competências na página 1, uma única ordem de seções em todos os formatos. Freada por duas coisas: o mestre ainda tem 6 páginas, e refocar o resumo em três cargos o levou de volta a 105 palavras (en) / 130 (pt), acima das ~70 em que o leitor para. |

**As quatro perguntas de métrica estão encerradas, e 13/25 é o teto por agora.** O bullet de
cobertura é o único resultado recente quantificado; em todo o resto, o trabalho recente ainda
conta artefatos — nove dashboards, quatro apps, seis ferramentas. Os dois caminhos que restam
estão bloqueados pela realidade, não pela redação: o dado de tráfego da P3 não existe, e a
plataforma de onboarding ainda não foi medida em produção (veja abaixo). Revisitar quando for.

---

## Aberto — sua decisão, nada bloqueante

Todos os dezenove itens numerados (P1–P19) estão encerrados, e também as três decisões de
julgamento que vieram depois. Resta um item cosmético.

| # | Item | Observações |
|---|---|---|
| **O1** | **A contagem de páginas do pt_BR é instável na fronteira 6/7.** | Oscilou 6→7→6→7 em quatro edições de conteúdo hoje. A causa é conhecida (veja a nota de paginação abaixo), não é defeito. O `--zoom 82%` fixou em 6 no teste. O en_US está estável em 6. Aceitar a oscilação, ou fixar o zoom. |

---

## Resolvido: `awards[].links` é dado de referência intencional

**Decisão: manter, sem renderizar.** Os dois links do Sea Hunter (vídeo de gameplay, download
do JAR) ficam na fonte como material de referência para uso futuro. Eles renderizam em **zero
dos cinco formatos** — o que agora é o comportamento pretendido, não um defeito. Todo renderer
lê apenas `title` / `date` / `awarder` / `summary` / `url` de um prêmio e ignora campos
desconhecidos.

Duas coisas foram ajustadas para tornar isso seguro:

- **Espelhado no pt_BR**, com labels traduzidos. A regra é os dois idiomas sempre, mesmo para
  dado que nada renderiza — senão os arquivos divergem e a próxima checagem de paridade acusa.
- **Documentado no `meta.notes`** dos dois arquivos, para não ser sinalizado de novo como dado
  morto por uma revisão futura. A nota registra que o campo é deliberado, não renderizado e válido.

**Risco de schema: descartado.** Não consegui acessar o schema pela rede, mas a cópia vendorada
em `node/node_modules/resume-schema/schema.json` (v1.0.0) resolve:

| Objeto | `additionalProperties` |
|---|---|
| nível raiz | **false** — não adicionar chaves novas na raiz |
| itens de `awards` | **true** — extras permitidos, então `links` é válido |
| `meta` | **true** — por isso `summaries` e `notes` já funcionam |

Vale saber: o schema do item `awards` declara formalmente apenas `awarder`/`date`/`summary`/
`title`, então até o `url` existente passa só porque extras são permitidos. Ressalva — essa é a
cópia vendorada do npm; o `$schema` aponta para a branch master no GitHub, que pode diferir.

---

## Conhecido, não corrigido, não bloqueia

| Item | Situação |
|---|---|
| **O mestre continua com 6 páginas**, nos dois idiomas | Enxugar o resumo liberou ~⅓ de página; a divisão de bullet e o bullet mais longo (e melhor) de `work[2]` consumiram esse espaço de volta. Resolvido para submissões pelo `mise run short` (**3 páginas**, diplomas preservados). **Encolher o mestre está fora de questão agora** — a P8 era a alavanca e você decidiu não fundir, corretamente: os blocos registram mudanças reais de foco. O mestre segue como arquivo de 6 páginas e o `mise run short` é o artefato a enviar. |
| **A plataforma "nacional" é permanentemente não quantificada** | `:85` nos dois idiomas: "Mantive uma plataforma web de abrangência nacional em produção, entregando novas funcionalidades com tráfego ativo." Os números de tráfego, usuários e volume de requisições **não existem / não estão disponíveis**, então isso não se resolve reescrevendo. Classificado originalmente como *lacuna do currículo*; não é lacuna do currículo nem de candidatura, e sim uma **lacuna de dado inexistente**. A afirmação fica como está — "nacional" é um fato sobre alcance, defensável em entrevista com "não tenho os números de tráfego". Não levantar de novo. |
| **O impacto da plataforma de onboarding ainda não é mensurável** | Construída e em teste; não existem números de produção. O ganho é esperado tanto em tempo (nove etapas automatizadas, mais acompanhamento, notificações e triggers que poupam esforço do staff) quanto em qualidade operacional — mas nada disso está medido, então **nenhum número vai para o currículo**; uma estimativa seria um resultado fabricado. O bullet agora declara capacidade. **Revisitar quando houver dado de produção** — tempo por onboarding antes → depois é a figura a capturar, e ela tiraria o impacto de 13/25. |
| **Terraform é lacuna de candidatura — não adicionar** | Você escreveu scripts Ansible e Helm charts e usou Kustomize, mas não lembra de ter usado Terraform, "pelo menos não diretamente". Então ele fica fora do currículo: alegar isso é justamente o que uma entrevista técnica derruba em um minuto. Ansible/Helm/Kustomize cobrem o mesmo terreno para a maioria das vagas; se uma vaga exigir Terraform como requisito obrigatório, isso é uma lacuna real a considerar, não um problema de redação. Não levantar de novo. |
| **Nenhuma afirmação de liderança depois de 2022** | Você exerceu o papel de liderança técnica em todos os projetos em que foi alocado **até 2022**; o cargo atual (2026) não faz nenhuma afirmação de liderança, e o currículo corretamente não inventa uma. Para um alvo staff isso é uma lacuna real do *histórico*, não da redação — nada a corrigir aqui, mas espere a pergunta na triagem ("como é sua liderança hoje?"). Relacionado à **P13**, a questão de título/senioridade. |
| **`Mentoria` é a única palavra-chave de liderança ainda não confirmada** | `Mentoring` / `Mentoria` em Processos e Liderança (en `:270`, pt `:260`) nunca foi confirmada explicitamente — você descreveu o papel de liderança técnica e a prática de code review, não mentoria em si. Mantida, porque liderar tecnicamente equipes de 6 a 15 pessoas por nove anos sem mentorar é implausível e, diferente do OpenTelemetry, é uma atividade e não uma ferramenta que se usou ou não. Remova se preferir não ter que defendê-la. |
| **Blocos separados por fase — decidido, não levantar de novo** | As oito entradas de `work` ficam como estão. Seu cargo não mudou, mas a forma de atuação e as tecnologias mudaram, então cada bloco registra uma fase distinta. **Correção à minha revisão anterior:** escrevi que quem lê o mesmo título duas vezes entende *enchimento*. Foi exagero — mesmo empregador, mesmo cargo, períodos distintos é uma forma normal e legível de mostrar uma passagem longa com fases, e o `summary` de cada entrada já diz o foco. Minha preocupação real era a contagem de páginas, que você acabou de resolver. |
| **Passado no cargo atual — decidido, não levantar de novo** | Mantido como está. O cargo está em andamento, mas os projetos dentro dele já terminaram, então "Built solo", "Shipped", "Delivered" descrevem uma entrega concluída e não o status do cargo. Essa é a leitura correta e coincide com a convenção documentada no `SKILL.md`. O presente seria de fato *menos* preciso aqui, porque sugeriria que o trabalho ainda está em curso. |
| **A URL da dissertação agora é canônica** | `https://shorturl.at/p0ZhO` substituída por `https://repositorio.ufpe.br/handle/123456789/2601` nos dois idiomas — um handle do repositório institucional da UFPE, muito mais durável que um encurtador e não descartado por parsers. **Não verificada**: `repositorio.ufpe.br` está fora da allowlist de rede, então esta é a sua resolução aceita sob confiança. |
| **Grade de competências em duas colunas — aceita e documentada** | A grade do `pdf`/`html` se intercala na extração de texto puro: os níveis se desprendem das categorias e palavras-chave hifenizadas se quebram (`Multi-arch builds` → `Multi-` / `arch builds`). Mantida, porque a grade vale para leitores humanos e `txt`/`docx` já são de coluna única. A mitigação é a escolha do artefato, não cirurgia no tema. Agora documentado no `README.md` → **"Which format to submit"**, com os comandos de verificação. Não levantar de novo. |
| **Verbo da plataforma de onboarding — fechado em "automatiza"** | Ainda em teste, então o original "que substituiu um processo manual de nove etapas" era exagerado: soa como implantação concluída. "**Automatiza**" é o que vai, e é preciso hoje. **Revisitar quando entrar em produção** — aí "substitui" passa a ser preciso e mais forte, e o antes/depois de produção fica capturável ao mesmo tempo. |
| **Três publicações nunca terão URL — encerrado** | Só o KSACI tem (capítulo na Springer, verificado). KEOPS, WJogos e o artigo da BCS-CMSG não têm DOI, não têm registro em índice, e você não tem os PDFs. Os **registros bibliográficos agora estão corretos e completos** — títulos, veículos, faixas de página, posição de autoria — que é o que um leitor pode de fato conferir. Uma citação sem link é normal para artigos de workshop de 2001–2008 em eventos pequenos. Não levantar de novo. |
| **Cabeçalho e títulos — resolvido** | O `basics.label` fica como **"Engenheiro de Software Sênior"** e as entradas de trabalho levam os títulos oficiais (`work[0]` = "Principal Technical Manager · Engenharia de Backend e Plataforma"). Cabeçalho = cargo-alvo, entradas = títulos reais: uma separação normal e amigável a ATS. Consequência a aceitar: o `basics.summary` abre com "Engenheiro backend sênior" e as quatro variantes de `meta.summaries` abrem com "engenheiro"/"líder de engenharia", concordando agora com o cabeçalho e não com o `work[0]`. Isso é coerente nesta escolha. |
| **Títulos pré-2009 estão corretos** | As entradas 4–7 (2000-06 → 2009-01) mantêm Engenheiro de Software Júnior ×2, Engenheiro de GCS, Engenheiro Sênior de GCS — confirmados como os títulos reais. Com os títulos de 2009 em diante, a progressão fica Júnior → Engenheiro de GCS → Engenheiro Sênior de GCS → Technical Manager → Senior Technical Manager → Principal Technical Manager. Não levantar de novo. |
| **Sentry — posicionado, P6 encerrada** | Usado em todos os projetos depois de 2022, então o bullet foi para o `work[1]` (2022-10 – 2025-12), onde a prática começa: "Configurei e operei o monitoramento de erros com Sentry nas duas plataformas — criando projetos por ambiente e instrumentando as aplicações de frontend e backend." Não duplicado no `work[0]`; repetir um bullet em blocos adjacentes traz de volta a aparência de enchimento. `Sentry` está nas `keywords` dos dois cargos, então o cargo atual segue etiquetado. O OpenTelemetry foi removido antes — nunca usado. |
| **C e Asterisk removidos por completo** | A pedido, toda referência saiu dos dois idiomas e dos dez artefatos (verificado: 0 ocorrências de C como palavra, `Asterisk`, `telephony`/`telefonia`). Isso foi além das duas palavras: o `work[3].h[0]` foi apagado (5 → 4 bullets, era inteiramente sobre a plataforma de telefonia), o `work[3].summary` foi reescrito, o `work[3].keywords` perdeu as duas entradas, e o qualificador de cargo teve de ser refeito a partir do que sobrou — agora **"Technical Manager · Java Corporativo e Mobile"** (en: "Enterprise Java & Mobile"), substituindo o aprovado "Telefonia e Java Corporativo", que ficara meio falso. A linha poliglota no `basics.summary` e no `meta.summaries.backend` caiu para "Java, PHP, Ruby e Python". Consequência a aceitar: aquele cargo agora soa como Java corporativo puro, e o currículo não contém mais nenhum trabalho de baixo nível. |
| **Paginação: WeasyPrint e Chrome divergem, e isso é esperado** | Salvar o `resume.html` pelo Chrome dá ~5 páginas onde o WeasyPrint dá 6. **Não reproduzido** — não foi possível rodar o Chrome headless neste ambiente. Duas causas candidatas, distinguíveis ajustando o diálogo de impressão do Chrome para Margens **Padrão** e Escala **100%** e salvando de novo: se continuar 5, é diferença de engine (a fragmentação de grid do WeasyPrint 69 é mais fraca que a do Blink — o `references/pipeline.md` já documenta a falha em resolver `repeat(auto-fill, …)`); se der 6, o diálogo estava sobrepondo o `@page { margin: 14mm 14mm 16mm 14mm }`. **Descartado:** substituição de fonte — o IosevkaTermSlab está instalado localmente (207 resultados no `fc-list`), então os dois engines usam as mesmas métricas. As 5 páginas do Chrome não são automaticamente "certas": se vierem de margens menores, o PDF tem menos respiro do que o tema pretende, e a saída do WeasyPrint é a que o build entrega. |
| **Por que seções deixam espaço em branco antes de quebrar** | O `Section` já é forçado a `break-inside: auto` (`Resume.jsx:20-25`), sobrepondo o `avoid` fixo do `@jsonresume/core`, e o `Item` omite `break-inside: avoid` de propósito — o comentário na linha `~271` registra que proibir isso somava ~2 páginas. As regras `avoid` que restam são estreitas e intencionais: `CompactItem` (~291), `ItemHeader` (~314, mais `break-after`), `Card` (~439) e o `break-after: avoid` do `SectionTitle` (~252), para um título nunca ficar sozinho no pé da página. Quando um título mais sua primeira entrada indivisível não cabem, os dois vão juntos — é esse o espaço vazio. É também por isso que a contagem de páginas oscila com mudanças pequenas de conteúdo. |
| **Corrigido: seções pulavam de página deixando espaço em branco** | O `ItemHeader` tinha um `break-after: avoid` sem condição. Uma entrada de formação sem summary e sem courses tem o header como *único* filho, então a regra não tinha irmão seguinte dentro do `Item` e se propagava para a próxima caixa em fluxo — o `SectionTitle` de `PUBLICAÇÕES`, que carrega o seu próprio `break-after: avoid` — encadeando até o grupo inteiro se mover. Isso deixava cerca de meia página vazia. Agora está restrito com `&:not(:last-child)`, então um header só se recusa a separar de um corpo que ele de fato tem. Resultado: os dois diplomas ficam na mesma página, `CERTIFICAÇÕES` saiu da página 6 para a 5, e as páginas 4–5 ganharam 2 linhas cada. **A contagem total de páginas não mudou** (6 nos dois idiomas) — o espaço recuperado é cerca de meia página, não uma inteira. O conteúdo é idêntico; só as posições de quebra de linha mudaram. |
| **Chrome vs WeasyPrint: ainda é hipótese** | O save-as-PDF do Chrome dá ~5 páginas contra 6 do WeasyPrint. **Não reproduzido** — não foi possível rodar o Chrome headless aqui (travou e foi encerrado). Descartado: substituição de fonte (o IosevkaTermSlab está instalado, 207 resultados no `fc-list`, então as métricas coincidem). Provavelmente diferença de engine — o WeasyPrint propaga `break-after: avoid` de um header último-filho de forma mais agressiva que o Blink, o mesmo mecanismo do bug acima, então o Chrome talvez nunca tenha pagado esse custo. Para descartar a explicação mais simples, ajuste o diálogo do Chrome para Margens **Padrão** e Escala **100%** e salve de novo: se continuar 5, é engine; se der 6, o diálogo estava sobrepondo o `@page { margin: 14mm 14mm 16mm 14mm }`. |
| **Afirmações de trabalho solo removidas — encerrado** | As quatro que restavam (`basics.summary`, `work[0].summary`, `meta.summaries.backend`, `meta.summaries.lead`) saíram na reescrita dos resumos. Verificado: zero ocorrências de "sozinho" nos dois arquivos-fonte. Substituídas por "entrega plataformas internas do modelo de dados à implantação", que declara a amplitude do trabalho sem alegar tamanho de equipe e é sustentada pelos bullets. Custo aceito: propriedade ponta a ponta é um sinal raro de nível Principal, e o documento não o faz mais em lugar nenhum. |
| **Data de conclusão do bacharelado corrigida — encerrado** | Agora `1996-01..1999-12` nos dois idiomas, coincidindo com os dois lugares em que o Lattes diz 1999. Corrigido pelo dono do repositório. |
| **Nova alavanca: `--no-highlights`** | Omite todas as listas de `work[].highlights` mantendo título, empregador, datas e resumo de cada cargo. Leva o PDF do mestre de **6 páginas para 4**, e combinado com `--summary ats --cut-date 2013` chega a **3**. As duas tasks `mise run short` já usam a flag. Isso significa que o mestre pode encurtar sem apagar nada da fonte — que é a resposta à pressão de páginas que atravessou esta revisão. Só o `work` é afetado; `projects` e `volunteer` mantêm os seus. |
| **Corrigido: competências agora na página 1** | As seções foram reordenadas para o `skills` abrir o documento, logo abaixo do resumo — estava na página 4 de 6, atrás de oito entradas de trabalho, exatamente onde um filtro por palavra-chave e um ATS nunca chegam. A experiência agora começa na página 2; essa é a troca deliberada. |
| **Corrigido: os cinco caminhos de renderização compartilham uma ordem** | Eles tinham divergido — md/txt/docx e o fallback Jinja punham formação antes de competências, o tema punha competências antes de formação. Agora é uniformemente `skills → work → projects → volunteer → education → certificates → publications → awards → languages → interests → references`. Verificado comparando o multiconjunto de palavras extraídas antes e depois: idêntico, então a mudança foi só de ordem. |

---

## Ordem recomendada

Nada está bloqueando. O único item aberto é cosmético:

1. **O1** — oscilação na contagem de páginas do pt_BR. Os dois idiomas estão hoje em 6 páginas,
   e o `--no-highlights` entrega um mestre de 4 páginas e uma variante de submissão de 3 sob
   demanda, então isso pesa menos do que antes. Aceitar a oscilação, ou fixar `--zoom 82%` na
   task do pt.

Duas coisas que não consegui resolver e deixo para você:

- **Paginação Chrome vs WeasyPrint** — não reproduzida. Ajuste o diálogo do Chrome para Margens
  **Padrão** e Escala **100%** e salve de novo: continuar em 5 páginas indica diferença de
  engine; dar 6 indica que o diálogo estava sobrepondo o `@page`.
- **Um mestre de 5 páginas** — a página 6 só tem duas certificações ClearCase e Idiomas. Enxugar
  um pouco ali, ou remover as três certificações de 2002, chega a 5 sem o `--no-highlights`.
