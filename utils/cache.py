import streamlit as st
import functools
import hashlib
import json
from typing import Any, Callable


# ----------------------------------------
# 🔑 GENERATE CACHE KEY
# ----------------------------------------
def generate_cache_key(*args, **kwargs) -> str:
    """
    Create a deterministic hash key from inputs.
    """
    try:
        data = json.dumps(
            {"args": args, "kwargs": kwargs},
            sort_keys=True,
            default=str
        )
    except Exception:
        data = str(args) + str(kwargs)

    return hashlib.sha256(data.encode()).hexdigest()


# ----------------------------------------
# ⚡ GENERIC CACHE DECORATOR (IN-MEMORY)
# ----------------------------------------
_memory_cache = {}

def cache_function(func: Callable):
    """
    Simple Python-level memoization.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        key = generate_cache_key(*args, **kwargs)

        if key in _memory_cache:
            return _memory_cache[key]

        result = func(*args, **kwargs)
        _memory_cache[key] = result
        return result

    return wrapper


# ----------------------------------------
# 📦 STREAMLIT DATA CACHE WRAPPER
# ----------------------------------------
def st_cache_data_wrapper(func: Callable):
    """
    Wrap a function with Streamlit cache_data.
    """

    @st.cache_data(show_spinner=False)
    def cached_func(*args, **kwargs):
        return func(*args, **kwargs)

    return cached_func


# ----------------------------------------
# 🧠 STREAMLIT RESOURCE CACHE (MODELS)
# ----------------------------------------
def st_cache_resource_wrapper(func: Callable):
    """
    Use for heavy objects (LLM, models).
    """

    @st.cache_resource(show_spinner=False)
    def cached_func(*args, **kwargs):
        return func(*args, **kwargs)

    return cached_func


# ----------------------------------------
# 🔁 MANUAL CACHE SET/GET
# ----------------------------------------
def cache_set(key: str, value: Any):
    _memory_cache[key] = value


def cache_get(key: str):
    return _memory_cache.get(key)


def cache_clear():
    _memory_cache.clear()


# ----------------------------------------
# 🧪 CACHE STATUS
# ----------------------------------------
def cache_info():
    return {
        "items": len(_memory_cache),
        "keys": list(_memory_cache.keys())[:10]
    }


# ----------------------------------------
# 🎯 FILE-BASED CACHE KEY
# ----------------------------------------
def file_based_cache_key(file_bytes: bytes) -> str:
    """
    Generate cache key from file content.
    """
    return hashlib.sha256(file_bytes).hexdigest()


# ----------------------------------------
# ⚡ COMBINED CACHE DECORATOR (STREAMLIT + MEMORY)
# ----------------------------------------
def hybrid_cache(func: Callable):
    """
    First checks memory cache, then Streamlit cache.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        key = generate_cache_key(*args, **kwargs)

        if key in _memory_cache:
            return _memory_cache[key]

        result = func(*args, **kwargs)
        _memory_cache[key] = result
        return result

    return wrapper
