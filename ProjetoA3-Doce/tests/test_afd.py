from src.automato import MaquinaDocesAFD

def testar_afd():
    maquina = MaquinaDocesAFD()
    
    # Teste 1: Doce A sem troco (R$6)
    maquina.inserir_dinheiro(5)
    maquina.inserir_dinheiro(1)
    assert maquina.saldo == 6, "Erro: Saldo deveria ser R$6"
    assert "Doce A (R$6) [Sem troco]" in maquina.get_opcoes(), "Erro: Deve mostrar Doce A sem troco"
    print("Teste 1 (Doce A sem troco): OK")
    
    # Teste 2: Doce B sem troco (R$7)
    maquina.resetar()
    maquina.inserir_dinheiro(5)
    maquina.inserir_dinheiro(2)
    assert maquina.saldo == 7, "Erro: Saldo deveria ser R$7"
    assert "Doce B (R$7) [Sem troco]" in maquina.get_opcoes(), "Erro: Deve mostrar Doce B sem troco"
    print("Teste 2 (Doce B sem troco): OK")
    
    # Teste 3: Doce C sem troco (R$8)
    maquina.resetar()
    maquina.inserir_dinheiro(5)
    maquina.inserir_dinheiro(2)
    maquina.inserir_dinheiro(1)
    assert maquina.saldo == 8, "Erro: Saldo deveria ser R$8"
    assert "Doce C (R$8) [Sem troco]" in maquina.get_opcoes(), "Erro: Deve mostrar Doce C sem troco"
    print("Teste 3 (Doce C sem troco): OK")
    
    # Teste 4: Doce A com troco (R$10)
    maquina.resetar()
    maquina.inserir_dinheiro(5)
    maquina.inserir_dinheiro(5)
    assert maquina.saldo == 10, "Erro: Saldo deveria ser R$10"
    assert "Doce A (R$6) [Troco: R$4.00]" in maquina.get_opcoes(), "Erro: Deve mostrar Doce A com troco"
    print("Teste 4 (Doce A com troco): OK")

if __name__ == "__main__":
    testar_afd()