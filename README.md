# Painel Ambas Marcam

Aplicação web responsiva para comparar até três partidas e calcular, de forma transparente:
- probabilidade de BTTS via Poisson usando ataque/defesa casa-fora com shrinkage à média por equipe configurável (padrão 1,35, parâmetro manual, não média automática observada da liga);
- frequência histórica média dos jogos recentes de cada equipe;
- frequência dos confrontos diretos anteriores disponíveis no calendário consultado;
- estimativa composta ponderada, odd justa, remoção de margem (quando Sim e Não estão preenchidas), EV e Kelly 1/4 como referência matemática.

## Dados e automatização
- Agenda diária e cache com 998 clubes/seleções em 36 competições são atualizados pelo GitHub Actions diariamente às 02h10 BRT. Ao escolher outra data/competição, a página consulta o feed ao vivo; filtros de texto permitem localizar partidas já carregadas.
- Busca personalizada de mandante e visitante usa o cache de equipes publicado, carrega os jogos anteriores e permite analisar um confronto solicitado sem afirmar que ele está oficialmente agendado. Para confrontos personalizados, data sem horário permanece sem horário confirmado.
- Abrange ligas sul-americanas e norte-americanas disponíveis no feed, divisões indicadas (Holanda 2, Itália B, França 2), Bélgica, Noruega, Arábia Saudita, Turquia e competições de seleções. A lista de ligas deve ser entendida como cobertura oferecida pela ESPN, não certificação oficial de calendário completo.
- Fonte automática desta versão: feed público ESPN (calendário, status e partidas concluídas por equipe). A fonte é identificada na interface e não é apresentada como fonte oficial da competição.
- Cálculos e seleções são feitos no navegador. Os dados dos três jogos ficam no `localStorage` do dispositivo; o botão Exportar baixa JSON. A persistência não sincroniza entre aparelhos.
- Odds: inserir manualmente após consulta direta à BetWinner, com a hora de captura. A casa bloqueou a leitura automatizada neste ambiente por DNS/região; o painel não finge obter preços.
- xG, escalações, lesões, viagens, árbitro e tendências oficiais da liga não são inventados; ficam sem dado até fonte integrada e verificada.

## Rodar localmente
Abra `index.html` com conexão à internet. Para ambiente local servido por HTTP, use um servidor estático qualquer. Não há dependências externas além das APIs públicas ESPN.

## Limites metodológicos
As três rotas não são independentes em sentido estatístico forte: forma e H2H podem se sobrepor; Poisson é uma aproximação que assume independência de gols. A frequência histórica não é probabilidade calibrada. A classificação baixa/média/alta é um rótulo operacional explícito, não modelo validado. EV e Kelly dependem da probabilidade calculada e de odds corretas — não são sugestão de aposta.
