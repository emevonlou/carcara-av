# Arquitetura do CarcaráAV

## Visão geral

O CarcaráAV será desenvolvido com uma arquitetura modular e organizada em camadas.

Cada camada terá uma responsabilidade específica, reduzindo o acoplamento entre os componentes e facilitando testes, manutenção e expansão.

A arquitetura foi pensada para permitir a inclusão futura de novos mecanismos de detecção sem a necessidade de reestruturar todo o sistema.

---

## Fluxo geral

```text
                Usuário
                   │
                   ▼
              Interface CLI
                   │
                   ▼
          Motor de Orquestração
                   │
        ┌──────────┴──────────┐
        ▼                     ▼
  Coleta de Dados      Banco de Assinaturas
        │                     │
        └──────────┬──────────┘
                   ▼
          Motor de Detecção
                   │
        ┌──────────┼──────────┐
        ▼          ▼          ▼
     Hashes   Heurística    Regras
                   │
                   ▼
           Classificação
                   │
                   ▼
        Logs • Quarentena • Relatórios
```

---

## Camadas

### 1. Interface

Responsável pela comunicação com o usuário.

Na primeira fase, o CarcaráAV utilizará uma interface de linha de comando.

Responsabilidades:

- receber caminhos de arquivos e diretórios;
- iniciar análises;
- exibir resultados;
- solicitar confirmação antes de ações sensíveis;
- apresentar explicações sobre as detecções.

Diretório previsto:

```text
src/carcara/interface/
```

---

### 2. Motor de Orquestração

Responsável por coordenar todo o fluxo de análise.

Ele receberá a solicitação da interface, encaminhará os arquivos para os módulos adequados e reunirá os resultados.

Responsabilidades:

- validar entradas;
- iniciar o scanner;
- coordenar os mecanismos de detecção;
- reunir evidências;
- encaminhar resultados para classificação;
- acionar logs, relatórios e quarentena.

Diretório previsto:

```text
src/carcara/orquestracao/
```

---

### 3. Coleta de Dados

Responsável por extrair informações dos arquivos analisados.

Responsabilidades:

- localizar arquivos;
- obter tamanho e extensão;
- identificar permissões;
- coletar metadados;
- reconhecer o tipo real do arquivo;
- preparar os dados para os motores de detecção.

Diretório previsto:

```text
src/carcara/scanner/
```

---

### 4. Banco de Assinaturas

Responsável por armazenar e consultar indicadores conhecidos de ameaça.

Inicialmente, poderá conter hashes associados a arquivos maliciosos conhecidos.

No futuro, poderá incluir:

- assinaturas de conteúdo;
- padrões binários;
- regras de detecção;
- indicadores de comprometimento;
- fontes externas confiáveis.

Diretório previsto:

```text
src/carcara/deteccao/
```

---

### 5. Motor de Detecção

Responsável por analisar as informações coletadas e produzir evidências.

O motor será composto por diferentes mecanismos independentes.

#### Hashes

Calcula hashes criptográficos dos arquivos e compara os valores com indicadores conhecidos.

Algoritmo inicial:

- SHA-256

Diretório:

```text
src/carcara/hashes/
```

#### Heurística

Analisa características suspeitas sem depender exclusivamente de uma assinatura conhecida.

Exemplos futuros:

- extensões incompatíveis com o conteúdo;
- nomes enganosos;
- permissões incomuns;
- arquivos executáveis em locais sensíveis;
- padrões associados a persistência;
- comportamento potencialmente perigoso.

Diretório:

```text
src/carcara/heuristica/
```

#### Regras

Permite aplicar regras estruturadas de detecção.

Esse mecanismo poderá futuramente utilizar regras próprias ou integrações com tecnologias específicas.

Diretório previsto:

```text
src/carcara/regras/
```

---

### 6. Classificação

Responsável por interpretar as evidências produzidas pelos mecanismos de detecção.

Cada evidência poderá contribuir para uma pontuação de risco.

Classificações iniciais previstas:

- limpo;
- desconhecido;
- suspeito;
- malicioso.

A classificação deverá informar:

- resultado;
- pontuação;
- evidências encontradas;
- mecanismos responsáveis pela detecção;
- recomendação de ação.

Diretório previsto:

```text
src/carcara/classificacao/
```

---

### 7. Resposta

Responsável pelas ações executadas após a classificação.

#### Logs

Registra as operações realizadas pelo sistema.

Diretório:

```text
src/carcara/logs/
```

#### Quarentena

Isola arquivos suspeitos ou maliciosos de maneira controlada.

Nenhum arquivo deverá ser movido ou alterado sem confirmação explícita do usuário, salvo quando uma política previamente configurada determinar o contrário.

Diretório:

```text
src/carcara/quarentena/
```

#### Relatórios

Produz relatórios compreensíveis sobre a análise.

Os relatórios deverão conter:

- arquivo analisado;
- hash;
- classificação;
- pontuação;
- evidências;
- data e horário;
- ação executada.

Diretório previsto:

```text
src/carcara/relatorios/
```

---

## Modelo de detecção explicável

O CarcaráAV não deverá apresentar apenas uma mensagem genérica de ameaça.

Sempre que possível, o sistema explicará por que um arquivo recebeu determinada classificação.

Exemplo:

```text
Classificação: suspeito
Pontuação: 72/100

Evidências:
- extensão incompatível com o tipo real do arquivo;
- permissão de execução ativa;
- hash não encontrado no banco local;
- arquivo localizado em diretório sensível.
```

Esse modelo permite auditoria e ajuda o usuário a compreender as decisões do sistema.

---

## Princípios arquiteturais

A implementação deverá seguir os seguintes princípios:

- modularidade;
- baixo acoplamento;
- alta coesão;
- separação de responsabilidades;
- código legível;
- detecção explicável;
- segurança por padrão;
- confirmação antes de ações destrutivas;
- facilidade para testes;
- facilidade para expansão.

---

## Estado atual

A arquitetura representa o planejamento inicial do CarcaráAV.

Ela poderá evoluir conforme o projeto for implementado, desde que as alterações sejam documentadas e mantenham os princípios de transparência e modularidade.
