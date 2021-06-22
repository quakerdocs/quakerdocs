/*
 * A vector helper class used by search.c
 */

#pragma once

#include <memory.h>

/*
 * A vector structure, also known as an array list. A vector reallocates
 * memory as the size of the container increases.
 */
typedef struct VECTOR {
   int size;
   int capacity;
   const void *data[];
} vector_t;

/*
 * Create a new vector.
 *
 * initial_size: the initial capacity of the vector.
 *
 * returns: the freshly allocated vector.
 */
static inline vector_t *vector_make(int initial_size) {
    vector_t *v = malloc(sizeof (vector_t) + initial_size * sizeof (const void *));
    v->size = 0;
    v->capacity = 8;
    return v;
}

/*
 * Free a vector from memory.
 *
 * v: the vector to deallocate.
 */
static inline void vector_free(vector_t *v) {
    free(v);
}

/*
 * Get an element at a specific point from a vector.
 *
 * v: the vector to push the element to.
 * i: the index of the element to return.
 *
 * returns: the element at index i.
 */
static inline const void *vector_at(vector_t *v, int i) {
    return v->data[i];
}

/*
 * Push a new element to the back of a vector.
 *
 * v: the vector to push the element to.
 * element: the element to put on the stack.
 *
 * returns: the possibly reallocated vector.
 */
static inline vector_t *vector_push(vector_t *v, const void *element) {
    if (v->size >= v->capacity) {
        v->capacity *= 2;
        v = realloc(v, sizeof (vector_t) + (v->capacity) * sizeof (const void *));
    }
    v->data[v->size++] = element;
    return v;
}

/*
 * Pop the last element from a vector.
 *
 * v: the vector to pop the element from.
 *
 * returns: the previously last element in the array.
 */
static inline const void *vector_pop(vector_t *v) {
    return vector_at(v, --v->size);
}

/*
 * Clear the vectors elements
 *
 * v: the vector to remove all elements from.
 */
static inline void vector_clear(vector_t *v) {
    v->size = 0;
}

/*
 * Return the size of the vector.
 *
 * v: the vector to get the size from.
 *
 * returns: the size of the vector.
 */
static inline int vector_size(vector_t *v) {
    return v->size;
}

/*
 * Return if the vector is empty.
 *
 * v: the possibly empty vector.
 *
 * returns: true if the vector is empty, false otherwise.
 */
static inline int vector_empty(vector_t *v) {
    return v->size == 0;
}
