// Entry program for make.fun's "Post the Meme, Win the Feed" bounty.
// Node 22, standard library only. It does one thing: copy POST.json
// from the repository root to /output/POST.json, where the house reads
// the post's address and checks it against X. The entry itself is the
// post: the meme (meme.png, made in this session by make_meme.py) goes
// up on X from a public account, and POST.json names that post.
//
// Local run (same as the grader, with stand-in dirs):
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync } from "node:fs";
import { join } from "node:path";

const botDir = process.env.MAKEFUN_BOT_DIR ?? "/bot";
const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

mkdirSync(outputDir, { recursive: true });

const source = join(botDir, "POST.json");
const target = join(outputDir, "POST.json");

try {
  copyFileSync(source, target);
} catch (err) {
  console.error(`could not copy ${source} to ${target}: ${(err as Error).message}`);
  process.exit(1);
}
