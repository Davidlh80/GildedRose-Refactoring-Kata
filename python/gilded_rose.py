# gilded_rose.py (Refatorado)

class Item:
    """Representação base de um item no inventário."""
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)

# --- Classes de Lógica Específica (Padrão Strategy) ---

class ItemUpdater:
    """Classe base para a estratégia de atualização de um item."""
    def __init__(self, item):
        self.item = item

    def _decrease_sell_in(self):
        """Diminui o SellIn para a maioria dos itens."""
        self.item.sell_in -= 1

    def _cap_quality(self):
        """Garante que a Quality esteja sempre entre 0 e 50 (exceto Sulfuras)."""
        if self.item.quality > 50:
            self.item.quality = 50
        if self.item.quality < 0:
            self.item.quality = 0

    def update(self):
        """Método principal de atualização, a ser implementado por subclasses."""
        raise NotImplementedError

class RegularItemUpdater(ItemUpdater):
    """Lógica para itens comuns (qualidade diminui em 1 ou 2)."""
    def update(self):
        self._decrease_sell_in()

        # Quality diminui em 1
        self.item.quality -= 1

        # Após SellIn expirar, Quality diminui mais 1
        if self.item.sell_in < 0:
            self.item.quality -= 1
        
        self._cap_quality()

class AgedBrieUpdater(ItemUpdater):
    """Lógica para 'Aged Brie' (qualidade aumenta)."""
    def update(self):
        self._decrease_sell_in()

        # Quality sempre aumenta em 1
        self.item.quality += 1
        
        # Após SellIn expirar, Quality aumenta mais 1
        if self.item.sell_in < 0:
            self.item.quality += 1
            
        self._cap_quality()

class SulfurasUpdater(ItemUpdater):
    """Lógica para 'Sulfuras' (nunca muda)."""
    def update(self):
        # Sulfuras não muda SellIn nem Quality
        pass

class BackstagePassUpdater(ItemUpdater):
    """Lógica para 'Backstage passes' (qualidade variável)."""
    def update(self):
        self._decrease_sell_in()
        
        # Aumenta Quality em 1
        self.item.quality += 1 

        # Aumenta mais 1 (total de +2) quando faltam 10 dias ou menos
        if self.item.sell_in < 10:
            self.item.quality += 1
        
        # Aumenta mais 1 (total de +3) quando faltam 5 dias ou menos
        if self.item.sell_in < 5:
            self.item.quality += 1
            
        # Quality cai para 0 após o show (SellIn < 0)
        if self.item.sell_in < 0:
            self.item.quality = 0
            
        self._cap_quality()

# --- Classe Principal com Factory ---

class GildedRose(object):

    # Mapeamento do nome do item para a classe atualizadora correspondente
    UPDATER_MAP = {
        "Aged Brie": AgedBrieUpdater,
        "Sulfuras, Hand of Ragnaros": SulfurasUpdater,
        "Backstage passes to a TAFKAL80ETC concert": BackstagePassUpdater,
    }

    def __init__(self, items):
        self.items = items

    def _get_updater(self, item):
        """
        Factory Method para obter o objeto de estratégia (Updater) correto.
        Se o nome não estiver no mapa, usa a estratégia RegularItemUpdater.
        """
        updater_class = self.UPDATER_MAP.get(item.name, RegularItemUpdater)
        return updater_class(item)

    def update_quality(self):
        """
        Itera sobre os itens e usa a estratégia (Updater) apropriada
        para atualizar sua qualidade e data de validade.
        """
        for item in self.items:
            updater = self._get_updater(item)
            updater.update()

# O código final é muito mais limpo e a lógica de negócios está
# claramente separada, o que facilita a modificação de uma regra
# sem afetar as outras.