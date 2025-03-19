class MaquinaDocesAFD:
    def __init__(self):
        self.saldo = 0.0
        self.precos = {"A": 6.0, "B": 7.0, "C": 8.0}  # Preços dos doces
        self.compras = {"A": 0, "B": 0, "C": 0}  # Histórico de doces comprados
        self.gasto_total = 0.0  # Gasto total acumulado

    def inserir_dinheiro(self, valor):
        self.saldo += valor

    def resetar(self):
        self.saldo = 0.0
        self.compras = {"A": 0, "B": 0, "C": 0}  # Reseta o histórico
        self.gasto_total = 0.0  # Reseta o gasto total

    def get_opcoes(self):
        opcoes = []
        if self.saldo == 0:
            return "Saldo insuficiente"

        for doce, preco in self.precos.items():
            if self.saldo >= preco:
                troco = self.saldo - preco
                opcoes.append(f"Doce {doce} (R${preco:.2f}) [Troco: R${troco:.2f}]")
        
        if not opcoes:
            opcoes.append("Saldo insuficiente")
        return " | ".join(opcoes)

    def comprar_doce(self, doce, unidades=1):
        """
        Tenta comprar 'unidades' do doce especificado.
        Retorna uma tupla (sucesso, mensagem, troco).
        """
        if doce not in self.precos:
            return False, "Doce inválido!", 0.0
        
        preco_unitario = self.precos[doce]
        custo_total = preco_unitario * unidades
        
        if self.saldo < custo_total:
            return False, f"Saldo insuficiente para comprar {unidades} x Doce {doce}!", 0.0
        
        # Compra bem-sucedida
        self.saldo -= custo_total
        self.compras[doce] += unidades  # Atualiza o histórico de compras
        self.gasto_total += custo_total  # Atualiza o gasto total
        troco = self.saldo
        return True, f"Doce {doce} Liberado! Troco: R${troco:.2f}", troco

    def get_compras(self):
        """
        Retorna uma lista com o histórico de compras e o gasto total.
        """
        compras_texto = []
        for doce, quantidade in self.compras.items():
            if quantidade > 0:
                compras_texto.append(f"{quantidade} Doce {doce}")
        if not compras_texto:
            compras_texto.append("Nenhum doce comprado")
        compras_texto.append(f"Gasto Total: R${self.gasto_total:.2f}")
        return compras_texto

# Exemplo de uso
if __name__ == "__main__":
    maquina = MaquinaDocesAFD()
    maquina.inserir_dinheiro(12.0)
    print(maquina.get_opcoes())  # Mostra as opções
    sucesso, mensagem, troco = maquina.comprar_doce("A", 1)  # Compra 1 unidade do Doce A
    print(mensagem)  # "Doce A Liberado! Troco: R$6.00"
    print(maquina.get_compras())  # Mostra o histórico