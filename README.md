# DATATHON

# 🧠 Inteligência Artificial no Recrutamento

Este projeto foi desenvolvido para o **Datathon de Data Analytics**, com foco na aplicação de **Inteligência Artificial** para otimizar processos de **Recrutamento e Seleção**, utilizando como base um estudo de caso da empresa **Decision** – especializada em serviços de bodyshop no setor de TI.

## 📌 Desafio

A empresa enfrenta desafios como:

- Falta de padronização nas entrevistas;
- Dificuldade para identificar o real engajamento dos candidatos;
- Processo demorado para encontrar o match ideal entre talento e vaga.

## 💡 Proposta da Solução

Nossa solução utiliza **Embeddings** e técnicas de NLP para:

1. **Analisar perfis de candidatos** com base em dados técnicos e comportamentais;
2. **Identificar atributos comuns** entre candidatos e vagas;
3. **Classificar candidatos** de acordo com o nível de compatibilidade com a vaga (match candidato + vaga);

## 🔍 Etapas do Projeto

1. **Coleta e limpeza dos dados** da Decision;
2. **Geração de embeddings** para candidatos e vagas;
3. **Cálculo de similaridade** usando distância vetorial;
4. **Criação de modelo de score de compatibilidade**;
5. **Deploy em ambiente interativo com Streamlit**.


## Link do Streamlit

https://datathondatanalytics.streamlit.app

## 📁 Estrutura de Pastas e Arquivos

### Pasta df_applicants:
  Contém os dados dos candidatos
  
│   ├── df_applicants.pkl                # Dataset bruto original com os candidatos

│   ├── df_final_candidatos_part1.pkl   # Parte 1 dos candidatos com embeddings pré-processados

│   └── df_final_candidatos_part2.pkl   # Parte 2 dos candidatos com embeddings pré-processados

### Pasta df_vagas:
  Contém os dados das vagas

│   ├── df_vagas.pkl                    # Dataset bruto original com as vagas

│   ├── df_final_vagas_part1.pkl       # Parte 1 das vagas com embeddings pré-processados

│   └── df_final_vagas_part2.pkl       # Parte 2 das vagas com embeddings pré-processados

### Pasta images:
  Imagens utilizadas na aplicação

│   └── logo_decision.png              # Logotipo utilizado no Streamlit

### Arquivos principais:

├── datathon.ipynb                       # Notebook com a análise exploratória e pré-processamento dos dados

├── app.py                               # Código principal da aplicação Streamlit para recomendação
