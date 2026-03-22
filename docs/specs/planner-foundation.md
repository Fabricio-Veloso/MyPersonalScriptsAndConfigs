# Spec: planner foundation

## Objetivo

Definir a fundacao do planner da CLI para transformar um profile declarado e o estado atual da maquina em um plano previsivel, legivel e reexecutavel, sem aplicar mudancas durante o planejamento.

## Contexto atual

O projeto ja possui um esqueleto funcional de `plan` em `src/personal_setup/services/planner.py`, mas ele ainda trabalha com regras muito simples: percorre os modulos na ordem do profile, chama `check()` e produz `keep`, `apply` ou `skip`.

Essa base e suficiente para validar o fluxo inicial da CLI, mas ainda nao define de forma estavel:

- como dependencias entre modulos devem ser resolvidas
- quais erros pertencem ao planejamento
- como a ordem final dos passos deve ser calculada
- quais acoes o plano pode representar
- quais contratos os modulos precisam respeitar para responder ao planner

Sem essa definicao, a implementacao concreta de `check()`, `apply()` e `verify()` em cada modulo corre o risco de ficar inconsistente ou muito acoplada a detalhes temporarios da primeira versao.

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
- Modulos que exigem acao devem aparecer como `apply`.
- O planner deve resolver dependencias entre modulos antes de montar a ordem final do plano.
- Dependencias devem ser planejadas antes dos modulos que dependem delas.
- Dependencia ausente no registry deve bloquear o planejamento.
- Dependencia circular deve bloquear o planejamento.
- Modulo referenciado no profile e ausente no registry deve bloquear o planejamento.
- Bloqueios de planejamento devem acontecer antes de qualquer tentativa de `apply()`.
- O planner deve preferir simplicidade: a primeira fundacao aceita as acoes `keep`, `apply`, `skip` e `blocked`.
- A ordem declarada no profile pode servir como prioridade humana, mas nao pode violar a ordem de dependencias.

## Impacto em modulos, interfaces, configuracoes, armazenamento de dados e integracoes, se houver

- `src/personal_setup/services/planner.py` deve evoluir de iteracao simples para planejamento com resolucao de dependencias e bloqueios explicitos.
- `src/personal_setup/models/plan.py` provavelmente precisara de campos adicionais para representar bloqueios, dependencias e talvez origem do passo.
- `src/personal_setup/models/module.py` pode precisar endurecer o contrato de `CheckResult`, deixando mais claro o que significa estar pronto, ausente ou nao aplicavel.
- `src/personal_setup/modules/base.py` deve continuar simples, mas com semantica mais clara para `check()`, `apply()` e `verify()`.
- `profiles/` continua como entrada declarativa principal, sem necessidade de mudar formato nesta etapa.
- `tests/` precisara cobrir resolucao de dependencias, ordem de passos e erros estruturais.

## Casos principais

- Um profile lista modulos validos sem dependencias e o planner produz uma sequencia simples de `keep`, `apply` e `skip`.
- Um modulo depende de outro e o planner garante que o modulo de base apareca antes do dependente.
- Um modulo Windows-only aparece em Linux e o planner o marca como `skip` com motivo claro.
- Um modulo faltante no sistema retorna `apply` com motivo derivado do `check()`.
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
- Modulos pendentes sao reportados como `apply`.
- Erros estruturais de planejamento sao reportados como `blocked` ou excecao tipada equivalente antes de qualquer execucao.
- A fundacao do planner deixa explicito o contrato esperado dos modulos sem exigir implementacao completa dos setups reais nesta etapa.
