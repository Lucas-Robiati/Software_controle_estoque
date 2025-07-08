# Software_controle_venda_e_estoque

> Descrição do projeto\
> Software desktop dinâmico voltado para controle de venda e estoque, ultilização de banco de dados local postgres para
> dinamização das funcionalidades, ultilizaou-se python3 com as bibliotecas psycopg2 para a manipulação do banco, TKinter
> para criação das interfaces, o sotware oferece um sistema de consulta dinamico em tempo real, assim como funcionalidades de cadastrar, remover e autualizar, produtos e clientes. Tambem é possivel registro de venda, assim como geração de relatorio de produtos vendidos no dia com data e hora registrados dinâmicamente. 

## Metodlogia Àgil Utilizada  
### Kanban
- Kanban, que significa "quadro de sinalização" em japonês, é uma abordagem visual para a gestão de projetos e processos. Ele utiliza um quadro com colunas que representam as diferentes etapas de um fluxo de trabalho, como "A fazer", "Em progresso" e "Concluído". As tarefas são representadas por cartões que são movidos pelas colunas conforme avançam no processo. 

- Visualização do trabalho: O quadro Kanban permite que todos os membros da equipe vejam o status de cada tarefa e o fluxo de trabalho como um todo. 

- Benefícios do Kanban: Maior visibilidade do fluxo de trabalho:
Permite que todos os membros da equipe tenham uma visão clara do progresso das tarefas. 

- Aumento da eficiência:
Ao otimizar o fluxo de trabalho e limitar o trabalho em progresso, o Kanban ajuda a equipe a trabalhar de forma mais eficiente e a entregar mais valor ao cliente. 
Redução de gargalos:
Ao identificar e resolver gargalos no fluxo de trabalho, o Kanban ajuda a equipe a evitar atrasos e a manter o ritmo de trabalho. 
Maior flexibilidade:

## Tabela de conclusão
- [x] Elaboração estrutural da interface - Arnaldo.
- [x] Estruturação do Banco de Dados - Lucas.
- [x] Criação das tabelas - Lucas. 
- [x] Correção de Bugs na tabela de vendas - Lucas.
- [x] Conecxão do cadastro usuário com o Banco - Milton.
- [x] Validação Regex de campos do cadastro - Milton. 
- [x] Falha de segurança, colocar validadores nos entrys - Arnaldo.
- [x] Testes finais - Lucas, Arnaldo e Milton  

## ⚙️ Pré-requisitos 
> dotenv==0.9.9 \
greenlet==3.2.3 \
numpy==2.3.1 \
psycopg2==2.9.10 \
psycopg2-binary==2.9.10 \
python-dotenv==1.1.1 \
tk==0.1.0 \
typing_extensions==4.14.0
> 

## 🔧 Build  
```bash
source .venv/bin/activate \
python3 MainInterface.py
```
