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

**Pontuação: 65 → 72/100.** Dois componentes se moveram, ambos por respostas suas:

| Componente | Peso | Era | Agora | Por quê |
|---|---|---|---|---|
| Cobertura de hard skills / palavras-chave | 30 | 25 | 25 | sem alteração |
| Evidência de impacto | 25 | 9 | **13** | A P4 trouxe o primeiro resultado *recente* quantificado — cobertura de 0% para ~80% em um repositório e de ~50% para ~80% em outros quatro. Antes disso, o único número do documento era de um cargo encerrado em 2005. |
| Aderência de senioridade e escopo | 20 | 15 | **16** | A P2 colocou o tamanho das equipes no papel (6 a 15 engenheiros em quatro projetos), então a afirmação de liderança agora tem escopo. |
| Aderência de domínio | 15 | 13 | 13 | sem alteração |
| Legibilidade em triagem | 10 | 3 | **5** | A abertura de 172 palavras acabou e os cabeçalhos do pt_BR estão localizados; ainda são 6 páginas com competências na página 4. |

**As quatro perguntas de métrica estão encerradas, e 13/25 é o teto por agora.** O bullet de
cobertura é o único resultado recente quantificado; em todo o resto, o trabalho recente ainda
conta artefatos — nove dashboards, quatro apps, seis ferramentas. Os dois caminhos que restam
estão bloqueados pela realidade, não pela redação: o dado de tráfego da P3 não existe, e a
plataforma de onboarding ainda não foi medida em produção (veja abaixo). Revisitar quando for.

---

## Bloqueando — depende da sua resposta

### Fatos que eu não consigo inferir

| # | Pergunta | Por que importa |
|---|---|---|
| **P6** | Você foi responsável por **observabilidade** — OpenTelemetry, Sentry? | Estão apenas em `skills.keywords` (en `:260`, pt `:250`) e nunca aparecem em um highlight. Parsers de ATS leem a prosa do documento, não o seu esquema de etiquetas, então como está hoje eles são efetivamente ausentes. Se foi você, merece um bullet; se era ambiente, provavelmente deveria sair das palavras-chave. |

### Decisões

| # | Decisão | Observações |
|---|---|---|

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
| **Competências caem na página 4 de 6** no PDF do mestre | Consequência da contagem de páginas. Na variante enxuta elas ficam na página 1. |
| **A ordem das seções difere entre formatos** | `md`/`txt`: Work → Education → Skills → Awards → Certifications → Publications → Languages. `pdf`/`html`: Experience → Skills → Education → Publications → Awards → Languages → Certificates. Nenhuma está errada, mas "o que o recrutador vê primeiro" precisa ser ajustado duas vezes. Unificar é uma mudança pequena, se você quiser. |

---

## Ordem recomendada

1. **P6** — a última pergunta que depende de um fato: qual(is) cargo(s) levam o trabalho com Sentry.
2. **P13** — a decisão de senioridade/título.
3. **P18** — opcional; torna escaneável a sua razão para os blocos separados.
4. **P15–P16** — detalhes dos registros das publicações; nenhum é bloqueante.
