#include <Python.h>
#include <sparsehash/sparse_hash_set>
#include "MurmurHash3.h"

using google::sparse_hash_set;

struct Key {
    Key() : len(0), data(0) {}
    Key(uint32_t l, void *d) : len(l), data(d) {}
    uint32_t len;
    void *data;
};

struct Hasher {
    uint32_t seed;
    Hasher(void) : seed(1) {}
    Hasher(uint32_t s) : seed(s) {}
    size_t operator()(const Key &k) const {
        uint32_t out;
        if (k.len == 0 || k.len == 0xffffffff)
            return 0;
        MurmurHash3_x86_32(k.data, k.len, seed, &out);
        return out;
    }
};

struct Equaler {
    Equaler(void) {}
    bool operator()(const Key &a, const Key &b) const {
        if (a.len != b.len)
            return false;
        if (a.len == 0 || a.len == 0xffffffff)
            return true;
        return memcmp(a.data, b.data, a.len) == 0;
    }
};

typedef sparse_hash_set<Key, Hasher, Equaler> SSSet;

typedef struct {
    PyObject_HEAD
    SSSet *set;
} SparseStrSet;

static PyObject *
SparseStrSet_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
    SparseStrSet *self;
    if ((self = (SparseStrSet *)type->tp_alloc(type, 0))) {
        self->set = new SSSet();
    }
    return (PyObject *)self;
}

static void
SparseStrSet_dealloc(SparseStrSet *self)
{
    delete self->set;
    self->ob_type->tp_free((PyObject *)self);
}

static int
SparseStrSet_init(SparseStrSet *self, PyObject *args, PyObject *kwds)
{
    // PyObject *list;
    // if (!PyArg_ParseTuple(args, "O", &list))
    //     return NULL;
    // PyObject *item;
    // PyObject *iter = PyObject_GetIter(list);
    // if (!iter) {
    //     // todo
    // }
    // while (item = PyIter_Next(iter)) {
    //     Py_DECREF(item);
    // }
    // Py_DECREF(iterator);
    // if (PyErr_Occurred()) {
    //     // todo
    // }
    return 0;
}

static PyObject *
SparseStrSet_add(SparseStrSet *self, PyObject *args)
{
    const char *ps = NULL;
    int pl;
    if (!PyArg_ParseTuple(args, "et#", "utf-8", &ps, &pl))
        return NULL;
    if (ps) {
        Key key;
        key.data = malloc(pl);
        key.len = (uint32_t)pl;
        memcpy(key.data, ps, pl);
        self->set->insert(key);
        PyMem_Free((void *)ps);
    }
    Py_RETURN_NONE;
}

static PyObject *
SparseStrSet_contains(SparseStrSet *self, PyObject *args)
{
    bool res = false;
    const char *ps = NULL;
    int pl;
    if (!PyArg_ParseTuple(args, "et#", "utf-8", &ps, &pl))
        return NULL;
    if (ps) {
        Key key;
        key.data = (void *)ps;
        key.len = (uint32_t)pl;
        SSSet::const_iterator it = self->set->find(key);
        res = (it != self->set->end());
        PyMem_Free((void *)ps);
    }
    if (res) {
        Py_RETURN_TRUE;
    } else {
        Py_RETURN_FALSE;
    }
}

static PyMethodDef SparseStrSet_methods[] = {
    { "add", (PyCFunction)SparseStrSet_add, METH_VARARGS,
      "Add a string to the set." },
    { "contains", (PyCFunction)SparseStrSet_contains, METH_VARARGS,
      "Check if string is a member of the set." },
    { NULL },
};

static PyTypeObject SparseStrSetType = {
    PyObject_HEAD_INIT(NULL)
    0,                                /* ob_size */
    "sparsehash.SparseStrSet",        /* tp_name */
    sizeof(SparseStrSet),             /* tp_basicsize */
    0,                                /* tp_itemsize */
    (destructor)SparseStrSet_dealloc, /* tp_dealloc */
    0,                                /* tp_print */
    0,                                /* tp_getattr */
    0,                                /* tp_setattr */
    0,                                /* tp_compare */
    0,                                /* tp_repr */
    0,                                /* tp_as_number */
    0,                                /* tp_as_sequence */
    0,                                /* tp_as_mapping */
    0,                                /* tp_hash  */
    0,                                /* tp_call */
    0,                                /* tp_str */
    0,                                /* tp_getattro */
    0,                                /* tp_setattro */
    0,                                /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT,               /* tp_flags */
    "Google SparseHash Set (may only contain strings without null chars)",
    0,                                /* tp_traverse */
    0,                                /* tp_clear */
    0,                                /* tp_richcompare */
    0,                                /* tp_weaklistoffset */
    0,                                /* tp_iter */
    0,                                /* tp_iternext */
    SparseStrSet_methods,             /* tp_methods */
    0,                                /* tp_members */
    0,                                /* tp_getset */
    0,                                /* tp_base */
    0,                                /* tp_dict */
    0,                                /* tp_descr_get */
    0,                                /* tp_descr_set */
    0,                                /* tp_dictoffset */
    (initproc)SparseStrSet_init,      /* tp_init */
    0,                                /* tp_alloc */
    SparseStrSet_new,                 /* tp_new */
};

///////////////////////////////////////////////////////////////////////////////

static PyObject *hello(PyObject *self, PyObject *args)
{
    const char *name;
    if (!PyArg_ParseTuple(args, "s", &name))
        return NULL;
    printf("Hello %s!\n", name);
    Py_RETURN_NONE;
}

static PyMethodDef methods[] = {
    { "hello", hello, METH_VARARGS, "greet somebody" },
    { NULL, NULL, 0, NULL },
};

///////////////////////////////////////////////////////////////////////////////

PyMODINIT_FUNC
initsparsehash(void)
{
    PyObject *mod;
    if (PyType_Ready(&SparseStrSetType) < 0)
        return;
    mod = Py_InitModule3("sparsehash", methods, "Google SparseHash Wrapper");
    Py_INCREF(&SparseStrSetType);
    PyModule_AddObject(mod, "SparseStrSet", (PyObject *)&SparseStrSetType);
}
