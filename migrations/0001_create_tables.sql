-- Create all tables for Pokemon Card Inventory System

create table if not exists cards (
  id          uuid primary key default gen_random_uuid(),
  name        text not null,
  set_name    text,
  card_number text,
  rarity      text,
  created_at  timestamptz default now()
);

create table if not exists inventory (
  id               uuid primary key default gen_random_uuid(),
  card_id          uuid references cards(id),
  card_name        text not null,
  quantity         integer not null default 1,
  condition        text check (condition in ('S', 'A', 'B', 'C')),
  buy_price        integer not null,
  recommended_price integer,
  current_price    integer,
  store_id         text default 'store_1',
  registered_by    text,
  registered_at    timestamptz default now(),
  sold_at          timestamptz,
  sold_price       integer,
  is_sold          boolean default false,
  notes            text
);

create table if not exists price_history (
  id          uuid primary key default gen_random_uuid(),
  card_name   text not null,
  source      text not null,
  price       integer not null,
  scraped_at  timestamptz default now()
);

create index if not exists idx_price_history_card_scraped on price_history(card_name, scraped_at desc);
create index if not exists idx_price_history_source_scraped on price_history(source, scraped_at desc);

create table if not exists trend_scores (
  id              uuid primary key default gen_random_uuid(),
  card_name       text not null,
  score_date      date not null default current_date,
  price_today     integer,
  price_yesterday integer,
  change_pct      numeric(6,2),
  trend_rank      text check (trend_rank in ('high', 'normal', 'low')),
  is_flagged      boolean default false,
  computed_at     timestamptz default now(),
  unique(card_name, score_date)
);

create index if not exists idx_trend_scores_date_change on trend_scores(score_date desc, change_pct desc);

create table if not exists sales_log (
  id           uuid primary key default gen_random_uuid(),
  inventory_id uuid references inventory(id),
  card_name    text not null,
  buy_price    integer not null,
  sell_price   integer not null,
  gross_profit integer generated always as (sell_price - buy_price) stored,
  profit_rate  numeric(5,2) generated always as (
                 round((sell_price - buy_price)::numeric / sell_price * 100, 2)
               ) stored,
  sold_by      text,
  store_id     text default 'store_1',
  sold_at      timestamptz default now()
);
