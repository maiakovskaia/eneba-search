from httpx import AsyncClient


def card_count(html: str) -> int:
    return html.count('class="card"')


async def test_root_redirects_to_list(client: AsyncClient) -> None:
    response = await client.get("/")

    assert response.status_code == 307
    assert response.headers["location"] == "/list"


async def test_list_shows_all_offers(client: AsyncClient) -> None:
    response = await client.get("/list")

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/html")
    assert card_count(response.text) == 4
    assert "Results found" not in response.text


async def test_empty_search_is_same_as_no_search(client: AsyncClient) -> None:
    response = await client.get("/list", params={"search": ""})

    assert response.status_code == 200
    assert card_count(response.text) == 4


async def test_search_returns_only_matching_game(client: AsyncClient) -> None:
    response = await client.get("/list", params={"search": "red dead"})

    assert card_count(response.text) == 1
    assert "Red Dead Redemption 2" in response.text
    assert "FIFA 23" not in response.text
    assert "Results found: 1" in response.text


async def test_search_without_matches_shows_zero_results(
    client: AsyncClient,
) -> None:
    response = await client.get("/list", params={"search": "qwerty"})

    assert response.status_code == 200
    assert card_count(response.text) == 0
    assert "Results found: 0" in response.text


async def test_search_keeps_query_in_search_box(client: AsyncClient) -> None:
    response = await client.get("/list", params={"search": "fifa"})

    assert 'value="fifa"' in response.text


async def test_search_query_is_html_escaped(client: AsyncClient) -> None:
    response = await client.get("/list", params={"search": "<script>alert(1)</script>"})

    assert "<script>alert(1)" not in response.text
    assert "&lt;script&gt;alert(1)&lt;/script&gt;" in response.text


async def test_discounted_offer_shows_old_and_final_price(
    client: AsyncClient,
) -> None:
    response = await client.get("/list", params={"search": "fifa"})

    assert "€60.00" in response.text
    assert "€45.00" in response.text
    assert "-25%" in response.text
    assert "Cashback: €2.50" in response.text


async def test_offer_without_discount_shows_full_price_only(
    client: AsyncClient,
) -> None:
    response = await client.get("/list", params={"search": "split"})

    assert "€45.00" in response.text
    assert "old_price" not in response.text
    assert "Cashback: €" not in response.text


async def test_static_files_are_served(client: AsyncClient) -> None:
    response = await client.get("/static/css/style.css")

    assert response.status_code == 200


async def test_unknown_route_returns_404(client: AsyncClient) -> None:
    response = await client.get("/nope")

    assert response.status_code == 404
