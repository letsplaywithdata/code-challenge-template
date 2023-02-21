import numpy
import psycopg2
from psycopg2.extensions import register_adapter, AsIs


# Postgresql database Adapter method
def adapt_numpy_float64(numpy_float64):
    return AsIs(numpy_float64)


# Postgresql database Adapter method
def adapt_numpy_int64(numpy_int64):
    return AsIs(numpy_int64)


# Postgresql database Adapter method
def nan_to_null(f, _NULL=psycopg2.extensions.AsIs('NULL'), _Float=psycopg2.extensions.Float):
    if f != f:
        return _NULL
    else:
        return _Float(f)


# Method to initialize Postgresql database Adapter
def create_adapters():
    register_adapter(numpy.float64, adapt_numpy_float64)
    register_adapter(numpy.int64, adapt_numpy_int64)
    register_adapter(float, nan_to_null)
