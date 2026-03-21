# AGENTS.md

## Objetivo do projeto

Construir uma ferramenta simples de CLI para instalar, configurar e validar o ambiente pessoal de trabalho do usuario de forma reexecutavel, modular e multiplataforma.

O projeto deve permitir replicar em uma nova maquina as ferramentas, configuracoes e ajustes necessarios do workflow pessoal, priorizando previsibilidade, facilidade de manutencao e evolucao incremental.

## Escopo positivo

- Instalar ferramentas e dependencias necessarias para o ambiente pessoal de trabalho.
- Aplicar configuracoes versionadas do usuario, como editor, atalhos, window manager, aliases e arquivos de suporte.
- Criar e ajustar estruturas locais necessarias, como pastas, links, arquivos de configuracao e pequenas automacoes auxiliares.
- Detectar o estado atual do ambiente e comparar com o estado desejado antes de aplicar mudancas.
- Validar se cada parte importante do setup ficou funcional apos a aplicacao.
- Permitir composicao do ambiente por modulos e perfis, mesmo que o projeto comece com um perfil principal unico.
- Funcionar no minimo em Windows e Linux, respeitando diferencas entre plataformas quando necessario.

## Escopo negativo

- Nao transformar o projeto em uma plataforma generica de provisionamento para terceiros.
- Nao tentar suportar todas as distribuicoes, gerenciadores de pacote ou ferramentas desde o inicio.
- Nao esconder a logica principal em scripts grandes, pouco testaveis e fortemente acoplados.
- Nao depender exclusivamente de menus interativos quando um fluxo declarativo e reexecutavel for suficiente.
- Nao modelar cedo demais uma arquitetura complexa de plugins, distribuicao binaria ou sincronizacao em nuvem sem necessidade real.

## Stack

- Python como linguagem principal da CLI e da orquestracao do setup.
- PowerShell e shell script como adaptadores pontuais quando fizer mais sentido para uma tarefa especifica da plataforma.
- Arquivos declarativos simples para perfis, modulos ou estado do ambiente, preferencialmente em formatos faceis de ler e editar.
- Git como base de versionamento das configuracoes, scripts, assets e decisoes estaveis do projeto.

Direcao atual da arquitetura:

- CLI declarativa e reexecutavel.
- Modulos por ferramenta ou capacidade.
- Perfil principal inicial com suporte a Windows e Linux.
- Separacao entre detectar estado, aplicar mudancas e validar resultado.

## Estrutura atual esperada

A estrutura pode evoluir, mas a direcao desejada e manter separacao clara entre:

- entrada da CLI
- definicao de perfis
- modulos de setup por ferramenta
- assets e configuracoes versionadas
- adaptadores especificos de plataforma
- estado local ou artefatos auxiliares, quando realmente necessarios

Organizacao conceitual esperada:

- `profiles/` para composicao do ambiente desejado
- `modules/` para capacidades isoladas como instalar, configurar e validar ferramentas
- `assets/` ou `configs/` para arquivos versionados do ambiente
- `platforms/`, `adapters/` ou equivalente para integracoes especificas de Windows e Linux
- `tests/` para testes pequenos e focados da logica principal

## Variaveis de ambiente

- Registrar aqui apenas variaveis que se tornarem estaveis e realmente necessarias para execucao, configuracao ou personalizacao do setup.
- Evitar depender de caminhos e valores hardcoded quando eles puderem ser inferidos, detectados ou declarados de forma mais clara.
- Quando uma variavel for obrigatoria, documentar nome, finalidade, formato esperado, valor padrao quando houver e impacto na execucao.

## Principios de implementacao

- Preferir simplicidade e mudancas pequenas.
- Respeitar os padroes ja usados no projeto sempre que forem suficientes.
- Nao mover o projeto para uma arquitetura mais complexa antes da necessidade.
- Fazer a menor mudanca que entregue comportamento correto e verificavel.
- Tratar o projeto como um gerenciador do ambiente pessoal, e nao apenas como um agrupado de scripts soltos.
- Priorizar modelagem por ferramenta ou capacidade, com fronteiras claras entre detectar, aplicar e validar.
- Preservar reexecucao segura e previsivel sempre que possivel, evitando passos destrutivos desnecessarios.
- Isolar diferencas entre plataformas em adaptadores pequenos, sem espalhar condicionais por toda a base.

## Modo de trabalho

Trabalharemos em iteracoes curtas, com alinhamento frequente sobre a proxima feature.

Fluxo esperado:

1. Criar uma branch para a sessão (o nome dela idealmente deve ser com base no que estamos fazendo).
2. Alinhar a feature ou correcao, entendendo a regra de negocio e o comportamento observavel esperado.
3. Registrar uma spec curta da tarefa, com contexto atual, entrada, saida esperada, restricoes, impactos tecnicos, casos principais, bordas relevantes e criterio de aceite.
4. Localizar os pontos afetados no sistema antes de editar, como modulos, interfaces, configuracoes, scripts, utilitarios, armazenamento de dados e integracoes relacionadas.
5. Quando fizer sentido, seguir TDD em ciclos curtos: escrever um teste que falha, implementar o minimo para faze-lo passar e refatorar com seguranca.
6. Implementar em pequenos passos, priorizando comportamento principal, evitando acumular responsabilidades em um unico passo e ajustando artefatos de configuracao ou estrutura de dados quando necessario.
7. Validar com testes automatizados relevantes e com o fluxo manual principal afetado; usar mocks para integracoes externas quando necessario e revisar impactos em interfaces, notificacoes, dados e outros pontos sensiveis.
8. Revisar impacto no sistema, incluindo efeitos colaterais em autenticacao, autorizacao, persistencia, integracoes e coerencia com a estrutura atual do projeto.
9. Consolidar no arquivo apenas decisoes que se tornarem estaveis.
10. Seguir as diretrizes de commits atomicos para fazer os commits.
11. Fazer rebase e depois merge para developement ou main ou outra branch escolhida.
12. Apagar a branch que usamos para trabalhar.

