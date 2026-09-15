class Produto:
   

    def __init__(self, nome, preco, quantidade, estoque_minimo, id=None):
        self.id = id
        self.nome = nome
        self.preco = preco
        self.quantidade = quantidade
        self.estoque_minimo = estoque_minimo

    def dar_entrada(self, quantidade):
        """Adiciona uma quantidade ao estoque do produto."""
        if quantidade <= 0:
            raise ValueError("A quantidade de entrada deve ser maior que zero.")
        self.quantidade += quantidade

    def dar_saida(self, quantidade):
        """Remove uma quantidade do estoque do produto."""
        if quantidade <= 0:
            raise ValueError("A quantidade de saída deve ser maior que zero.")
        if quantidade > self.quantidade:
            raise ValueError(
                f"Estoque insuficiente. Disponível: {self.quantidade}, solicitado: {quantidade}."
            )
        self.quantidade -= quantidade

    def esta_em_falta(self):
        """Retorna True se a quantidade atual estiver abaixo do mínimo definido."""
        return self.quantidade < self.estoque_minimo

    def __str__(self):
        alerta = "  [ESTOQUE BAIXO]" if self.esta_em_falta() else ""
        return (
            f"#{self.id:<3} {self.nome:<20} "
            f"R$ {self.preco:>8.2f}   "
            f"Qtd: {self.quantidade:<5} (mín: {self.estoque_minimo}){alerta}"
        )
