import VendingMachine from './automaton.js';
import { animateMoney, animateCandy, animateChange, updateMessage } from './animation.js';

const vm = new VendingMachine();
const screenBalance = document.querySelector('.screen .balance');
const candyButtons = document.querySelectorAll('.candy-btn');
const historyList = document.querySelector('.history-list');
const changeButton = document.querySelector('.change-btn');
let lastPurchaseChange = 0;
let changeAvailable = false;

const stock = {
    A: 6,
    B: 6,
    C: 6
};

function initializeShelves() {
    document.querySelectorAll('.candy-slot').forEach(slot => {
        const candy = slot.dataset.candy;
        const img = document.createElement('img');
        img.src = `assets/images/candy${candy}.png`;
        img.onerror = () => {
            img.replaceWith(document.createTextNode(candy));
        };
        slot.appendChild(img);
    });
}

function updateUI() {
    const balance = vm.getCurrentState();
    screenBalance.textContent = `Saldo: R$${balance},00`;

    if (balance === 0) {
        if (changeAvailable) {
            updateMessage(`Troco disponível: R$${lastPurchaseChange},00!`);
            changeButton.classList.add('visible'); // Mostra o botão
        } else {
            updateMessage('Insira Dinheiro!');
            changeButton.classList.remove('visible'); // Esconde o botão
        }
    } else if (balance === 10) {
        updateMessage('Limite máximo de R$10,00 atingido!');
        changeButton.classList.remove('visible'); // Esconde o botão
    } else if (balance < 6) {
        updateMessage('Insira mais dinheiro!');
        changeButton.classList.remove('visible'); // Esconde o botão
    } else if (balance >= 6 && balance < 7) {
        updateMessage('Você pode comprar o Doce A!');
        changeButton.classList.remove('visible'); // Esconde o botão
    } else if (balance >= 7 && balance < 8) {
        updateMessage('Você pode comprar o Doce A ou B!');
        changeButton.classList.remove('visible'); // Esconde o botão
    } else {
        updateMessage('Você pode comprar qualquer Doce!');
        changeButton.classList.remove('visible'); // Esconde o botão
    }

    candyButtons.forEach(btn => {
        const candy = btn.dataset.candy;
        btn.disabled = !vm.canBuy(candy) || stock[candy] === 0;
    });

    changeButton.disabled = balance !== 0 || !changeAvailable;
}

function addToHistory(candy, change, action = 'compra') {
    const li = document.createElement('li');
    if (action === 'compra') {
        li.textContent = `Doce ${candy} - Troco: R$${change},00`;
    } else if (action === 'troco') {
        li.textContent = `Troco Retirado: R$${change},00`;
    } else if (action === 'reset') {
        li.textContent = 'Máquina Resetada: Estoque Reabastecido';
    }
    historyList.prepend(li);
    if (historyList.children.length > 5) {
        historyList.removeChild(historyList.lastChild);
    }
}

function checkStockAndReset() {
    const totalStock = stock.A + stock.B + stock.C;
    if (totalStock === 0) {
        stock.A = 6;
        stock.B = 6;
        stock.C = 6;
        initializeShelves();
        addToHistory(null, 0, 'reset');
    }
}

document.querySelectorAll('.money-slot button').forEach(button => {
    button.addEventListener('click', () => {
        const amount = parseInt(button.dataset.value);
        const currentState = vm.getCurrentState();
        const newState = vm.insertMoney(amount);
        if (newState !== currentState) {
            console.log(`Inserindo R$${amount}`);
            animateMoney(amount);
        } else {
            console.log(`Dinheiro não aceito: Limite de R$10,00 atingido`);
        }
        updateUI();
    });
});

candyButtons.forEach(button => {
    button.addEventListener('click', () => {
        const candy = button.dataset.candy;
        if (vm.canBuy(candy) && stock[candy] > 0) {
            const result = vm.dispenseCandy(candy);
            stock[candy]--;
            const shelf = document.querySelector(`.shelf[data-candy="${candy}"]`);
            const slots = shelf.querySelectorAll('.candy-slot');
            for (let i = 0; i < slots.length; i++) {
                if (slots[i].children.length > 0) {
                    slots[i].innerHTML = '';
                    break;
                }
            }
            console.log(`Doce ${candy} dispensado, troco: R$${result.change}`);
            lastPurchaseChange = result.change;
            changeAvailable = result.change > 0;
            animateCandy(candy);
            setTimeout(() => {
                if (result.change > 0) {
                    animateChange(result.change);
                }
                setTimeout(() => {
                    addToHistory(candy, result.change, 'compra');
                    checkStockAndReset();
                    updateUI();
                }, result.change > 0 ? 1000 : 0);
            }, 1000);
        }
    });
});

changeButton.addEventListener('click', () => {
    if (changeAvailable && lastPurchaseChange > 0) {
        animateChange(lastPurchaseChange);
        setTimeout(() => {
            addToHistory(null, lastPurchaseChange, 'troco');
            lastPurchaseChange = 0;
            changeAvailable = false;
            updateUI();
        }, 1000);
    }
});

initializeShelves();
updateUI();