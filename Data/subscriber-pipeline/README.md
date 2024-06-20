# Subscriber Pipeline Project

## Introdução

Este projeto tem como objetivo transformar uma base de dados desordenada de assinantes cancelados em uma fonte de dados limpa e pronta para análise. O pipeline foi desenvolvido para rodar automaticamente com o mínimo de intervenção humana.

## Estrutura do Projeto

```
/home/jampamatos/workspace/codecademy/Data/subscriber-pipeline/
│
├── dev/
│ ├── cademycode.db
│ ├── clean_cademycode.db
│ ├──final_output.csv
├── logs/
│ ├── data_pipeline.log
│ ├── changelog.txt
│
├── prod/
│ ├── (arquivos movidos para produção)
├── run_pipeline.sh
└── main.py
```


## Descrição dos Arquivos

- **`dev/cademycode.db`**: Banco de dados original com os dados desordenados.
- **`dev/clean_cademycode.db`**: Banco de dados limpo gerado pelo pipeline.
- **`logs/data_pipeline.log`**: Arquivo de log contendo informações sobre a execução do pipeline.
- **`logs/changelog.txt`**: Changelog contendo informações sobre as atualizações realizadas.
- **`prod/`**: Diretório onde os arquivos atualizados são movidos após a execução bem-sucedida do pipeline.
- **`dev/final_output.csv`**: Arquivo CSV final com os dados limpos e prontos para análise.
- **`run_pipeline.sh`**: Script Bash para executar o pipeline e mover os arquivos para o diretório de produção.
- **`main.py`**: Script Python que contém o código do pipeline de dados.

## Instruções para Executar o Pipeline

1. **Configurar o Alias (Opcional)**: 
Você pode configurar um alias para facilitar a execução do pipeline:

```bash
alias run_pipeline="/path/to/run_pipeline.sh"
```

2. **Executar o Pipeline:**
No diretório do projeto, execute o script Bash:

```bash
./run_pipeline.sh
```

Ou, se você configurou o alias:

```bash
run_pipeline
```

## Controle de Versão e Changelog

O changelog.txt contém detalhes sobre cada atualização realizada no banco de dados, incluindo:

- Número da versão
- Número de novas linhas adicionadas
- Contagem de dados ausentes

A versão atual é verificada antes e depois da execução do pipeline para determinar se uma atualização foi realizada.

## Logs de Erros

Todos os erros encontrados durante a execução do pipeline são registrados em `log/data_pipeline.log`. Verifique este arquivo para obter detalhes sobre quaisquer problemas que ocorreram.