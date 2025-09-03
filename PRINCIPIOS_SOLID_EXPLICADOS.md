# Princípios SOLID Explicados com o Código Real
## Análise Linha por Linha dos Princípios SOLID no Simulador

---

## 1. SINGLE RESPONSIBILITY PRINCIPLE (SRP) - Princípio da Responsabilidade Única

### O que é?
**"Uma classe deve ter apenas UM motivo para mudar"**

Isso significa que cada classe deve fazer apenas uma coisa e fazer muito bem. Se você precisar mudar uma classe por dois motivos diferentes, é sinal que ela tem responsabilidades demais.

### Onde acontece no código?

#### **Classe Player** - `src/domain/models.py:16`
```python
@dataclass
class Player:
    name: str
    strategy: str
    balance: int = 300
    position: int = 0
    properties: List[Property] = field(default_factory=list)
    active: bool = True
```

**RESPONSABILIDADE ÚNICA**: Gerenciar o estado e comportamento de UM jogador.

#### **Método `move()` - Linha 25**
```python
def move(self, steps: int, board_size: int) -> bool:
    """Move player and return True if completed a lap"""
    prev = self.position
    self.position = (self.position + steps) % board_size
    return (prev + steps) >= board_size
```
**RESPONSABILIDADE**: Apenas movimentar o jogador no tabuleiro. Não faz pagamento, não compra propriedades, só move.

#### **Método `pay()` - Linha 31**
```python
def pay(self, amount: int) -> None:
    self.balance -= amount
    if self.balance < 0:
        self.active = False
```
**RESPONSABILIDADE**: Apenas processar pagamentos. Não move jogador, não compra propriedades, só gerencia dinheiro.

#### **Método `buy()` - Linha 39**
```python
def buy(self, prop: Property) -> None:
    self.balance -= prop.price
    self.properties.append(prop)
    prop.owner = self
```
**RESPONSABILIDADE**: Apenas comprar propriedades. Não move jogador, só faz a transação de compra.

### Por que isso é bom?

**Motivos para mudar a classe Player:**
- ✅ **UM SÓ**: Mudanças nas regras do jogador (ex: saldo inicial, limite de propriedades)

**Se estivesse ERRADO (violando SRP):**
- ❌ Mudanças nas regras do jogador
- ❌ Mudanças nas regras do tabuleiro  
- ❌ Mudanças na interface gráfica
- ❌ Mudanças no banco de dados

---

## 2. OPEN/CLOSED PRINCIPLE (OCP) - Princípio Aberto/Fechado

### O que é?
**"Aberto para extensão, fechado para modificação"**

Significa que você deve poder ADICIONAR novas funcionalidades sem ALTERAR o código existente. É como ter um celular onde você pode instalar novos aplicativos sem mexer no sistema operacional.

### Onde acontece no código?

#### **Sistema de Estratégias** - `src/adapters/strategies.py:29`

```python
STRATEGIES: Dict[str, Callable[[Player, Property], bool]] = {
    "impulsivo": impulsive_strategy,
    "exigente": demanding_strategy, 
    "cauteloso": cautious_strategy,
    "aleatorio": random_strategy,
}
```

#### **Como ADICIONAR nova estratégia SEM alterar código existente:**

```python
def conservative_strategy(player: Player, prop: Property) -> bool:
    """Conservative: only buys if property cost < 30% of balance"""
    return prop.price < (player.balance * 0.3)

# EXTENSÃO - Adicionando nova estratégia
STRATEGIES["conservador"] = conservative_strategy
```

#### **Uso no Game** - `src/usecases/game.py:37`
```python
strategy = STRATEGIES[player.strategy]
if player.balance >= prop.price and strategy(player, prop):
    player.buy(prop)
```

### Por que isso funciona?

**Linha 37**: `strategy = STRATEGIES[player.strategy]`
- O código do Game **NUNCA PRECISA MUDAR**
- Novas estratégias são **ADICIONADAS** no dicionário
- O Game continua funcionando com qualquer estratégia

### Analogia Fácil:
É como um **controle universal de TV**:
- **FECHADO**: O controle não muda quando você compra TV nova
- **ABERTO**: Funciona com qualquer TV que você conectar

---

