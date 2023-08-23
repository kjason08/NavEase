const grid = document.getElementById('grid');
const startButton = document.getElementById('startButton');
const resetButton = document.getElementById('resetButton');

let cells = [];
let startCell = null;
let targetCell = null;

const ROWS = 10;
const COLS = 10;

let isSettingStart = false;
let isSettingTarget = false;

function initializeGrid() {
    for (let i = 0; i < ROWS; i++) {
        for (let j = 0; j < COLS; j++) {
            const cell = document.createElement('div');
            cell.className = 'grid-cell';
            cell.dataset.row = i;
            cell.dataset.col = j;
            cell.addEventListener('click', handleCellClick); // Event listener 추가
            grid.appendChild(cell);
            cells.push(cell);
        }
    }
}

function handleCellClick(event) {
    const cell = event.target;
    console.log(isSettingStart)
    console.log(isSettingTarget)

    if (isSettingStart) {
        if (startCell) startCell.classList.remove('start');
        cell.classList.add('start');
        startCell = cell;
    } else if (isSettingTarget) {
        if (targetCell) targetCell.classList.remove('target');
        cell.classList.add('target');
        targetCell = cell;
    } else {
        cell.classList.toggle('obstacle');
    }
}

function heuristic(cellA, cellB) {
    const rowDiff = Math.abs(cellA.dataset.row - cellB.dataset.row);
    const colDiff = Math.abs(cellA.dataset.col - cellB.dataset.col);
    return rowDiff + colDiff;
}

function findPath() {
    if (!startCell || !targetCell) {
        alert("Please select both start and target cells.");
        return;
    }

    const openSet = [startCell];
    const cameFrom = {};
    const gScore = {};
    const fScore = {};

    for (const cell of cells) {
        gScore[cell.id] = Infinity;
        fScore[cell.id] = Infinity;
    }

    gScore[startCell.id] = 0;
    fScore[startCell.id] = heuristic(startCell, targetCell);

    while (openSet.length > 0) {
        let current = openSet[0];
        for (const cell of openSet) {
            if (fScore[cell.id] < fScore[current.id]) {
                current = cell;
            }
        }

        if (current === targetCell) {
            reconstructPath(cameFrom, current);
            return;
        }

        openSet.splice(openSet.indexOf(current), 1);

        for (const neighbor of getNeighbors(current)) {
            const tentativeGScore = gScore[current.id] + 1;
            if (tentativeGScore < gScore[neighbor.id]) {
                cameFrom[neighbor.id] = current;
                gScore[neighbor.id] = tentativeGScore;
                fScore[neighbor.id] = gScore[neighbor.id] + heuristic(neighbor, targetCell);
                if (!openSet.includes(neighbor)) {
                    openSet.push(neighbor);
                }
            }
        }
    }

    alert("No path found.");
}

function getNeighbors(cell) {
    const row = parseInt(cell.dataset.row);
    const col = parseInt(cell.dataset.col);
    const neighbors = [];

    if (row > 0) neighbors.push(cells[(row - 1) * COLS + col]);
    if (row < ROWS - 1) neighbors.push(cells[(row + 1) * COLS + col]);
    if (col > 0) neighbors.push(cells[row * COLS + col - 1]);
    if (col < COLS - 1) neighbors.push(cells[row * COLS + col + 1]);

    return neighbors.filter(neighbor => !neighbor.classList.contains('obstacle'));
}

function reconstructPath(cameFrom, current) {
    const path = [current];
    while (cameFrom[current.id]) {
        current = cameFrom[current.id];
        path.unshift(current);
    }

    for (const cell of path) {
        if (!cell.classList.contains('start') && !cell.classList.contains('target')) {
            cell.classList.add('path');
        }
    }
}

function resetGrid() {
    for (const cell of cells) {
        cell.classList.remove('start', 'target', 'obstacle', 'path');
    }
    startCell = null;
    targetCell = null;
}

startButton.addEventListener('click', findPath);
resetButton.addEventListener('click', resetGrid);

grid.addEventListener('mousedown', () => {
    grid.addEventListener('mouseover', handleCellClick);
});

document.addEventListener('mouseup', () => {
    grid.removeEventListener('mouseover', handleCellClick);
});

initializeGrid();
