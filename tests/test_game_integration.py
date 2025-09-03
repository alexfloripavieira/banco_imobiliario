from src.usecases.game import simulateGames


def test_simulate_single():
    res = simulateGames(n=1, seed=42)
    assert "vencedor" in res
    assert "jogadores" in res
    assert "rodadas" in res


def test_simulate_batch():
    res = simulateGames(n=10, seed=42)
    assert res["simulacoes"] == 10
    assert "vitorias" in res
    assert "percentuais" in res
    assert "media_rodadas" in res
