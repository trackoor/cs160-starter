<img src="logo/cs160.svg" alt="UC Santa Barbara CS160 Compilers, Fall 2026. Instructor Yu Feng, TA Hanzhi Liu." width="100%">

-----------------

[![Build Status](https://github.com/trackoor/cs160-starter/actions/workflows/ci.yml/badge.svg)](https://github.com/trackoor/cs160-starter/actions/workflows/ci.yml)

This is the starter code of the ChocoPy compiler you build in [CS160 Compilers](https://github.com/fredfeng/CS160) at [UC Santa Barbara](https://www.cs.ucsb.edu). The compiler, written in Python, translates programs in the course's subset of [ChocoPy](https://chocopy.org), a statically typed subset of Python, into LLVM IR, which `clang` compiles together with a small C runtime into a native executable. This system was developed for educational purposes and should not be used in production environments.

Each of the six programming assignments adds to the same compiler. The assignment writeups are posted in the course repository under [`assignments/`](https://github.com/fredfeng/CS160/tree/main/assignments), and the language your compiler accepts is specified in [`chocopy/SPEC.md`](https://github.com/fredfeng/CS160/blob/main/chocopy/SPEC.md).

```console
$ echo 'print(160)' > hello.py
$ python3 -m compiler run hello.py
160
```

**WARNING: DO NOT DIRECTLY FORK THIS REPO. DO NOT PUSH ASSIGNMENT SOLUTIONS PUBLICLY. THIS IS AN ACADEMIC INTEGRITY VIOLATION UNDER THE [UCSB ACADEMIC INTEGRITY POLICY](https://studentconduct.sa.ucsb.edu/academic-integrity), AND SO IS SHARING YOUR SOLUTION IN ANY OTHER WAY.**

## Cloning this Repository

The following instructions are adapted from the GitHub documentation on [duplicating a repository](https://docs.github.com/en/github/creating-cloning-and-archiving-repositories/creating-a-repository-on-github/duplicating-a-repository). The procedure below walks you through creating a private repository that you can use for development.

1. [Create a new repository](https://github.com/new) under your account. Pick a name (e.g. `cs160-private`) and select **Private** for the repository visibility level.
2. On your development machine, create a bare clone of the starter repository:
   ```console
   $ git clone --bare https://github.com/trackoor/cs160-starter.git cs160-public
   ```
3. Next, [mirror](https://git-scm.com/docs/git-push#Documentation/git-push.txt---mirror) the starter repository to your own private repository. Suppose your GitHub name is `student` and your repository name is `cs160-private`. The procedure for mirroring the repository is then:
   ```console
   $ cd cs160-public

   # If you pull / push over HTTPS
   $ git push https://github.com/student/cs160-private.git main

   # If you pull / push over SSH
   $ git push git@github.com:student/cs160-private.git main
   ```
   This copies everything in the starter repository to your own private repository. You can now delete your local clone of the starter repository:
   ```console
   $ cd ..
   $ rm -rf cs160-public
   ```
4. Clone your private repository to your development machine:
   ```console
   # If you pull / push over HTTPS
   $ git clone https://github.com/student/cs160-private.git

   # If you pull / push over SSH
   $ git clone git@github.com:student/cs160-private.git
   ```
5. Add the starter repository as a second remote. This allows you to retrieve each assignment as it is released, and any fixes, and merge them with your solution throughout the quarter:
   ```console
   $ git remote add public https://github.com/trackoor/cs160-starter.git
   ```
   You can verify that the remote was added with the following command:
   ```console
   $ git remote -v
   origin	https://github.com/student/cs160-private.git (fetch)
   origin	https://github.com/student/cs160-private.git (push)
   public	https://github.com/trackoor/cs160-starter.git (fetch)
   public	https://github.com/trackoor/cs160-starter.git (push)
   ```
6. You can now pull in changes from the starter repository as needed with:
   ```console
   $ git pull --no-rebase public main
   ```
7. **Disable GitHub Actions** from the project settings of your private repository; otherwise, you may run out of GitHub Actions quota.
   ```
   Settings > Actions > General > Actions permissions > Disable actions.
   ```

We suggest working on your assignments in separate branches. If you do not understand how Git branches work, [learn how](https://git-scm.com/book/en/v2/Git-Branching-Basic-Branching-and-Merging). If you fail to do this, you might lose all your work at some point in the quarter, and nobody will be able to help you.

## Build

We recommend developing your compiler on Ubuntu 24.04, or macOS (M1/M2/Intel). On Windows, use WSL 2 with Ubuntu 24.04. We do not support any other environments (i.e., do not come to office hours to debug them). The grading environment runs Ubuntu 24.04, with Python 3.12 and clang 18.

### Linux (Recommended) / macOS (Development Only)

To ensure that you have the proper packages on your machine, run the following script to automatically install them:

```console
# Linux
$ sudo build_support/packages.sh
# macOS
$ build_support/packages.sh
```

It installs Python 3.11 or later, clang 15 or later, and the `ruff` formatter and linter. Then check that everything works:

```console
$ python3 tools/doctor.py
```

Your compiler needs no build step. To compile and run a program:

```console
$ python3 -m compiler run prog.py
```

To print the LLVM IR instead, use `python3 -m compiler ll prog.py`; `python3 -m compiler --help` lists every command. To run the tests of every assignment released so far, together with your own tests in `test/mine`:

```console
$ make check-tests
```

Each writeup describes the tests, the design document and the submission of its assignment.

There are some differences between macOS and Linux (e.g., Apple's clang compiles LLVM IR that is not in valid SSA form, which LLVM's own verifier would reject) that might cause test cases to produce different results on different platforms. Check your IR with `--verify` (for example `python3 tools/difftest.py --verify test/pa1`), and use a Linux machine to reproduce a result from the grading environment whenever possible.
