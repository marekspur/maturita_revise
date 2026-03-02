
// Hlavní logika hry Piškvorky
const poleEl = document.getElementById('board');
const obtiznostEl = document.getElementById('difficulty');

// Při načtení stránky nastavíme uloženou obtížnost
const ulozenaObtiznost = localStorage.getItem('difficulty') || 'easy';
obtiznostEl.value = ulozenaObtiznost;

// Při změně volby uložíme do localStorage
obtiznostEl.addEventListener('change', () => {
  localStorage.setItem('difficulty', obtiznostEl.value);
});

const SIZE = 5;
const WIN_LENGTH = 3;

// Stav hry
let board = Array(SIZE).fill(null).map(() => Array(SIZE).fill(''));
let player = 'X';
let ai = 'O';
let gameOver = false;

// Vytvoření vizuálu
function renderBoard() {
  poleEl.innerHTML = '';
  for (let i = 0; i < SIZE; i++) {
    for (let j = 0; j < SIZE; j++) {
      const cell = document.createElement('div');
      cell.classList.add('cell');
      cell.textContent = board[i][j];
      cell.addEventListener('click', () => makeMove(i, j));
      poleEl.appendChild(cell);
    }
  }
}

// Tah hráče
function makeMove(row, col) {
  if (board[row][col] !== '' || gameOver) return;
  board[row][col] = player;
  if (checkWin(player)) return endGame('Vyhrál jsi!');
  if (isDraw()) return endGame('Remíza!');
  aiMove();
}

// Tah AI podle obtížnosti
function aiMove() {
  const level = obtiznostEl.value;
  let move;

  if (level === 'easy') {
    move = randomMove();
  } else if (level === 'medium') {
    move = mediumMove();
  } else if (level === 'hard') {
    move = hardMove();
  }

  if (move) {
    board[move[0]][move[1]] = ai;
    if (checkWin(ai)) return endGame('AI vyhrála!');
    if (isDraw()) return endGame('Remíza!');
    renderBoard();
  }
}

// Jednoduché tahy AI (náhodný)
function randomMove() {
  const empty = [];
  for (let i = 0; i < SIZE; i++)
    for (let j = 0; j < SIZE; j++)
      if (board[i][j] === '') empty.push([i, j]);
  return empty[Math.floor(Math.random() * empty.length)];
}

// Střední AI: blokuje hráče, jinak náhodně
function mediumMove() {
  // Zkontroluje, zda může hráč vyhrát příští tah a blokuje
  for (let i = 0; i < SIZE; i++) {
    for (let j = 0; j < SIZE; j++) {
      if (board[i][j] === '') {
        board[i][j] = player;
        if (checkWin(player)) {
          board[i][j] = '';
          return [i, j];
        }
        board[i][j] = '';
      }
    }
  }
  return randomMove();
}

// Těžká AI: minimax s omezením hloubky
function hardMove() {
  let bestScore = -Infinity;
  let move;
  for (let i = 0; i < SIZE; i++) {
    for (let j = 0; j < SIZE; j++) {
      if (board[i][j] === '') {
        board[i][j] = ai;
        let score = minimax(board, 2, false);
        board[i][j] = '';
        if (score > bestScore) {
          bestScore = score;
          move = [i, j];
        }
      }
    }
  }
  return move || randomMove();
}

// Minimalistický minimax (omezená hloubka)
function minimax(b, depth, isMaximizing) {
  if (checkWin(ai)) return 10;
  if (checkWin(player)) return -10;
  if (isDraw()) return 0;
  if (depth === 0) return 0;

  // Maximizing pro AI
  if (isMaximizing) {
    let maxEval = -Infinity;
    for (let i = 0; i < SIZE; i++) {
      for (let j = 0; j < SIZE; j++) {
        if (b[i][j] === '') {
          b[i][j] = ai;
          let score = minimax(b, depth - 1, false);
          b[i][j] = '';
          maxEval = Math.max(maxEval, eval);
        }
      }
    }
    return maxEval;
    // Minimizing pro hráče
  } else {
    let minEval = Infinity;
    for (let i = 0; i < SIZE; i++) {
      for (let j = 0; j < SIZE; j++) {
        if (b[i][j] === '') {
          b[i][j] = player;
          let score = minimax(b, depth - 1, true);
          b[i][j] = '';
          minEval = Math.min(minEval, score);
        }
      }
    }
    return minEval;
  }
}

// Kontrola výhry (řádky, sloupce, diagonály)
function checkWin(symbol) {
  // Řádky a sloupce
  for (let i = 0; i < SIZE; i++) {
    for (let j = 0; j <= SIZE - WIN_LENGTH; j++) {
      if (Array(WIN_LENGTH).fill(0).map((_, k) => board[i][j+k]).every(c => c === symbol)) return true;
      if (Array(WIN_LENGTH).fill(0).map((_, k) => board[j+k][i]).every(c => c === symbol)) return true;
    }
  }
  // Diagonály
  for (let i = 0; i <= SIZE - WIN_LENGTH; i++) {
    for (let j = 0; j <= SIZE - WIN_LENGTH; j++) {
      if (Array(WIN_LENGTH).fill(0).map((_, k) => board[i+k][j+k]).every(c => c === symbol)) return true;
      if (Array(WIN_LENGTH).fill(0).map((_, k) => board[i+WIN_LENGTH-1-k][j+k]).every(c => c === symbol)) return true;
    }
  }
  return false;
}

// Kontrola remízy
function isDraw() {
  return board.flat().every(cell => cell !== '');
}

function endGame(msg) {
  alert(msg);
  // Uloží aktuální obtížnost pro reload
  localStorage.setItem('difficulty', obtiznostEl.value);
  // Reset hry reloadem
  location.reload();
}

renderBoard();