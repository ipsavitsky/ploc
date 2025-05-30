import argparse
import asyncio
import json
import multiprocessing

import matplotlib.pyplot as plt
from pygit2 import Repository
from pygit2.enums import SortMode
from tqdm.asyncio import tqdm


async def run_cloc(commit, semaphores):
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


async def run_script(repo, cpu_count):
    repo = Repository(repo)
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
    plt.savefig("plot.png")


def main():
    parser = argparse.ArgumentParser(prog="ploc")
    parser.add_argument(
        "--jobs",
        "-j",
        help="How many cloc jobs to run un parallel",
        default=multiprocessing.cpu_count(),
        type=int,
    )
    parser.add_argument(
        "--repo", "-r", help="Path to bare git repository", default=".git", type=str
    )
    args = parser.parse_args()
    asyncio.run(run_script(args.repo, args.jobs))
