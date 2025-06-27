import argparse
import asyncio
import json
import multiprocessing
from typing import Any

import matplotlib.pyplot as plt
from pygit2.repository import Repository
from pygit2.enums import SortMode
from pygit2 import Commit
from tqdm.asyncio import tqdm


async def run_cloc(commit: Commit, semaphores: asyncio.Semaphore) -> dict[str, Any]:
    async with semaphores:
        tqdm.write(f"checking {commit.short_id}")
        process = await asyncio.create_subprocess_exec(
            "cloc",
            "--git",
            str(commit.id),
            "--json",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        out, _ = await process.communicate()
    stats = json.loads(out.decode())
    del stats["header"]
    return stats


async def run_script(repo_name: str, cpu_count: int, output_path: str) -> None:
    repo = Repository(repo_name)
    print(f"executing on {cpu_count} cores")
    semaphores = asyncio.Semaphore(cpu_count)
    tasks = [
        run_cloc(commit, semaphores)
        for commit in repo.walk(
            repo.head.target, SortMode.TOPOLOGICAL | SortMode.REVERSE
        )
    ]
    plot_dicts = await tqdm.gather(*tasks)
    x_points = list(range(0, len(plot_dicts)))

    fig, ax = plt.subplots()
    lang_set = set()
    for dict_ in plot_dicts:
        for lang in dict_:
            lang_set.add(lang)
    print(lang_set)

    for lang in lang_set:
        ax.plot(
            x_points,
            list(map(lambda x: x.get(lang, {"code": 0})["code"], plot_dicts)),
            label=lang,
        )

    plt.legend()
    plt.savefig(output_path)


def main() -> None:
    parser = argparse.ArgumentParser(prog="ploc")
    parser.add_argument(
        "--jobs",
        "-j",
        help="How many cloc jobs to run un parallel",
        default=multiprocessing.cpu_count(),
        type=int,
    )
    parser.add_argument(
        "--output", "-o", help="What to output to", default="plot.png", type=str
    )
    parser.add_argument(
        "--repo", "-r", help="Path to bare git repository", default=".git", type=str
    )
    args = parser.parse_args()
    asyncio.run(run_script(args.repo, args.jobs, args.output))
