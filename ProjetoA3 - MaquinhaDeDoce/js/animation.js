export function animateMoney(amount) {
    const slot = document.querySelector('.slot-hole');
    const money = document.createElement('img');
    money.src = `assets/images/note${amount}.png`;
    money.classList.add('money-animation');

    money.onerror = () => {
        console.log(`Imagem note${amount}.png não encontrada, usando texto como fallback`);
        const fallback = document.createElement('div');
        fallback.textContent = `R$${amount}`;
        fallback.classList.add('money-animation');
        slot.appendChild(fallback);
        setTimeout(() => fallback.remove(), 1000);
    };

    slot.appendChild(money);
    setTimeout(() => money.remove(), 1000);
}

export function animateCandy(candy) {
    const tray = document.querySelector('.tray');
    const shelf = document.querySelector(`.shelf[data-candy="${candy}"]`);
    const candyImg = document.createElement('img');
    candyImg.src = `assets/images/candy${candy}.png`;
    candyImg.classList.add('candy-animation');

    candyImg.onerror = () => {
        console.log(`Imagem candy${candy}.png não encontrada, usando texto como fallback`);
        const fallback = document.createElement('div');
        fallback.textContent = `Doce ${candy}`;
        fallback.classList.add('candy-animation');
        tray.appendChild(fallback);
        tray.classList.add('active');
        setTimeout(() => {
            tray.classList.remove('active');
            fallback.remove();
        }, 2000);
    };

    tray.appendChild(candyImg);
    tray.classList.add('active');
    setTimeout(() => {
        tray.classList.remove('active');
        candyImg.remove();
    }, 2000);
}

export function animateChange(amount) {
    if (amount > 0) {
        const tray = document.querySelector('.tray');
        const change = document.createElement('div');
        change.textContent = `Troco R$${amount}`;
        change.classList.add('change-animation');
        tray.appendChild(change);
        setTimeout(() => change.remove(), 1000);
    }
}

export function updateMessage(message) {
    const messageElement = document.querySelector('.screen .message');
    messageElement.textContent = message;
}