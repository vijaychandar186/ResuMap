# uv Package Manager Usage Guide

This guide provides a clean and structured overview of using the `uv` package and environment manager in Python projects.

---

## 🚀 Project Setup with uv

### 1. Install `uv`

Install `uv` globally using pip:

```bash
pip install uv
```

### 2. Initialize a New Project (optional)

If you're starting a new project:

```bash
uv init
```

> This will create a `pyproject.toml` file.

### 3. Create a Virtual Environment

```bash
uv venv --python 3.12
```

> This creates a virtual environment in the `.venv/` directory.

### 4. Activate the Virtual Environment

* **macOS/Linux**:

  ```bash
  source .venv/bin/activate
  ```

* **Windows**:

  ```bash
  .venv\Scripts\activate
  ```

### 5. Install Dependencies from `requirements.txt`

```bash
uv add -r requirements.txt
```

> This adds the dependencies to `pyproject.toml` and installs them in the environment.

### 6. Sync with Lockfile (Exact Versions)

```bash
uv sync --frozen
```

> This installs dependencies exactly as listed in `uv.lock`.

---

## 📦 Common uv Commands

* **Add a new dependency**:

  ```bash
  uv add <package>
  ```

* **Update all dependencies**:

  ```bash
  uv sync
  ```

* **Export to `requirements.txt`**:

  ```bash
  uv export > requirements.txt
  ```

* **Run commands in the environment**:

  ```bash
  uv run <command>
  ```

---

## ❗ Troubleshooting

* **Dependency conflicts**:

  Run:

  ```bash
  uv sync
  ```

* **Python version mismatch**:

  Ensure Python 3.12 is installed and correctly referenced in your shell or IDE.

---