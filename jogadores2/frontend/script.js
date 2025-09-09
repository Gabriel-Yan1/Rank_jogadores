document.addEventListener('DOMContentLoaded', () => {
    const rankingList = document.getElementById('ranking-list');
    const loadingMessage = document.getElementById('loading');
    const errorMessage = document.getElementById('error');

    async function fetchRanking() {
        try {
            const response = await fetch('http://127.0.0.1:5000/api/ranking');
            if (!response.ok) {
                throw new Error('Erro ao buscar dados do ranking.');
            }
            const data = await response.json();
            displayRanking(data);
        } catch (error) {
            console.error('Erro:', error);
            errorMessage.textContent = 'Não foi possível carregar o ranking. Verifique se o servidor está rodando.';
        } finally {
            loadingMessage.style.display = 'none'; 
        }
    }

    function displayRanking(players) {
        rankingList.innerHTML = '';

        players.forEach((player, index) => {
            const listItem = document.createElement('li');
            listItem.className = 'player-item';
            if (index < 3) {
                listItem.classList.add('top-3');
            }

            listItem.innerHTML = `
                <span class="player-rank">${player.posicao}º</span>
                <span class="player-name">${player.nome}</span>
                <span class="player-level">Nível ${player.nivel}</span>
                <span class="player-score">Pontuação: ${player.pontuacao}</span>
            `;
            
            rankingList.appendChild(listItem);
        });
    }

    fetchRanking();
});