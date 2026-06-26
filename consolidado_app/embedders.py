"""
Backends de embeddings para la búsqueda semántica.

Orden de preferencia automático (get_embedder):
  1. fastembed  -> modelo multilingüe local (semántico, recomendado)
  2. OpenAI     -> si existe la variable de entorno OPENAI_API_KEY
  3. hashing    -> fallback offline sin dependencias (lexical, siempre funciona)

Cada embedder expone:
  .name  -> identificador guardado en la BD
  .dim   -> dimensión del vector
  .embed(texts: list[str]) -> list[list[float]]   (vectores L2-normalizados)
"""
from __future__ import annotations
import hashlib
import math
import os
import re
import unicodedata


def _l2(v):
    n = math.sqrt(sum(x * x for x in v)) or 1.0
    return [x / n for x in v]


def _norm_text(s: str) -> str:
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode().lower()
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9 ]", " ", s)).strip()


class HashingEmbedder:
    """Embedding offline determinista basado en hashing de n-gramas de caracteres.

    No es semántico (es léxico/fuzzy), pero no requiere red ni dependencias y es
    útil para buscar nombres con errores de OCR. Sirve de respaldo garantizado.
    """

    name = "hashing-ngram-256"
    dim = 256

    def __init__(self, dim: int = 256, ngram=(3, 4, 5)):
        self.dim = dim
        self.name = f"hashing-ngram-{dim}"
        self.ngram = ngram

    def _vec(self, text: str):
        t = f" {_norm_text(text)} "
        v = [0.0] * self.dim
        for n in self.ngram:
            if len(t) < n:
                continue
            for i in range(len(t) - n + 1):
                g = t[i:i + n]
                h = int(hashlib.md5(g.encode()).hexdigest(), 16)
                idx = h % self.dim
                sign = 1.0 if (h >> 8) & 1 else -1.0
                v[idx] += sign
        return _l2(v)

    def embed(self, texts):
        return [self._vec(t) for t in texts]


class FastEmbedEmbedder:
    """Embeddings semánticos locales con fastembed (ONNX, sin API key)."""

    def __init__(self, model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"):
        from fastembed import TextEmbedding  # import perezoso
        self._m = TextEmbedding(model_name=model_name)
        self.name = "fastembed:" + model_name.split("/")[-1]
        # descubrir dimensión con una muestra
        self.dim = len(next(iter(self._m.embed(["dimension probe"]))))

    def embed(self, texts):
        return [_l2(list(map(float, e))) for e in self._m.embed(list(texts))]


class OpenAIEmbedder:
    """Embeddings vía API de OpenAI (requiere OPENAI_API_KEY)."""

    def __init__(self, model="text-embedding-3-small"):
        from openai import OpenAI  # import perezoso
        self._c = OpenAI()
        self._model = model
        self.name = "openai:" + model
        self.dim = len(self._c.embeddings.create(model=model, input="probe").data[0].embedding)

    def embed(self, texts):
        out = self._c.embeddings.create(model=self._model, input=list(texts)).data
        return [_l2(d.embedding) for d in out]


def get_embedder(prefer: str | None = None):
    """Devuelve el mejor embedder disponible.

    prefer: 'fastembed' | 'openai' | 'hashing' | None (auto)
    """
    order = [prefer] if prefer else []
    order += ["fastembed", "openai", "hashing"]
    for choice in order:
        if not choice:
            continue
        try:
            if choice == "fastembed":
                return FastEmbedEmbedder()
            if choice == "openai":
                if not os.environ.get("OPENAI_API_KEY"):
                    continue
                return OpenAIEmbedder()
            if choice == "hashing":
                return HashingEmbedder()
        except Exception as e:  # noqa: BLE001
            print(f"[embedders] '{choice}' no disponible: {e}")
            continue
    return HashingEmbedder()
