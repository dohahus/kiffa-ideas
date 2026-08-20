-- ─────────────────────────────────────────────────────────────
--  قاعدة بيانات لوحة الأفكار — كِفّة
--  الصقي هذا الملف كاملًا في:  Supabase ← SQL Editor ← Run
-- ─────────────────────────────────────────────────────────────

create table if not exists public.ideas (
  id         text primary key,
  name       text        not null,
  points     smallint    not null check (points in (1, 10)),
  note       text        not null default '',
  date       date        not null,
  ts         bigint      not null,
  created_at timestamptz not null default now()
);

create index if not exists ideas_date_idx on public.ideas (date desc);
create index if not exists ideas_name_idx on public.ideas (name);

alter table public.ideas enable row level security;

-- اللوحة مفتوحة عمدًا: أي شخص معه الرابط يقدر يقرأ ويسجّل ويحذف.
-- لو احتجتِ لاحقًا تقييد الحذف أو إضافة تسجيل دخول، عدّلي هذه السياسات.
drop policy if exists ideas_read   on public.ideas;
drop policy if exists ideas_insert on public.ideas;
drop policy if exists ideas_delete on public.ideas;

create policy ideas_read   on public.ideas for select using (true);
create policy ideas_insert on public.ideas for insert with check (true);
create policy ideas_delete on public.ideas for delete using (true);
