//===----------------------------------------------------------------------===//
//
//                         CS160 ChocoPy Compiler
//
// runtime.c
//
// Identification: runtime/runtime.c
//
// Copyright (c) 2026, CS160 Course Staff, UC Santa Barbara
//
//===----------------------------------------------------------------------===//
#include <signal.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/**
 * The layout of a string on the heap: its length, then its characters. A list
 * of T has the same layout, { i32, [0 x T] }. None is the null pointer.
 */
typedef struct {
  int32_t len;
  char data[];
} cp_str;

/**
 * @brief Print an int and a newline, as CPython's print does.
 * @param x the value
 */
void cp_print_int(int32_t x) { printf("%d\n", x); }

/**
 * @brief Print a bool as True or False, and a newline.
 * @param b the value, widened from i1 to i32 with zext
 */
void cp_print_bool(int32_t b) { puts(b ? "True" : "False"); }

/**
 * @brief Print a string and a newline.
 * @param s the string
 */
void cp_print_str(const cp_str *s) {
  fwrite(s->data, 1, (size_t)s->len, stdout);
  putchar('\n');
}

/**
 * @brief Stop the program with a ChocoPy run-time error. The output printed so
 * far is flushed first, and the message goes to standard error.
 * @param code the exit code
 * @param message the error message
 */
static void cp_abort(int code, const char *message) {
  fflush(stdout);
  fprintf(stderr, "%s\n", message);
  exit(code);
}

/** @brief Exit with code 1, "Invalid argument": len of a list that is None. */
void cp_error_arg(void) { cp_abort(1, "Invalid argument"); }

/** @brief Exit with code 2, "Division by zero". */
void cp_error_div(void) { cp_abort(2, "Division by zero"); }

/** @brief Exit with code 3, "Index out of bounds". */
void cp_error_oob(void) { cp_abort(3, "Index out of bounds"); }

/** @brief Exit with code 4, "Operation on None". */
void cp_error_none(void) { cp_abort(4, "Operation on None"); }

/**
 * @brief Allocate zeroed heap memory. Exits with code 5, "Out of memory", if
 * the allocation fails.
 * @param bytes the size of the object
 * @return the object
 */
void *cp_alloc(int64_t bytes) {
  void *p = calloc(1, bytes > 0 ? (size_t)bytes : 1);
  if (!p) cp_abort(5, "Out of memory");
  return p;
}

/**
 * @brief Compare two strings.
 * @param a a string
 * @param b another string
 * @return 1 if they hold the same characters, else 0
 */
int32_t cp_str_eq(const cp_str *a, const cp_str *b) {
  return a->len == b->len && memcmp(a->data, b->data, (size_t)a->len) == 0;
}

/**
 * @brief On a crash, flush the output printed so far, then let the signal end
 * the program as it would have. Without this, output still in the buffer is
 * lost when standard output is a pipe, as it is under the test tools.
 * @param sig the signal
 */
static void cp_crashed(int sig) {
  signal(sig, SIG_DFL);
  fflush(stdout);
  raise(sig);
}

/** @brief Install cp_crashed before main runs. */
__attribute__((constructor)) static void cp_install_crash_handler(void) {
  int signals[] = {SIGSEGV, SIGBUS, SIGFPE, SIGILL, SIGTRAP, SIGABRT};
  for (size_t i = 0; i < sizeof signals / sizeof signals[0]; i++) signal(signals[i], cp_crashed);
}
