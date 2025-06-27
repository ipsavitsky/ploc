# Ploc

`ploc` is a tool for visualizing code statistics over the history of a Git repository. It uses `cloc` to gather statistics for each commit and `matplotlib` to plot the changes in lines of code for different languages over time.

## Features

- Analyze code statistics (lines of code, comments, blanks) for each commit in a Git repository.
- Visualize code changes for multiple languages on a single plot.
- Supports parallel execution of `cloc` jobs for faster processing.

## Installation

This project uses `uv` for Python dependency management and `nix` for a reproducible development environment, including `cloc`.

### Option 1: Using `uv` (recommended)

1.  **Install `uv`:**
    Follow the instructions on the [uv GitHub page](https://github.com/astral-sh/uv#installation) to install `uv`.

2.  **Install Python dependencies:**
    Navigate to the `ploc` directory and run:
    ```bash
    uv sync
    ```

3.  **Install `cloc`:**
    `cloc` is an external dependency. Install it using your system's package manager (e.g., `sudo apt-get install cloc` on Debian/Ubuntu, `brew install cloc` on macOS, `nix-env -iA nixpkgs.cloc` if you have Nix installed).

### Option 2: Using `nix`

If you have Nix installed, you can enter a development shell that includes all Python dependencies and `cloc`.

1.  **With `direnv` (recommended for seamless integration):**
    If you have `direnv` installed, navigate to the `ploc` directory, and it will automatically load the environment.

2.  **Manually enter the development shell:**
    ```bash
    nix develop
    ```
    This command will set up the environment with all necessary dependencies, including `cloc`, and put you into a shell where `ploc` can be run.

## Usage

To run `ploc`, execute the `__main__.py` script.

```bash
python -m ploc --help
```

### Command Line Arguments

- `--jobs`, `-j`: (Optional) How many `cloc` jobs to run in parallel. Defaults to the number of CPU cores.
- `--output`, `-o`: (Optional) What to output the plot to. Defaults to `plot.png`.
- `--repo`, `-r`: (Optional) Path to the bare Git repository (e.g., `.git` directory). Defaults to `.git`.

### Examples

**Analyze the current repository and save the plot to `plot.png`:**

```bash
python -m ploc
```

**Analyze a specific repository with 4 parallel jobs and save the output to `my_repo_plot.png`:**

```bash
python -m ploc -r /path/to/your/repo/.git -j 4 -o my_repo_plot.png
```

## Output

The script generates a PNG image (default: `plot.png`) showing the lines of code for each detected language across the commits. The X-axis represents the commit order (from the first to the latest), and the Y-axis represents the lines of code.

## Development

Contributions are welcome!
