"""
Seed data for the Pokemon Card Inventory system.

Uses the Supabase table API with upsert to stay idempotent.
Safe to run multiple times — existing rows are updated, not duplicated.
"""

from supabase import Client

CARDS = [
    {
        "id": "00000000-0000-0000-0000-000000000001",
        "name": "リザードン ex",
        "set_name": "黒炎の支配者",
        "card_number": "SV3-115",
        "rarity": "SAR",
    },
    {
        "id": "00000000-0000-0000-0000-000000000002",
        "name": "ピカチュウ ex",
        "set_name": "スカーレット ex",
        "card_number": "SV1S-024",
        "rarity": "SR",
    },
    {
        "id": "00000000-0000-0000-0000-000000000003",
        "name": "ミュウツー ex",
        "set_name": "ポケモンカード151",
        "card_number": "SV2a-150",
        "rarity": "SAR",
    },
    {
        "id": "00000000-0000-0000-0000-000000000004",
        "name": "レックウザ VMAX",
        "set_name": "蒼空ストリーム",
        "card_number": "S7R-047",
        "rarity": "HR",
    },
    {
        "id": "00000000-0000-0000-0000-000000000005",
        "name": "ギラティナ VSTAR",
        "set_name": "ロストアビス",
        "card_number": "S11-043",
        "rarity": "UR",
    },
    {
        "id": "00000000-0000-0000-0000-000000000006",
        "name": "ナンジャモ",
        "set_name": "クレイバースト",
        "card_number": "SV2P-091",
        "rarity": "SAR",
    },
    {
        "id": "00000000-0000-0000-0000-000000000007",
        "name": "リーリエの全力",
        "set_name": "ドリームリーグ",
        "card_number": "SM11b-068",
        "rarity": "SR",
    },
    {
        "id": "00000000-0000-0000-0000-000000000008",
        "name": "ルギア VSTAR",
        "set_name": "パラダイムトリガー",
        "card_number": "S12-083",
        "rarity": "UR",
    },
]

INVENTORY = [
    {
        "id": "10000000-0000-0000-0000-000000000001",
        "card_id": "00000000-0000-0000-0000-000000000001",
        "card_name": "リザードン ex",
        "quantity": 2,
        "condition": "S",
        "buy_price": 9000,
        "recommended_price": 14400,
        "current_price": 14000,
        "store_id": "store_1",
        "registered_by": "Tanaka",
    },
    {
        "id": "10000000-0000-0000-0000-000000000002",
        "card_id": "00000000-0000-0000-0000-000000000002",
        "card_name": "ピカチュウ ex",
        "quantity": 3,
        "condition": "A",
        "buy_price": 3500,
        "recommended_price": 5400,
        "current_price": 5000,
        "store_id": "store_1",
        "registered_by": "Tanaka",
    },
    {
        "id": "10000000-0000-0000-0000-000000000003",
        "card_id": "00000000-0000-0000-0000-000000000003",
        "card_name": "ミュウツー ex",
        "quantity": 1,
        "condition": "A",
        "buy_price": 7000,
        "recommended_price": 10800,
        "current_price": 10000,
        "store_id": "store_1",
        "registered_by": "Suzuki",
    },
    {
        "id": "10000000-0000-0000-0000-000000000004",
        "card_id": "00000000-0000-0000-0000-000000000006",
        "card_name": "ナンジャモ",
        "quantity": 1,
        "condition": "S",
        "buy_price": 15000,
        "recommended_price": 22800,
        "current_price": 22000,
        "store_id": "store_1",
        "registered_by": "Tanaka",
    },
    {
        "id": "10000000-0000-0000-0000-000000000005",
        "card_id": "00000000-0000-0000-0000-000000000004",
        "card_name": "レックウザ VMAX",
        "quantity": 2,
        "condition": "B",
        "buy_price": 4000,
        "recommended_price": 6000,
        "current_price": 5500,
        "store_id": "store_1",
        "registered_by": "Suzuki",
    },
]

PRICE_HISTORY = [
    # リザードン ex — price going up (triggers high flag)
    {"card_name": "リザードン ex", "source": "pokeca_chart", "price": 11000},
    {"card_name": "リザードン ex", "source": "pokeca_chart", "price": 12000},
    # ピカチュウ ex — stable
    {"card_name": "ピカチュウ ex", "source": "pokeca_chart", "price": 4500},
    {"card_name": "ピカチュウ ex", "source": "pokeca_chart", "price": 4500},
    # ミュウツー ex — price dropping (triggers low flag)
    {"card_name": "ミュウツー ex", "source": "pokeca_chart", "price": 9500},
    {"card_name": "ミュウツー ex", "source": "pokeca_chart", "price": 9000},
    # ナンジャモ — big jump (triggers high flag)
    {"card_name": "ナンジャモ", "source": "pokeca_chart", "price": 18000},
    {"card_name": "ナンジャモ", "source": "pokeca_chart", "price": 19000},
    # レックウザ VMAX — stable
    {"card_name": "レックウザ VMAX", "source": "pokeca_chart", "price": 5000},
    {"card_name": "レックウザ VMAX", "source": "pokeca_chart", "price": 5100},
]

TREND_SCORES = [
    {
        "card_name": "リザードン ex",
        "price_today": 12000,
        "price_yesterday": 11000,
        "change_pct": 9.09,
        "trend_rank": "normal",
        "is_flagged": True,
    },
    {
        "card_name": "ピカチュウ ex",
        "price_today": 4500,
        "price_yesterday": 4500,
        "change_pct": 0.00,
        "trend_rank": "normal",
        "is_flagged": False,
    },
    {
        "card_name": "ミュウツー ex",
        "price_today": 9000,
        "price_yesterday": 9500,
        "change_pct": -5.26,
        "trend_rank": "low",
        "is_flagged": True,
    },
    {
        "card_name": "ナンジャモ",
        "price_today": 19000,
        "price_yesterday": 18000,
        "change_pct": 5.56,
        "trend_rank": "normal",
        "is_flagged": True,
    },
    {
        "card_name": "レックウザ VMAX",
        "price_today": 5100,
        "price_yesterday": 5000,
        "change_pct": 2.00,
        "trend_rank": "normal",
        "is_flagged": False,
    },
]


def seed_all(client: Client) -> None:
    print("  [cards] upserting...")
    client.table("cards").upsert(CARDS, on_conflict="id").execute()
    print(f"  [ok] {len(CARDS)} cards")

    print("  [inventory] upserting...")
    client.table("inventory").upsert(INVENTORY, on_conflict="id").execute()
    print(f"  [ok] {len(INVENTORY)} inventory items")

    print("  [price_history] inserting...")
    client.table("price_history").insert(PRICE_HISTORY).execute()
    print(f"  [ok] {len(PRICE_HISTORY)} price records")

    print("  [trend_scores] upserting...")
    client.table("trend_scores").upsert(
        TREND_SCORES, on_conflict="card_name,score_date"
    ).execute()
    print(f"  [ok] {len(TREND_SCORES)} trend scores")

    print("  Seed complete.")