O usuario pode interromper a qualquer momento para corrigir entendimento, mudar a abordagem ou pedir explicacoes.

## Diretriz de commits

- Todo commit deve ser atomico.
- A regra para fechar um bloco de commit e: esta mudanca pode sofrer rollback sozinha sem afetar as demais?
- Se a resposta for sim, esse bloco pode virar um commit.
- No pior caso, aceitar um commit por arquivo inteiro, mas isso e o limite minimo de granularidade, nao o alvo.
- Quando um mesmo arquivo reunir mudancas de naturezas diferentes, separar os commits por hunk sempre que isso permitir isolar melhor cada comportamento ou responsabilidade.
- Ao preparar commits, separar refatoracoes estruturais por bloco coerente de responsabilidade, evitando misturar docs, regra de negocio e reorganizacao sem necessidade.
- Nao agrupar commits por arquivo quando o diff puder ser particionado por comportamento observavel, motivo da mudanca ou unidade de rollback.
- Antes de commitar, propor um plano curto de particionamento quando houver duvida razoavel sobre como dividir os blocos.

### Convencao de mensagem de commit

- Usar prefixos comuns e amplamente reconhecidos em historicos de commit, como `chore`, `feat`, `refac`, `fix`, `docs`, `test` e equivalentes apropriados ao contexto.
- Escolher o prefixo conforme o tipo da mudanca:
  - `feat` para comportamento novo entregue ao sistema
  - `fix` para correcao de bug ou regressao
  - `refac` para reorganizacao interna sem mudar comportamento
  - `docs` para documentacao quando esse for o foco principal do commit
  - `test` para cobertura automatizada quando esse for o foco principal do commit
  - `chore` para manutencao, docs operacionais, ajustes de suporte e infraestrutura quando nao houver prefixo mais especifico
- Formato obrigatorio da mensagem:
  - `<tipo>: <dominio ou area> - <porque da mudanca>`
- A mensagem deve explicar principalmente o porquê, e nao apenas listar o que foi alterado.
- Exemplo de estrutura aceita:
  - `refac: eventos views - reduzir acoplamento do modulo sem mudar as rotas`

## Fluxo de TDD

Quando fizer sentido, usar o ciclo de TDD descrito no modo de trabalho e detalhar os testes conforme as convencoes de teste abaixo.

## Formato de spec

Antes de implementar uma tarefa, definir uma spec curta com:

- objetivo
- contexto atual
- entrada
- saida esperada
- restricoes ou regras
- impacto em modulos, interfaces, configuracoes, armazenamento de dados e integracoes, se houver
- casos principais
- casos de borda relevantes
- criterio de aceite

A spec nao precisa ser formal, mas precisa ser suficiente para orientar implementacao e testes.

## Criterio de pronto

Uma tarefa so deve ser considerada pronta quando:

- os testes relevantes estiverem passando ou atualizados de forma coerente
- o comportamento estiver de acordo com a spec combinada
- o fluxo manual principal afetado tiver sido revisado
- ajustes de configuracao, estrutura de dados ou compatibilidade tiverem sido tratados quando necessario
- a mudanca nao quebrar fluxos existentes essenciais do sistema
- a implementacao mantiver a simplicidade esperada do projeto

## Pipeline desejado para features

Para features, usar o modo de trabalho como fluxo principal e dar atencao especial aos pontos afetados na arquitetura atual, nos dados e nas integracoes relacionadas.

## Convencoes de teste

- Priorizar testes pequenos, legiveis e focados.
- Cobrir comportamento principal antes de detalhes de implementacao.
- Testar regras de negocio e fluxos criticos quando forem afetados.
- Usar mock para integracoes externas e cenarios nao deterministicos.
- Reaproveitar a base de testes e os padroes ja existentes no projeto, salvo decisao explicita de evolucao.
- Sempre que possivel, validar regressao para bugs corrigidos.

## Decisoes em aberto

Estas decisoes ainda podem ser esclarecidas ao longo da evolucao:

- consolidar a estrategia de testes e as ferramentas principais do projeto
- definir o formato declarativo principal para perfis, modulos e eventual estado local
- decidir como representar dependencias entre modulos sem complexidade desnecessaria
- definir quais regras de negocio dependem de integracoes externas
- decidir o quanto da experiencia sera nao interativa por padrao e o que permanecera opcionalmente interativo
- revisar criterios de elegibilidade, validacao e bloqueio nos fluxos principais
- revisar quais campos, entradas ou parametros devem ser obrigatorios
- decidir onde concentrar regras mais complexas entre camadas e modulos do sistema
- priorizar melhorias tecnicas nas areas mais sensiveis da aplicacao

## Como validar mudancas

A validacao deve seguir o modo de trabalho e o criterio de pronto, combinando testes automatizados e revisao manual proporcional ao impacto da mudanca.
