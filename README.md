# Painel Ambas Marcam

Aplicação web responsiva para comparar até três partidas e calcular, de forma transparente:
- probabilidade de BTTS via Poisson usando ataque/defesa casa-fora com shrinkage à média da liga;
- frequência histórica média dos jogos recentes de cada equipe;
- frequência dos confrontos diretos anteriores disponíveis no calendário consultado;
- estimativa composta ponderada, odd justa, remoção de margem (quando Sim e Não estão preenchidas), EV e Kelly 1/4 como referência matemática.

## Dados e automatização
- Agenda diária e resultados recentes são carregados ao abrir/atualizar a página, conforme competição e data escolhidas.
- Fonte automática desta versão: feed público ESPN (calendário, status e partidas concluídas por equipe). A fonte é identificada na interface e não é apresentada como fonte oficial da competição.
- Cálculos e seleções são feitos no navegador. Os dados dos três jogos ficam no `localStorage` do dispositivo; o botão Exportar baixa JSON. A persistência não sincroniza entre aparelhos.
- Odds: inserir manualmente após consulta direta à BetWinner, com a hora de captura. A casa bloqueou a leitura automatizada neste ambiente por DNS/região; o painel não finge obter preços.
- xG, escalações, lesões, viagens, árbitro e tendências oficiais da liga não são inventados; ficam sem dado até fonte integrada e verificada.

## Rodar localmente
Abra `index.html` com conexão à internet. Para ambiente local servido por HTTP, use um servidor estático qualquer. Não há dependências externas além das APIs públicas ESPN.

## Limites metodológicos
As três rotas não são independentes em sentido estatístico forte: forma e H2H podem se sobrepor; Poisson é uma aproximação que assume independência de gols. A frequência histórica não é probabilidade calibrada. A classificação baixa/média/alta é um rótulo operacional explícito, não modelo validado. EV e Kelly dependem da probabilidade calculada e de odds corretas — não são sugestão de aposta.
