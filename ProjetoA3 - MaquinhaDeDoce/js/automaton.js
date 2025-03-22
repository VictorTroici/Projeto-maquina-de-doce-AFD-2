class VendingMachine {
    constructor() {
        this.state = 0; // Estado inicial (q0)
        this.maxBalance = 10; // Limite máximo de saldo
        this.transitions = {
            0: { 1: 1, 2: 2, 5: 5 }, // q0 (R$0)
            1: { 1: 2, 2: 3, 5: 6 }, // q1 (R$1)
            2: { 1: 3, 2: 4, 5: 7 }, // q2 (R$2)
            3: { 1: 4, 2: 5, 5: 8 }, // q3 (R$3)
            4: { 1: 5, 2: 6, 5: 9 }, // q4 (R$4)
            5: { 1: 6, 2: 7, 5: 10 }, // q5 (R$5)
            6: { 1: 7, 2: 8, 5: 10 }, // q6 (R$6)
            7: { 1: 8, 2: 9, 5: 10 }, // q7 (R$7)
            8: { 1: 9, 2: 10 }, // q8 (R$8)
            9: { 1: 10 }, // q9 (R$9)
            10: {} // q10 (R$10) - Não aceita mais dinheiro
        };
        this.candies = { A: 6, B: 7, C: 8 };
    }

    insertMoney(amount) {
        // Verifica se o saldo atual + o valor inserido ultrapassa o limite
        const potentialState = this.state + amount;
        if (potentialState > this.maxBalance) {
            console.log(`Limite máximo de R$${this.maxBalance},00 atingido!`);
            return this.state; // Não permite inserir mais dinheiro
        }

        // Se há uma transição válida, atualiza o estado
        if (this.transitions[this.state] && this.transitions[this.state][amount]) {
            this.state = this.transitions[this.state][amount];
        }
        return this.state;
    }

    canBuy(candy) {
        return this.state >= this.candies[candy];
    }

    dispenseCandy(candy) {
        if (this.canBuy(candy)) {
            const change = this.state - this.candies[candy];
            this.reset(); // Reseta para q0 após dispensar
            return { candy, change };
        }
        return null;
    }

    reset() {
        this.state = 0; // Volta ao estado inicial
    }

    getCurrentState() {
        return this.state;
    }
}

export default VendingMachine;