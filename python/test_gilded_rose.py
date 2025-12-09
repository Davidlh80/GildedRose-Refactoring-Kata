# test_gilded_rose.py
import pytest
from gilded_rose import Item, GildedRose

# --- Fixtures ---
# Uma 'fixture' do pytest para criar instâncias de GildedRose
@pytest.fixture
def gilded_rose_instance():
    # Inicializa com uma lista vazia de itens
    return GildedRose([])

# --- Testes Unitários para a Regra Comum ---

def test_regular_item_quality_and_sellin_decrease():
    """
    Testa um item comum: Quality e SellIn diminuem em 1.
    """
    items = [Item("Elixir of the Mongoose", 10, 20)]
    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()
    
    assert items[0].sell_in == 9
    assert items[0].quality == 19

def test_regular_item_quality_decreases_twice_after_sellin():
    """
    Testa que a Quality de itens comuns diminui duas vezes mais rápido
    após a data de SellIn.
    """
    items = [Item("Elixir of the Mongoose", 0, 10)]
    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()
    
    # SellIn passa de 0 para -1
    assert items[0].sell_in == -1
    # Quality diminui em 2 (1 + 1 extra por SellIn < 0)
    assert items[0].quality == 8

def test_regular_item_quality_never_negative():
    """
    Testa que a Quality de um item comum nunca é negativa.
    """
    items = [Item("Elixir of the Mongoose", 5, 0)]
    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()
    
    assert items[0].quality == 0
    assert items[0].sell_in == 4

# --- Testes Unitários para Itens Especiais ---

# 1. Sulfuras, Hand of Ragnaros
def test_sulfuras_never_changes():
    """
    Testa que Sulfuras nunca muda de Quality ou SellIn.
    """
    items = [Item("Sulfuras, Hand of Ragnaros", 10, 80)]
    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()
    
    assert items[0].sell_in == 10  # Nunca muda
    assert items[0].quality == 80  # Nunca muda

# 2. Aged Brie
def test_aged_brie_quality_increases():
    """
    Testa que Aged Brie aumenta Quality em 1 a cada dia.
    """
    items = [Item("Aged Brie", 10, 40)]
    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()
    
    assert items[0].sell_in == 9
    assert items[0].quality == 41

def test_aged_brie_quality_increases_twice_after_sellin():
    """
    Testa que Aged Brie aumenta Quality em 2 após a data de SellIn.
    """
    items = [Item("Aged Brie", 0, 40)]
    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()
    
    assert items[0].sell_in == -1
    assert items[0].quality == 42 # Aumenta em 2 (1 + 1 extra)

def test_aged_brie_quality_max_50():
    """
    Testa que a Quality de Aged Brie nunca excede 50.
    """
    items = [Item("Aged Brie", 10, 50)]
    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()
    
    assert items[0].quality == 50
    
    # Teste de limite (49 -> 50)
    items = [Item("Aged Brie", 10, 49)]
    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()
    assert items[0].quality == 50

# 3. Backstage passes
def test_backstage_pass_quality_increases_by_1_normally():
    """
    Testa que Backstage passes aumenta Quality em 1 quando SellIn > 10.
    """
    items = [Item("Backstage passes to a TAFKAL80ETC concert", 15, 20)]
    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()
    
    assert items[0].sell_in == 14
    assert items[0].quality == 21

def test_backstage_pass_quality_increases_by_2_near_concert_10():
    """
    Testa que Backstage passes aumenta Quality em 2 quando 5 < SellIn <= 10.
    """
    items = [Item("Backstage passes to a TAFKAL80ETC concert", 10, 20)] # Limite
    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()
    
    assert items[0].sell_in == 9
    assert items[0].quality == 22 # Aumentou em 2

    items = [Item("Backstage passes to a TAFKAL80ETC concert", 6, 20)]
    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()
    
    assert items[0].sell_in == 5
    assert items[0].quality == 22 # Aumentou em 2

def test_backstage_pass_quality_increases_by_3_near_concert_5():
    """
    Testa que Backstage passes aumenta Quality em 3 quando 0 < SellIn <= 5.
    """
    items = [Item("Backstage passes to a TAFKAL80ETC concert", 5, 20)] # Limite
    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()
    
    assert items[0].sell_in == 4
    assert items[0].quality == 23 # Aumentou em 3
    
    items = [Item("Backstage passes to a TAFKAL80ETC concert", 1, 20)]
    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()
    
    assert items[0].sell_in == 0
    assert items[0].quality == 23 # Aumentou em 3

def test_backstage_pass_quality_drops_to_0_after_concert():
    """
    Testa que Backstage passes zera Quality após a data de SellIn.
    """
    items = [Item("Backstage passes to a TAFKAL80ETC concert", 0, 30)]
    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()
    
    assert items[0].sell_in == -1
    assert items[0].quality == 0 # Zera completamente
    
def test_backstage_pass_quality_max_50():
    """
    Testa que Quality de Backstage passes nunca excede 50, mesmo nos picos.
    """
    # Teste no pico de +3
    items = [Item("Backstage passes to a TAFKAL80ETC concert", 2, 48)]
    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()
    
    assert items[0].quality == 50 # Limita a 50
    
    # Teste no pico de +2
    items = [Item("Backstage passes to a TAFKAL80ETC concert", 7, 49)]
    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()
    
    assert items[0].quality == 50 # Limita a 50