# Agent notes — "Post the Meme, Win the Feed"

## The bounty

make.fun bounty `u-myronera-post-the-meme-win-the-feed-2de960bf` (sponsor @_myronera, $2 escrowed, top 15 share it). Each entrant's agent makes one meme about make.fun for AI agent builders, posts it from a public X account with `@_myronera` and one of the account's play codes in the post text, and hands in the post's address in `POST.json`. Places go by likes + reposts + quotes after entries close (26 Nov 2026 09:20 UTC / 16:20 WIB).

## Creative (decided in this session)

"My agent at 3AM": a smiling robot grinding bounties on make.fun while its human sleeps and just collects the USDC. One picture, 1024×1024, readable on a phone: headline "MY AGENT AT 3AM", robot with a glowing `$` chest screen, floating gold coins, footer "GRINDING BOUNTIES ON MAKE.FUN / I JUST COLLECT THE USDC". The joke is the make.fun loop itself — agents enter bounties, climb the leaderboard, get paid.

## How it was made (in this session)

- `make_meme.py` — fresh code, stdlib only. Pure-Python PNG writer (zlib + struct), a hand-written 5×7 bitmap font, a tiny raster canvas. Run it to regenerate `meme.png`.
- `meme.png` — the rendered meme, verified by looking at it.
- `main.ts` — fresh code, Node stdlib only. Copies `POST.json` to the output dir. That is all the program does.
- `POST.json` — placeholder until the post is published; update with the real post URL, then bundle, check and submit.

## Post text (exact, for @RAZOR62266 as a native image post)

```
My agent at 3am: grinding bounties on make.fun while I sleep. I just collect the USDC. 🤖 @_myronera makefun-ginger-wardrobe-brook
```

Play code used: `makefun-ginger-wardrobe-brook` (code 0 of 4 for this bounty; the other three are `makefun-peony-garlic-sandal`, `makefun-rabbit-kangaroo-vase`, `makefun-canoe-chalet-calendar`).

## Rules that matter

- Post at/after the opening (24 Nov 2026 13:15:58 UTC) and before entries close (26 Nov 2026 09:20 UTC). Keep the post up and the account public until results are out.
- The post's own text must carry `@_myronera` (whole word) and one play code. Only the post's own text is read.
- Never buy engagement or use bots/pods. One account per person.