## 3. LISKOV SUBSTITUTION PRINCIPLE (LSP) - Princípio da Substituição de Liskov

### O que é?
**"Objetos de uma classe devem poder ser substituídos por objetos de suas subclasses sem quebrar o programa"**

No nosso caso, todas as estratégias seguem o mesmo "contrato" e podem ser substituídas umas pelas outras.

### Onde acontece no código?

#### **Todas as estratégias seguem a MESMA assinatura:**

**Estratégia Impulsiva** - Linha 9:
```python
def impulsive_strategy(player: Player, prop: Property) -> bool:
    return True
```

**Estratégia Exigente** - Linha 14:
```python
def demanding_strategy(player: Player, prop: Property) -> bool:
    return prop.rent > 50
```

**Estratégia Cautelosa** - Linha 19:
```python
def cautious_strategy(player: Player, prop: Property) -> bool:
    return (player.balance - prop.price) >= 80
```

### O "Contrato" que todas seguem:
- **ENTRADA**: Recebem `Player` e `Property`
- **SAÍDA**: Retornam `bool` (True = compra, False = não compra)
- **COMPORTAMENTO**: Decidem se o jogador deve comprar a propriedade

### Substituição em ação - `src/usecases/game.py:37-39`:
```python
strategy = STRATEGIES[player.strategy]  # LSP: Qualquer estratégia serve
if player.balance >= prop.price and strategy(player, prop):  # LSP: Todas funcionam igual
    player.buy(prop)
```

### Analogia Fácil:
É como **tomadas elétricas**:
- Qualquer aparelho com **plug padrão** funciona em qualquer tomada
- **Impulsiva** = Aspirador (sempre ligado)
- **Exigente** = TV 4K (só liga se a energia for boa)  
- **Cautelosa** = Geladeira (economiza energia)
- **Todas** se conectam na **mesma tomada** (Game)

---

## 4. INTERFACE SEGREGATION PRINCIPLE (ISP) - Princípio da Segregação de Interface

### O que é?
**"Uma classe não deve ser forçada a implementar interfaces que não usa"**

Significa criar interfaces pequenas e específicas ao invés de uma grande interface genérica.

### Onde acontece no código?

#### **Estratégias têm interface ESPECÍFICA** - `src/adapters/strategies.py:29`
```python
# Interface específica: APENAS decisão de compra
Callable[[Player, Property], bool]
```

**O que as estratégias FAZEM:**
- ✅ Decidem se compram ou não

**O que as estratégias NÃO FAZEM:**
- ❌ Não movem o jogador
- ❌ Não gerenciam o dinheiro
- ❌ Não controlam o jogo
- ❌ Não fazem relatórios

#### **Se estivesse ERRADO (violando ISP):**
```python
# INTERFACE INCHADA (exemplo do que NÃO fazer)
class PlayerStrategy:
    def decide_purchase(self, player, prop) -> bool: pass
    def move_player(self, steps) -> None: pass           # ❌ Nem todas precisam
    def generate_report(self) -> str: pass               # ❌ Nem todas precisam  
    def manage_database(self) -> None: pass              # ❌ Nem todas precisam
```

### Por que é melhor assim?

**Interface pequena e focada:**
- **Estratégia Impulsiva**: Só precisa decidir compra (simples)
- **Estratégia Exigente**: Só precisa decidir compra (analisando aluguel)
- Cada uma implementa **APENAS** o que precisa

---

## 5. DEPENDENCY INVERSION PRINCIPLE (DIP) - Princípio da Inversão de Dependência

### O que é?
**"Módulos de alto nível não devem depender de módulos de baixo nível. Ambos devem depender de abstrações"**

É como ter um **carregador universal** para celular ao invés de cada aparelho ter seu próprio carregador específico.

### Onde acontece no código?

#### **Game recebe Random como dependência** - `src/usecases/game.py:11`

```python
class Game:
    def __init__(self, rng: Optional[Random] = None):
        self.board: List[Property] = []
        self.players: List[Player] = []
        self.max_rounds = 1000
        self.rng = rng or random.Random()  # ← DEPENDÊNCIA INJETADA
```

#### **Por que isso é INVERSÃO de dependência?**

**ERRADO** (dependência direta):
```python
class Game:
    def __init__(self):
        self.rng = random.Random()  # ❌ Game depende DIRETAMENTE do Random
```

