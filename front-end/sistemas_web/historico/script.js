/* ════════════════════════════════════════════════════════════
   DADOS MOCK - HISTÓRICO DE ESTUDOS
   ════════════════════════════════════════════════════════════ */

const mockHistoryData = [
  {
    date: '2026-06-10',
    cardsStudied: 15,
    correct: 12,
    incorrect: 3,
    duration: '12 min'
  },
  {
    date: '2026-06-09',
    cardsStudied: 20,
    correct: 16,
    incorrect: 4,
    duration: '18 min'
  },
  {
    date: '2026-06-08',
    cardsStudied: 10,
    correct: 9,
    incorrect: 1,
    duration: '8 min'
  },
  {
    date: '2026-06-07',
    cardsStudied: 25,
    correct: 18,
    incorrect: 7,
    duration: '22 min'
  },
  {
    date: '2026-06-06',
    cardsStudied: 12,
    correct: 10,
    incorrect: 2,
    duration: '10 min'
  },
  {
    date: '2026-06-05',
    cardsStudied: 18,
    correct: 14,
    incorrect: 4,
    duration: '15 min'
  }
];

/* ════════════════════════════════════════════════════════════
   ELEMENTO DO DOM
   ════════════════════════════════════════════════════════════ */

const historyTableBody = document.getElementById('historyTableBody');
const emptyState = document.getElementById('emptyState');
const themeToggle = document.getElementById('themeToggle');
const searchInput = document.getElementById('searchInput');
const filterSelect = document.getElementById('filterSelect');
const clearHistoryBtn = document.getElementById('clearHistoryBtn');

const totalSessionsEl = document.getElementById('total-sessions');
const totalCardsEl = document.getElementById('total-cards-studied');
const totalCorrectEl = document.getElementById('total-correct');
const totalIncorrectEl = document.getElementById('total-incorrect');

/* ════════════════════════════════════════════════════════════
   TEMA - DARK / LIGHT
   ════════════════════════════════════════════════════════════ */

function initTheme() {
  const savedTheme = localStorage.getItem('theme') || 'dark';
  applyTheme(savedTheme);
  updateThemeToggleText(savedTheme);
}

function applyTheme(theme) {
  if (theme === 'white') {
    document.documentElement.setAttribute('data-theme', 'white');
    localStorage.setItem('theme', 'white');
  } else {
    document.documentElement.removeAttribute('data-theme');
    localStorage.setItem('theme', 'dark');
  }
}

function updateThemeToggleText(theme) {
  themeToggle.textContent = theme === 'white' ? '🌙 Dark' : '☀️ White';
}

function toggleTheme() {
  const currentTheme = localStorage.getItem('theme') || 'dark';
  const newTheme = currentTheme === 'white' ? 'dark' : 'white';
  applyTheme(newTheme);
  updateThemeToggleText(newTheme);
}

/* ════════════════════════════════════════════════════════════
   CALCULAR TAXA DE ACERTO
   ════════════════════════════════════════════════════════════ */

function calculateAccuracy(correct, total) {
  if (total === 0) return 0;
  return Math.round((correct / total) * 100);
}

/* ════════════════════════════════════════════════════════════
   FORMATAR DATA
   ════════════════════════════════════════════════════════════ */

function formatDate(dateString) {
  const date = new Date(dateString);
  const day = String(date.getDate()).padStart(2, '0');
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const year = date.getFullYear();
  
  const options = { weekday: 'short' };
  const dayName = date.toLocaleDateString('pt-BR', options);
  
  return `${day}/${month}/${year} (${dayName})`;
}

/* ════════════════════════════════════════════════════════════
   RENDERIZAR TABELA DE HISTÓRICO
   ════════════════════════════════════════════════════════════ */

function renderHistoryTable(data) {
  historyTableBody.innerHTML = '';

  if (data.length === 0) {
    emptyState.style.display = 'block';
    return;
  }

  emptyState.style.display = 'none';

  data.forEach((entry) => {
    const accuracy = calculateAccuracy(entry.correct, entry.cardsStudied);
    const accuracyBadgeClass = accuracy >= 70 ? '' : 'low';

    const row = document.createElement('tr');
    row.innerHTML = `
      <td class="cell-date">${formatDate(entry.date)}</td>
      <td>${entry.cardsStudied}</td>
      <td class="cell-success">${entry.correct}</td>
      <td class="cell-error">${entry.incorrect}</td>
      <td>
        <span class="accuracy-badge ${accuracyBadgeClass}">
          ${accuracy}%
        </span>
      </td>
      <td>${entry.duration}</td>
    `;

    historyTableBody.appendChild(row);
  });
}

/* ════════════════════════════════════════════════════════════
   ATUALIZAR RESUMO DE ESTATÍSTICAS
   ════════════════════════════════════════════════════════════ */

function updateStats(data) {
  let totalSessions = data.length;
  let totalCards = 0;
  let totalCorrect = 0;
  let totalIncorrect = 0;

  data.forEach((entry) => {
    totalCards += entry.cardsStudied;
    totalCorrect += entry.correct;
    totalIncorrect += entry.incorrect;
  });

  totalSessionsEl.textContent = totalSessions;
  totalCardsEl.textContent = totalCards;
  totalCorrectEl.textContent = totalCorrect;
  totalIncorrectEl.textContent = totalIncorrect;
}

/* ════════════════════════════════════════════════════════════
   FILTRAR E BUSCAR HISTÓRICO
   ════════════════════════════════════════════════════════════ */

function filterHistory() {
  let filteredData = [...mockHistoryData];

  // Busca por texto (data ou qualquer campo)
  const searchTerm = searchInput.value.toLowerCase();
  if (searchTerm) {
    filteredData = filteredData.filter((entry) => {
      const dateFormatted = formatDate(entry.date).toLowerCase();
      return dateFormatted.includes(searchTerm);
    });
  }

  // Filtro por taxa de acerto
  const filterValue = filterSelect.value;
  if (filterValue === 'high') {
    filteredData = filteredData.filter((entry) => {
      const accuracy = calculateAccuracy(entry.correct, entry.cardsStudied);
      return accuracy >= 70;
    });
  } else if (filterValue === 'low') {
    filteredData = filteredData.filter((entry) => {
      const accuracy = calculateAccuracy(entry.correct, entry.cardsStudied);
      return accuracy < 70;
    });
  }

  renderHistoryTable(filteredData);
}

/* ════════════════════════════════════════════════════════════
   LIMPAR HISTÓRICO
   ════════════════════════════════════════════════════════════ */

function clearHistory() {
  if (confirm('Tem certeza que deseja limpar todo o histórico? Esta ação não pode ser desfeita.')) {
    mockHistoryData.length = 0;
    renderHistoryTable(mockHistoryData);
    updateStats(mockHistoryData);
    searchInput.value = '';
    filterSelect.value = '';
  }
}

/* ════════════════════════════════════════════════════════════
   INICIALIZAR
   ════════════════════════════════════════════════════════════ */

function init() {
  // Tema
  initTheme();

  // Renderizar dados
  renderHistoryTable(mockHistoryData);
  updateStats(mockHistoryData);

  // Event Listeners
  themeToggle.addEventListener('click', toggleTheme);
  searchInput.addEventListener('input', filterHistory);
  filterSelect.addEventListener('change', filterHistory);
  clearHistoryBtn.addEventListener('click', clearHistory);
}

// Iniciar quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', init);
