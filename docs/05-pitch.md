# Pitch — MoneyJourney 💹

## Visão Geral

| Item | Detalhe |
|---|---|
| **Duração** | 3 minutos |
| **Formato** | Vídeo gravado com gravação de tela |
| **Público** | Avaliadores do bootcamp DIO/Bradesco + Recrutadores de tecnologia |
| **Tom** | Direto, confiante e técnico — sem enrolação |

---

## Roteiro Completo

> 💡 **Como usar este roteiro:**
> Cada bloco indica o que falar e o que mostrar na tela simultaneamente.
> Grave a tela do projeto rodando enquanto narra o texto em voz alta.

---

### ⏱️ 0:00 — 0:30 | Abertura — O Problema

**O que mostrar na tela:** tela inicial do chat MoneyJourney

**O que falar:**
> "A maioria das pessoas não investe. Não por falta de dinheiro — mas por falta de orientação acessível. Contratar um consultor financeiro custa caro. Pesquisar sozinho é confuso. E chatbots genéricos não conhecem o seu perfil.
>
> O MoneyJourney resolve isso. É um agente financeiro inteligente, construído com IA Generativa, que conhece o perfil do cliente, analisa seus gastos reais e indica investimentos adequados — de forma educativa, segura e personalizada."

---

### ⏱️ 0:30 — 1:00 | Demonstração — O Agente em Ação

**O que mostrar na tela:** fazer ao vivo (ou mostrar gravado) três perguntas no chat:
1. "Para onde está indo meu dinheiro?"
2. "Qual investimento você recomenda para mim?"
3. "Me fale sobre futebol." ← para mostrar o escopo

**O que falar:**
> "Aqui está o agente funcionando. Quando pergunto sobre meus gastos, ele analisa as transações reais do cliente e responde com dados concretos. Quando peço uma recomendação, ele considera o perfil moderado, os objetivos e o patrimônio atual antes de sugerir qualquer produto.
>
> E quando tento fugir do escopo — pedindo algo fora de finanças — ele recusa educadamente e redireciona. Isso não é sorte. É engenharia de prompt."

---

### ⏱️ 1:00 — 1:30 | Diferencial 1 — Segurança e Prompt Injection

**O que mostrar na tela:** tentar um ataque de Prompt Injection ao vivo — ou mostrar o print da evidência

**O que falar:**
> "No setor financeiro, segurança não é opcional. Por isso testei o agente contra três níveis de ataque de Prompt Injection — desde instruções diretas até injeção de comandos dentro dos próprios dados do contexto.
>
> Em todos os casos, o agente manteve sua identidade e recusou seguir as instruções maliciosas. Isso foi alcançado não com filtros externos, mas com arquitetura de prompt — identidade forte, escopo positivo e instrução explícita contra manipulação."

---

### ⏱️ 1:30 — 2:00 | Diferencial 2 — Dashboard de Métricas

**O que mostrar na tela:** navegar pelo dashboard — mostrar os gráficos de latência, tokens e feedbacks

**O que falar:**
> "Além do chat, o projeto conta com um dashboard completo de observabilidade. Cada interação é registrada automaticamente — latência, tokens consumidos, velocidade de geração e feedback do usuário.
>
> Com 48 interações registradas durante os testes, o agente atingiu 94% de taxa de satisfação nos feedbacks coletados. Esses dados não são estimativas — são métricas reais, coletadas em produção, visualizadas com Plotly."

---

### ⏱️ 2:00 — 2:30 | Diferencial 3 — Comparador de Modelos

**O que mostrar na tela:** abrir o comparador, digitar uma pergunta e mostrar os 5 modelos respondendo simultaneamente

**O que falar:**
> "E para ir além do básico, implementei um comparador de modelos LLM. Com uma única pergunta, é possível testar simultaneamente cinco modelos diferentes — GPT OSS 120B, GPT OSS 20B, LLaMA, Mixtral e Gemma — e comparar latência, velocidade e qualidade das respostas lado a lado.
>
> Isso permite escolher o modelo mais eficiente para cada caso de uso, com dados reais — não benchmarks de papel."

---

### ⏱️ 2:30 — 3:00 | Encerramento — Arquitetura e Próximos Passos

**O que mostrar na tela:** voltar para o chat ou mostrar a estrutura de arquivos no VS Code

**O que falar:**
> "O projeto foi construído com Python, Streamlit, Groq API e Plotly, seguindo uma arquitetura em camadas — separando interface, lógica de negócio e visualização. Tudo documentado, testado e com código limpo.
>
> Os próximos passos naturais são suporte a múltiplos perfis de clientes, integração com dados em tempo real e deploy em produção.
>
> Me chamo [seu nome]. Sou desenvolvedor focado em aplicações com IA Generativa. O MoneyJourney é a prova de que é possível construir soluções financeiras inteligentes, seguras e observáveis — do zero. Obrigado."

---

## Checklist Antes de Gravar

- [ ] Projeto rodando localmente sem erros
- [ ] `metricas.csv` com dados reais para o dashboard aparecer populado
- [ ] `metricas_comparador.csv` com pelo menos uma comparação registrada
- [ ] Perguntas de demonstração preparadas (não improvisar ao vivo)
- [ ] Resolução da tela adequada — fonte grande o suficiente para o vídeo
- [ ] Microfone testado — áudio claro é tão importante quanto o visual
- [ ] Falar devagar — 3 minutos passa rápido mas correria transmite insegurança

---

## Dicas para Recrutadores Técnicos

Se o vídeo chegar para recrutadores além do bootcamp, esses são os pontos que mais pesam na avaliação técnica:

- **Arquitetura em camadas** — `utils/charts.py` separado do `dashboard.py` mostra que você pensa em manutenibilidade
- **Métricas reais** — 94.1% de satisfação com 48 interações é um número concreto, não estimativa
- **Prompt Injection documentado** — poucos projetos de bootcamp chegam nesse nível de segurança
- **Comparador de modelos** — demonstra que você entende que o modelo é uma variável, não uma constante

---

## Frase de Impacto (para descrição do vídeo ou LinkedIn)

> "Construí um agente financeiro com IA Generativa que personaliza recomendações de investimento, resiste a ataques de Prompt Injection e monitora sua própria performance em tempo real — com dashboard interativo e comparador de 5 modelos LLM."