**CORRETO** (dependência invertida):
```python
class Game:
    def __init__(self, rng: Optional[Random] = None):
        self.rng = rng or random.Random()  # ✅ Game recebe abstração
```

### Como isso é usado?

#### **Em produção** (números reais aleatórios):
```python
game = Game()  # Usa random.Random() padrão
result = game.simulate()
```

#### **Em testes** (números controlados):
```python
controlled_random = Random(42)  # Seed fixo para testes
game = Game(rng=controlled_random)  # Injeta dependência controlada
result = game.simulate()  # Resultado previsível
```

#### **Game usa a dependência** - `src/usecases/game.py:30`
```python
steps = self.rng.randint(1, 6)  # Usa a abstração injetada
```

### Por que isso é bom?

#### **Flexibilidade:**
- **Produção**: Random real para jogos variados
- **Testes**: Random controlado para testes previsíveis
- **Demo**: Random com seed fixa para demonstrações

#### **Testabilidade:**
```python
# Teste sempre passa - comportamento previsível
def test_game_with_fixed_random():
    fixed_rng = Random(123)
    game = Game(rng=fixed_rng)
    
    # Sabemos exatamente o que vai acontecer
    winner = game.simulate()
    assert winner == "impulsivo"  # Resultado previsível
```

### Analogia Fácil:
É como um **carro com combustível flexível**:
- **Alto nível**: Carro (Game)
- **Baixo nível**: Gasolina/Álcool (Random específico)
- **Abstração**: Sistema de combustível (qualquer Random)

**Sem DIP**: Carro só roda com gasolina Shell do posto específico
**Com DIP**: Carro roda com qualquer combustível compatível

---

## 6. RESUMO - TODOS OS PRINCÍPIOS TRABALHANDO JUNTOS

### Como os princípios se COMPLEMENTAM no código:

#### **Fluxo de uma jogada** - `src/usecases/game.py:30-42`
```python
# DIP: Random injetado
steps = self.rng.randint(1, 6)

# SRP: Player só move
completed = player.move(steps, len(self.board))

# SRP: Player só recebe dinheiro  
if completed:
    player.receive(100)

prop = self.board[player.position]
if prop.owner is None:
    # OCP + LSP: Estratégias substituíveis
    strategy = STRATEGIES[player.strategy]
    if player.balance >= prop.price and strategy(player, prop):
        # SRP: Player só compra
        player.buy(prop)
elif prop.owner is not player:
    # SRP: Player só paga
    player.pay(prop.rent)
    # SRP: Owner só recebe
    prop.owner.receive(prop.rent)
```

### Benefícios PRÁTICOS:

#### **Para TESTES:**
```python
def test_impulsive_player():
    # DIP: Controlo o random
    game = Game(rng=Random(42))
    
    # SRP: Testo só uma coisa por vez
    player = Player("test", "impulsivo")
    
    # LSP: Qualquer estratégia funciona
    strategy = STRATEGIES["impulsivo"]
    result = strategy(player, Property(0, 100, 10))
    
    assert result == True  # Impulsivo sempre compra
```

#### **Para NOVAS FEATURES:**
```python
# OCP: Adiciono sem quebrar nada
def millionaire_strategy(player: Player, prop: Property) -> bool:
    return player.balance > 1000  # Só compra se for rico

STRATEGIES["milionario"] = millionaire_strategy  # Extensão pura
```

#### **Para MANUTENÇÃO:**
- **Bug na movimentação?** Mexo só no método `move()` (SRP)
- **Nova estratégia?** Adiciono sem tocar no Game (OCP)
- **Mudar gerador random?** Injeto outro no construtor (DIP)
- **Teste quebrou?** Cada método testado isoladamente (SRP + DIP)

### Por que SOLID é importante?

**SEM SOLID**: Código espaguete onde tudo depende de tudo
**COM SOLID**: Código modular onde cada peça tem sua função

É a diferença entre uma **casa de cartas** (mexe numa, cai tudo) e **blocos de LEGO** (cada peça independente, pode montar qualquer coisa).

---

*Os 5 princípios SOLID trabalhando juntos criam um código que é fácil de entender, fácil de testar, fácil de manter e fácil de estender.*