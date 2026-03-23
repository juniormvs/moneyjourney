# Base de Conhecimento

## Dados Utilizados

Descreva se usou os arquivos da pasta `data`, por exemplo:

| Arquivo | Formato | Utilização no Agente |
|---------|---------|---------------------|
| `historico_atendimento.csv` | CSV | Contextualizar interações anteriores, e dar respostas mais inteligentes. |
| `perfil_investidor.json` | JSON | Personalizar recomendações tanto de tópicos explicativos, dicas, quanto investimentos. |
| `produtos_financeiros.json` | JSON | Sugerir produtos adequados ao perfil, de acordo com o perfil avaliado. |
| `transacoes.csv` | CSV | Analisar padrão de gastos do cliente, tendo assim uma base de comportamento financeiro do usuário. |

---

## Adaptações nos Dados

> Você modificou ou expandiu os dados mockados? Descreva aqui.

O produto Fundo Imobiliário (FII) foi acrescentado, expandindo o leque de opções.

---

## Estratégia de Integração

### Como os dados são carregados?
> Descreva como seu agente acessa a base de conhecimento.

Existem duas possibilidades, injetar os dados diretamente no prompt (ctrl +c, crt+v) ou carregar os arquivos via código como no exemplo abaixo.

```
import pandas as pd
import json

#CSV
historico = pd.read_csv('data/historico_atendimento.csv')
transacoes = pd.read_csv('data/transacoes.csv')

#JSON
with open('data/perfil_investidor.json', 'r', encoding='utf='8') as file:
  perfil = json.load(file)

with open('data/produtos_financeiros.json', 'r', encoding='utf=8') as file:
  produtos = json.load(file)

```


### Como os dados são usados no prompt?
> Os dados vão no system prompt? São consultados dinamicamente?
Podemos inserir os dados diretamente no prompt, deixando assim o assistente mais consistente e com menor chance de alucinação.

```text
DADOS E PERFIL DO CLIENTE:[data/perfil_investidor.json]
{
  "nome": "João Silva",
  "idade": 32,
  "profissao": "Analista de Sistemas",
  "renda_mensal": 5000.00,
  "perfil_investidor": "moderado",
  "objetivo_principal": "Construir reserva de emergência",
  "patrimonio_total": 15000.00,
  "reserva_emergencia_atual": 10000.00,
  "aceita_risco": false,
  "metas": [
    {
      "meta": "Completar reserva de emergência",
      "valor_necessario": 15000.00,
      "prazo": "2026-06"
    },
    {
      "meta": "Entrada do apartamento",
      "valor_necessario": 50000.00,
      "prazo": "2027-12"
    }
  ]
}
TRANSACOES DO CLIENTE: [data/transacoes.csv]
data	descricao	categoria	valor	tipo
2025-10-01	Salário	receita	5000.00	entrada
2025-10-02	Aluguel	moradia	1200.00	saida
2025-10-03	Supermercado	alimentacao	450.00	saida
2025-10-05	Netflix	lazer	55.90	saida
2025-10-07	Farmácia	saude	89.00	saida
2025-10-10	Restaurante	alimentacao	120.00	saida
2025-10-12	Uber	transporte	45.00	saida
2025-10-15	Conta de Luz	moradia	180.00	saida
2025-10-20	Academia	saude	99.00	saida
2025-10-25	Combustível	transporte	250.00	saida

PRODUTOS DISPONIVEIS PARA CONSULTA: [data/produtos_financeiros.json]
[
  {
    "nome": "Tesouro Selic",
    "categoria": "renda_fixa",
    "risco": "baixo",
    "rentabilidade": "100% da Selic",
    "aporte_minimo": 30.00,
    "indicado_para": "Reserva de emergência e iniciantes"
  },
  {
    "nome": "CDB Liquidez Diária",
    "categoria": "renda_fixa",
    "risco": "baixo",
    "rentabilidade": "102% do CDI",
    "aporte_minimo": 100.00,
    "indicado_para": "Quem busca segurança com rendimento diário"
  },
  {
    "nome": "LCI/LCA",
    "categoria": "renda_fixa",
    "risco": "baixo",
    "rentabilidade": "95% do CDI",
    "aporte_minimo": 1000.00,
    "indicado_para": "Quem pode esperar 90 dias (isento de IR)"
  },
  {
    "nome": "Fundo Multimercado",
    "categoria": "fundo",
    "risco": "medio",
    "rentabilidade": "CDI + 2%",
    "aporte_minimo": 500.00,
    "indicado_para": "Perfil moderado que busca diversificação"
  },
  {
    "nome": "Fundo de Ações",
    "categoria": "fundo",
    "risco": "alto",
    "rentabilidade": "Variável",
    "aporte_minimo": 100.00,
    "indicado_para": "Perfil arrojado com foco no longo prazo"
  },
  {
    "nome": "Fundo Imobiliário (FII)",
    "categoria": "fundo",
    "risco": "medio",
    "rentabilidade": "Variável - 6% a 12% ao ano",
    "aporte_minimo": 100.00,
    "indicado_para": "Perfil moderado que busca diversificação e renda recorrente mensal"
  }
]

HISTORICO ATENDIMENTO DO CLIENTE: [data/historico_atendimento.csv]
data	canal	tema	resumo	resolvido
2025-09-15	chat	CDB	Cliente perguntou sobre rentabilidade e prazos	sim
2025-09-22	telefone	Problema no app	Erro ao visualizar extrato foi corrigido	sim
2025-10-01	chat	Tesouro Selic	Cliente pediu explicação sobre o funcionamento do Tesouro Direto	sim
2025-10-12	chat	Metas financeiras	Cliente acompanhou o progresso da reserva de emergência	sim
2025-10-25	email	Atualização cadastral	Cliente atualizou e-mail e telefone	sim
```

---

## Exemplo de Contexto Montado

> Mostre um exemplo de como os dados são formatados para o agente.

Aqui é um exemplo de dados extraídos da própria base de dados do projeto, de forma mais organizada, padronizada, concisa e clara, viabilizando um prompt mais objetivo, seguindo boas práticas de economia de tokens.

```
Dados do Cliente:
- Nome: João Silva
- Perfil: Moderado
- Objetivo: Construir reserva de emergência
- Reserva atual: R$ 15.000 (meta: R$ 20.000)

Resumo de Gastos:
- Moradia: R$ 1.300
- Alimentação: R$ 570
- Transporte: R$ 295
- Saúde: R$ 188
- Lazer: R$ 55,90
- Total de saídas: R$ 2.488,90

Produtos Disponíveis Para Explicar/Sugerir
- Tesouro Selic (risco baixo)
- CDB Liquidez Diária (risco baixo)
- LCI/LCA (risco baixo)
- Fundo Imobiliário - FII (risco médio)
- Fundo de Ações (risco médio)
```
