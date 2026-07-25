#!/usr/bin/env python3
"""Build the deterministic canonical JAX notebook-native exception."""

from __future__ import annotations

from pathlib import Path

import nbformat

from tools.notebook_helpers import code, deterministic_cell_id, markdown, notebook

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "notebooks" / "instructor" / "extensions"


def write_notebook(filename: str, content: nbformat.NotebookNode) -> None:
    for index, cell in enumerate(content.cells):
        cell["id"] = deterministic_cell_id(f"extensions/{filename}", index)
    nbformat.write(content, OUTPUT / filename)


def build_jax_bridge() -> None:
    metadata = {
        "assessed": False,
        "concept_ids": ["DP-JAX-01", "DP-JAX-02", "DP-JAX-03"],
        "difficulty": "D2",
        "duration_minutes": 70,
        "execution_profile": "full",
        "language": "en",
        "outcomes": ["LO8", "LO11"],
        "prerequisites": ["NumPy arrays", "vectorisation", "stable loss functions"],
        "priority": "P2",
    }
    cells = [
        markdown(
            "# JAX transformations for data scientists\n\n"
            "**P2 Extension · D2 Independent · 70 minutes · not assessed**\n\n"
            "This compact bridge covers arrays, pure functions, explicit random keys, automatic "
            "differentiation, compilation, and vectorisation. It deliberately excludes neural "
            "network construction, PyTrees, Optax, accelerators, and long training loops."
        ),
        code("import jax\nimport jax.numpy as jnp\nimport numpy as np", ["setup"]),
        markdown(
            "## Pure numerical function\n\n"
            "JAX transformations operate most predictably on functions whose outputs depend only "
            "on explicit inputs. The small linear mean-squared error is our complete oracle."
        ),
        code(
            "def mse_loss(theta, x, y):\n"
            "    prediction = x @ theta\n"
            "    return jnp.mean((prediction - y) ** 2)\n\n"
            "x = jnp.array([[1.0, -1.0], [1.0, 0.0], [1.0, 2.0], [1.0, 3.0]])\n"
            "true_theta = jnp.array([0.5, 1.25])",
            ["setup"],
        ),
        markdown(
            "## Explicit randomness\n\n"
            "A random key is data: split it and pass the subkey that owns each random operation. "
            "Reusing a key repeats the same values and is usually an error."
        ),
        code(
            "def noisy_targets(key, x, theta, scale=0.05):\n"
            "    key, noise_key = jax.random.split(key)\n"
            "    noise = scale * jax.random.normal(noise_key, shape=(x.shape[0],))\n"
            "    return key, x @ theta + noise\n\n"
            "key = jax.random.key(20260718)\n"
            "key, y = noisy_targets(key, x, true_theta)\n"
            "assert y.shape == (4,)\n"
            "assert jnp.isfinite(y).all()",
            ["solution", "test-public"],
            "def noisy_targets(key, x, theta, scale=0.05):\n"
            "    # TODO: split the key and use one new key for normal noise.\n"
            "    raise NotImplementedError\n\n"
            "key = jax.random.key(20260718)\n"
            "key, y = noisy_targets(key, x, true_theta)\n",
        ),
        markdown(
            "## Differentiate and verify\n\n"
            "Automatic differentiation is executable chain-rule bookkeeping, not independent "
            "evidence that a model or implementation is correct. Compare it with a finite-difference "
            "oracle on a small deterministic input."
        ),
        code(
            "def central_difference(function, theta, step=1e-3):\n"
            "    basis = jnp.eye(theta.size, dtype=theta.dtype)\n"
            "    return jax.vmap(\n"
            "        lambda direction: (function(theta + step * direction)\n"
            "                           - function(theta - step * direction)) / (2 * step)\n"
            "    )(basis)\n\n"
            "theta = jnp.array([0.0, 0.0])\n"
            "value, gradient = jax.value_and_grad(mse_loss)(theta, x, y)\n"
            "finite_difference = central_difference(lambda t: mse_loss(t, x, y), theta)\n"
            "assert jnp.isfinite(value)\n"
            "assert jnp.allclose(gradient, finite_difference, atol=2e-3, rtol=2e-3)",
            ["solution", "test-public"],
            "def central_difference(function, theta, step=1e-3):\n"
            "    # TODO: return a central-difference estimate for every parameter.\n"
            "    raise NotImplementedError\n\n"
            "theta = jnp.array([0.0, 0.0])\n"
            "value, gradient = jax.value_and_grad(mse_loss)(theta, x, y)\n"
            "finite_difference = central_difference(lambda t: mse_loss(t, x, y), theta)\n",
        ),
        markdown(
            "## Compile and vectorise\n\n"
            "`jit` specialises a pure function for input shapes and dtypes. The first call includes "
            "compilation, so a one-call wall-clock comparison is misleading. `vmap` introduces a "
            "batch axis without writing a Python loop."
        ),
        code(
            "compiled_gradient = jax.jit(jax.grad(mse_loss))\n"
            "compiled_value = compiled_gradient(theta, x, y)\n\n"
            "def example_loss(theta, row, target):\n"
            "    return (row @ theta - target) ** 2\n\n"
            "per_example_loss = jax.vmap(example_loss, in_axes=(None, 0, 0))\n"
            "per_example_gradient = jax.vmap(jax.grad(example_loss), in_axes=(None, 0, 0))\n"
            "losses = per_example_loss(theta, x, y)\n"
            "gradients = per_example_gradient(theta, x, y)\n"
            "assert jnp.allclose(losses.mean(), mse_loss(theta, x, y))\n"
            "assert jnp.allclose(gradients.mean(axis=0), gradient)\n"
            "assert jnp.allclose(compiled_value, gradient)\n"
            "{'loss': float(value), 'gradient': np.asarray(gradient), "
            "'batch_shape': gradients.shape}",
            ["solution", "test-public"],
            "compiled_gradient = jax.jit(jax.grad(mse_loss))\n"
            "compiled_value = compiled_gradient(theta, x, y)\n\n"
            "def example_loss(theta, row, target):\n"
            "    return (row @ theta - target) ** 2\n\n"
            "# TODO: vectorise example_loss and its gradient over rows and targets.\n"
            "per_example_loss = None\n"
            "per_example_gradient = None\n",
        ),
        markdown(
            "## Transfer and boundary\n\n"
            "Replace mean-squared error with the stable binary logistic loss from the core course. "
            "Verify one gradient, then compare scalar and vectorised per-example losses. Record shape, "
            "dtype, key ownership, and the compilation boundary. Continue with model construction, "
            "PyTrees, Optax, accelerators, and physics-informed objectives in Scientific Machine "
            "Learning—not in the required Data Processing assessment path."
        ),
    ]
    write_notebook("jax-transformations.ipynb", notebook(metadata, cells))


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    build_jax_bridge()
    print("Built the JAX notebook-native source")


if __name__ == "__main__":
    main()
