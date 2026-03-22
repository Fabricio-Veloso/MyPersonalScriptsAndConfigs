# Spec: planner foundation

## Objetivo

Definir a fundacao do planner da CLI para transformar um profile declarado e o estado atual da maquina em um plano previsivel, legivel e reexecutavel, sem aplicar mudancas durante o planejamento.

## Contexto atual

O projeto ja possui uma primeira fundacao funcional de `plan` em `src/personal_setup/services/planner.py`. Hoje o planner:

- carrega o profile declarado
- resolve dependencias entre modulos
- deduplica modulos repetidos
- identifica erros estruturais como modulo desconhecido, dependencia ausente e dependencia circular
- produz passos com `keep`, `install`, `configure`, `skip` ou `blocked`

Essa base ja e suficiente para sustentar a primeira versao da CLI, mas ainda deixa em aberto:

- quais contratos os modulos precisam respeitar para responder ao planner
- como evoluir de `install/configure` para tipos de acao mais ricos sem perder simplicidade
- como representar melhor bloqueios ou pre-condicoes entre modulos no resultado final

Sem consolidar essa semantica, a implementacao concreta de `check()`, `apply()` e `verify()` em cada modulo pode voltar a divergir com o tempo.

## Entrada

- nome de um profile
- definicao declarativa do profile carregada do diretorio `profiles/`
- registry de modulos disponiveis na aplicacao
- plataforma atual detectada pela aplicacao
- resultado de `check()` de cada modulo considerado no plano

## Saida esperada

Um `PlanResult` que represente o que a CLI pretende fazer para aproximar o estado atual do estado desejado, contendo no minimo:

- profile resolvido
- plataforma atual
- lista ordenada de passos
- acao de cada passo
- motivo de cada decisao
- indicacao de bloqueios quando houver erro estrutural de planejamento

O plano precisa ser apenas descritivo. Ele nao instala, nao configura e nao altera estado do sistema.

## Restricoes ou regras

- O planner deve ser deterministico para a mesma entrada e o mesmo estado observado.
- O planner deve tratar o profile como fonte de verdade do estado desejado.
- O planner nao deve depender de menus interativos ou perguntas ao usuario para montar o plano.
- Modulos nao suportados na plataforma atual devem aparecer como `skip`, e nao como erro.
- Modulos que ja satisfazem o baseline esperado devem aparecer como `keep`.
- Modulos que exigem acao devem aparecer com a acao mais especifica disponivel, priorizando `install` ou `configure` quando o contrato do modulo permitir.
- O planner deve resolver dependencias entre modulos antes de montar a ordem final do plano.
- Dependencias devem ser planejadas antes dos modulos que dependem delas.
- Dependencia ausente no registry deve bloquear o planejamento.
- Dependencia circular deve bloquear o planejamento.
- Modulo referenciado no profile e ausente no registry deve bloquear o planejamento.
- Bloqueios de planejamento devem acontecer antes de qualquer tentativa de `apply()`.
- O planner deve preferir simplicidade: a fundacao atual aceita `keep`, `install`, `configure`, `skip` e `blocked`, evitando explodir cedo demais a quantidade de tipos de passo.
- A ordem declarada no profile pode servir como prioridade humana, mas nao pode violar a ordem de dependencias.

## Impacto em modulos, interfaces, configuracoes, armazenamento de dados e integracoes, se houver

- `src/personal_setup/services/planner.py` ja concentra ordenacao por dependencias e bloqueios estruturais, mas ainda pode evoluir na forma como explica razoes e pre-condicoes.
- `src/personal_setup/models/plan.py` ja representa dependencias e bloqueios basicos, mas pode evoluir se o plano precisar carregar mais contexto.
- `src/personal_setup/models/module.py` ja diferencia readiness, install, configure e bloqueio, mas ainda pode ganhar semantica adicional conforme surgirem mais modulos.
- `src/personal_setup/modules/base.py` deve continuar simples, mas com semantica mais clara para `check()`, `apply()` e `verify()`.
- `profiles/` continua como entrada declarativa principal, sem necessidade de mudar formato nesta etapa.
- `tests/` precisara cobrir resolucao de dependencias, ordem de passos e erros estruturais.

## Casos principais

- Um profile lista modulos validos sem dependencias e o planner produz uma sequencia simples de `keep`, `install`, `configure` e `skip` conforme o estado observado.
- Um modulo depende de outro e o planner garante que o modulo de base apareca antes do dependente.
- Um modulo Windows-only aparece em Linux e o planner o marca como `skip` com motivo claro.
- Um modulo faltante no sistema retorna `install` com motivo derivado do `check()`.
- Um modulo instalado, mas com config ou inicializacao faltando, retorna `configure`.
- Um modulo ja atendido retorna `keep` com motivo estavel e legivel.

## Casos de borda relevantes

- O profile referencia um modulo desconhecido.
- Um modulo declara dependencia de outro modulo inexistente.
- Dois ou mais modulos formam dependencia circular.
- Um modulo e aplicavel, mas seu `check()` retorna dados insuficientes ou ambiguos para o planner.
- Um mesmo modulo entra no plano tanto por declaracao direta no profile quanto por dependencia de outro modulo.
- O profile contem modulos repetidos.

## Criterio de aceite

- O planner gera um plano estavel e legivel para o mesmo profile no mesmo estado observado.
- Dependencias aparecem antes dos modulos dependentes no plano final.
- Modulos nao aplicaveis sao reportados como `skip`.
- Modulos prontos sao reportados como `keep`.
- Modulos pendentes sao reportados como `install` ou `configure`, conforme o contrato do modulo.
- Erros estruturais de planejamento sao reportados como `blocked` ou excecao tipada equivalente antes de qualquer execucao.
- A fundacao do planner deixa explicito o contrato esperado dos modulos sem exigir implementacao completa dos setups reais nesta etapa.
