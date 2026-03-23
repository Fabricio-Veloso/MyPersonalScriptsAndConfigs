# Spec: neovim isolated verification

## Objetivo

Evoluir o modulo `neovim` para detectar dependencias basicas da configuracao, aplicar a instalacao/configuracao principal, validar a inicializacao em um ambiente isolado por diretorios temporarios e preparar uma prova de conceito de sandbox verify.

## Contexto atual

Nesta iteracao, `src/personal_setup/modules/neovim.py` ja entrega o fluxo principal planejado.

- `check()` valida `nvim`, baseline de dependencias, fonte da configuracao e acessibilidade do repo remoto
- `apply()` instala o binario principal quando possivel e materializa a configuracao por fonte local ou Git remoto
- `verify()` roda smoke verify isolado por diretorios temporarios e pode executar sandbox verify opcional
- a configuracao funcional real do usuario continua vindo do repo publico `https://github.com/Fabricio-Veloso/NvimConfig`, com suporte a sobrescrita por user settings
- o sandbox atual usa workspace temporario proprio dentro do backend e remove esse workspace ao final; dependencias instaladas no backend continuam persistentes

O principal proximo passo arquitetural, se necessario, e generalizar esse modelo de sandbox para outros modulos sem acoplar demais a base ao caso do Neovim.

## Entrada

- plataforma atual detectada pela aplicacao
- binarios disponiveis no host
- caminho local de origem da configuracao do Neovim, quando existir
- URL publica do repositorio da configuracao do Neovim
- configuracao persistida do usuario para sobrescrever a URL do repo, quando necessario
- caminho de destino da configuracao do Neovim
- resultado de execucao headless do `nvim` em diretorios temporarios isolados com smoke test

## Saida esperada

Um `CheckResult` para `check()` e `verify()` que deixe explicito:

- se o `nvim` esta instalado
- se a origem da configuracao existe
- se o repositorio remoto configurado continua publico e acessivel
- se a configuracao esperada esta presente no destino gerenciado
- quais dependencias basicas da configuracao estao faltando
- se a inicializacao isolada do Neovim passou ou falhou
- qual comando-base pode ser usado depois para um sandbox verify em Docker ou WSL

## Restricoes ou regras

- o modulo deve continuar simples e usar a mesma semantica atual de `check`, `apply` e `verify`
- `check()` deve ser leve e nao pode depender de rede, Docker ou execucao interativa
- `verify()` deve isolar o Neovim por diretorios temporarios, sem reutilizar config, data, state ou cache do host
- `verify()` deve fazer mais que abrir e fechar o binario: ele precisa pelo menos carregar `lazy` e executar `checkhealth` no ambiente isolado
- a primeira versao nao precisa descobrir automaticamente todas as dependencias de plugins; ela deve validar um baseline inicial e expor falhas da inicializacao real
- a origem da configuracao deve poder ser resolvida tanto por caminho local quanto por repositorio Git publico
- a URL do repo deve poder ser configurada via user settings, sem depender apenas de variavel de ambiente
- se uma dependencia vital conhecida estiver faltando, o modulo deve explicitar isso de forma legivel antes da aplicacao
- a primeira versao pode instalar apenas o binario principal do Neovim; dependencias extras ainda podem ficar como pre-condicoes reportadas
- os arquivos temporarios do verify isolado devem ser descartados ao final da execucao
- a prova de conceito de sandbox deve poder ser executada opcionalmente pela CLI, sem virar comportamento padrao do `verify`

## Impacto em modulos, interfaces, configuracoes, armazenamento de dados e integracoes

- `src/personal_setup/modules/neovim.py` passa a concentrar instalacao, obtencao da configuracao por fonte local ou remota e verificacao isolada
- `src/personal_setup/services/user_settings.py` passa a guardar a URL configurada do repo do Neovim
- `src/personal_setup/cli.py` e `src/personal_setup/app.py` passam a expor uma forma simples de persistir essa URL
- `src/personal_setup/services/verifier.py` e o contrato base dos modulos passam a aceitar `sandbox=True` no fluxo de verify
- `src/personal_setup/adapters/shell.py` pode precisar aceitar ambiente e diretorio de trabalho para o verify isolado
- `tests/unit/` precisara cobrir a nova semantica de `check`, `apply` e `verify`
- o design prepara o caminho para futuras estrategias de sandbox mais fortes, como Docker ou WSL, sem obrigar isso agora

## Casos principais

- `nvim` ausente e configuracao presente: `check()` pede instalacao
- `nvim` presente, configuracao ausente no destino e origem valida: `check()` pede configuracao
- a origem local esta ausente, mas o repo remoto publico responde: `check()` confirma a acessibilidade publica e permite materializar a config no `apply()`
- dependencia vital conhecida ausente, como `lua`: `check()` reporta bloqueio claro
- `apply()` instala o binario principal quando possivel e copia a configuracao para o destino gerenciado
- `verify()` sobe o Neovim headless em diretorios temporarios isolados, carrega `lazy`, executa `checkhealth` e retorna sucesso quando a inicializacao passa
- `verify --sandbox` executa tambem a prova de conceito em backend suportado, preferindo Docker e caindo para WSL no Windows quando necessario, provisionando as dependencias basicas dentro do backend antes do teste e limpando o workspace temporario ao final

## Casos de borda relevantes

- a origem da configuracao nao existe
- o repositorio remoto deixa de ser publico ou acessivel
- a origem e o destino da configuracao sao o mesmo caminho
- a execucao headless falha por erro de startup, plugin ou dependencia externa
- o instalador da plataforma retorna erro e o binario continua ausente
- a plataforma atual nao e suportada pelo modulo

## Criterio de aceite

- `check()` diferencia instalacao faltante, configuracao faltante e bloqueios de pre-condicao
- `apply()` consegue instalar `nvim` e copiar a configuracao quando as pre-condicoes basicas estao atendidas
- `apply()` consegue clonar a configuracao a partir do repositorio remoto quando nao houver fonte local valida
- `verify()` usa diretorios temporarios isolados e nao depende do estado existente em `AppData`, `HOME` ou caches anteriores
- `verify()` executa um smoke test mais forte que o bootstrap minimo, incluindo `lazy` e `checkhealth`
- o verify isolado nao deixa lixo no filesystem ao terminar
- o sandbox verify executa em diretorio temporario dedicado dentro do backend e remove esse workspace ao final
- falhas de inicializacao do Neovim aparecem no resultado de `verify()` com motivo legivel
- a URL do repo do Neovim pode ser persistida em user settings e consumida pelo modulo sem reiniciar a aplicacao em outro processo
- `verify --sandbox` funciona de forma opt-in e falha com mensagem clara quando nao houver backend suportado
- testes unitarios cobrem o comportamento principal e as bordas mais importantes da nova semantica
