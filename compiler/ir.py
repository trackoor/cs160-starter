# ===----------------------------------------------------------------------=== #
#
#                         CS160 ChocoPy Compiler
#
# ir.py
#
# Identification: compiler/ir.py
#
# Copyright (c) 2026, CS160 Course Staff, UC Santa Barbara
#
# ===----------------------------------------------------------------------=== #
"""The course's LLVM IR as a control-flow graph, for your optimization passes (PA5, PA6).

`parse(text)` reads the LLVM IR the course's code generators print and returns a
Module; `Module.render()` prints it back. A Function is a list of Blocks; a
Block is a label and a list of Instrs, the last of which is its terminator.

    module = parse(text)
    for fn in module.functions:
        for block in fn.blocks:
            for instr in block.instrs:
                ...  instr.result, instr.op, instr.uses(), ...
        fn.predecessors()          # {label: [labels of predecessor blocks]}
        fn.verify()                # [] if the function is well formed SSA

Only the instructions the course emits are understood: alloca, load, store,
integer arithmetic and bitwise operations, icmp, select, zext, sext, trunc,
ptrtoint, getelementptr, call, br, ret, unreachable and phi.
"""

import re

NAME = r"[%@][-\w$.]+"
BINARY = {"add", "sub", "mul", "sdiv", "srem", "udiv", "urem", "shl", "lshr", "ashr", "and", "or", "xor"}
CASTS = {"zext", "sext", "trunc", "ptrtoint", "inttoptr", "bitcast"}
TERMINATORS = {"br", "ret", "unreachable"}


class IRError(Exception):
    """IRError is raised for IR that this module cannot read or print."""


class Instr:
    """
    Instr is one instruction. `result` is the value it defines, such as `%t3`,
    or None; `op` is its opcode. The other fields depend on `op`:


    alloca       type
    load         type, args=[pointer]
    store        type, args=[value, pointer]
    binary ops   type, args=[a, b]
    icmp         pred, type, args=[a, b]
    select       type, args=[condition, a, b]
    casts        type (source), to_type, args=[value]
    getelementptr type (source element type), args=[pointer, index...], index_types
    call         type (return type), callee, args, arg_types
    br           args=[] and targets=[label], or args=[condition] and targets=[then, else]
    ret          type ('void' or a type), args=[] or [value]
    phi          type, incoming=[(value, label), ...]
    """

    def __init__(self, op, result=None, type=None, args=None, **extra):
        self.op = op
        self.result = result
        self.type = type
        self.args = list(args or [])
        self.pred = extra.get("pred")
        self.to_type = extra.get("to_type")
        self.callee = extra.get("callee")
        self.arg_types = list(extra.get("arg_types") or [])
        self.index_types = list(extra.get("index_types") or [])
        self.targets = list(extra.get("targets") or [])
        self.incoming = list(extra.get("incoming") or [])

    def uses(self) -> list[str]:
        """
        @brief List the values this instruction reads.

        @return the operands, and a phi's incoming values; not labels or the callee
        """
        if self.op == "phi":
            return [value for value, _ in self.incoming]
        return list(self.args)

    def replace_uses(self, old: str, new: str) -> None:
        """
        @brief Replace every use of one value in this instruction by another.

        @param old the value to replace, such as `%t3`
        @param new the replacement, such as `%t1` or `5`
        """
        self.args = [new if a == old else a for a in self.args]
        self.incoming = [(new if v == old else v, label) for v, label in self.incoming]

    def is_terminator(self) -> bool:
        """@return True for `br`, `ret` and `unreachable`"""
        return self.op in TERMINATORS

    def has_side_effects(self) -> bool:
        """
        @brief Tell whether the instruction must stay even when its result is unused.

        @return True for memory writes, calls and terminators
        """
        return self.op in ("store", "call") or self.is_terminator()

    def __str__(self) -> str:
        op = self.op
        if op == "alloca":
            text = f"alloca {self.type}"
        elif op == "load":
            text = f"load {self.type}, ptr {self.args[0]}"
        elif op == "store":
            text = f"store {self.type} {self.args[0]}, ptr {self.args[1]}"
        elif op in BINARY:
            text = f"{op} {self.type} {self.args[0]}, {self.args[1]}"
        elif op == "icmp":
            text = f"icmp {self.pred} {self.type} {self.args[0]}, {self.args[1]}"
        elif op == "select":
            text = f"select i1 {self.args[0]}, {self.type} {self.args[1]}, {self.type} {self.args[2]}"
        elif op in CASTS:
            text = f"{op} {self.type} {self.args[0]} to {self.to_type}"
        elif op == "getelementptr":
            indices = "".join(f", {t} {v}" for t, v in zip(self.index_types, self.args[1:]))
            text = f"getelementptr {self.type}, ptr {self.args[0]}{indices}"
        elif op == "call":
            args = ", ".join(f"{t} {v}" for t, v in zip(self.arg_types, self.args))
            text = f"call {self.type} {self.callee}({args})"
        elif op == "br":
            if self.args:
                text = f"br i1 {self.args[0]}, label %{self.targets[0]}, label %{self.targets[1]}"
            else:
                text = f"br label %{self.targets[0]}"
        elif op == "ret":
            text = "ret void" if self.type == "void" else f"ret {self.type} {self.args[0]}"
        elif op == "unreachable":
            text = "unreachable"
        elif op == "phi":
            pairs = ", ".join(f"[ {v}, %{label} ]" for v, label in self.incoming)
            text = f"phi {self.type} {pairs}"
        else:
            raise IRError(f"cannot print {op}")
        return f"{self.result} = {text}" if self.result else text


class Block:
    """Block is a label and a list of instructions, the last of which is its terminator."""

    def __init__(self, label: str):
        self.label = label
        self.instrs: list[Instr] = []

    @property
    def terminator(self) -> Instr | None:
        """@return the block's terminator, or None if it has none"""
        return self.instrs[-1] if self.instrs and self.instrs[-1].is_terminator() else None

    def successors(self) -> list[str]:
        """@return the labels of the blocks the terminator branches to"""
        t = self.terminator
        return list(t.targets) if t is not None and t.op == "br" else []

    def phis(self) -> list[Instr]:
        """@return the phis at the top of the block"""
        return [i for i in self.instrs if i.op == "phi"]


class Function:
    """Function is one function's control-flow graph; its first block is the entry block."""

    def __init__(self, name: str, return_type: str, params: list[tuple[str, str]]):
        self.name = name
        self.return_type = return_type
        self.params = params  # [(type, '%name'), ...]
        self.blocks: list[Block] = []

    def block(self, label: str) -> Block:
        """
        @brief Find a block by its label.

        @param label the label
        @return the block
        @throws IRError if there is none
        """
        for b in self.blocks:
            if b.label == label:
                return b
        raise IRError(f"@{self.name} has no block {label}")

    def predecessors(self) -> dict[str, list[str]]:
        """@return for each block's label, the labels of the blocks that branch to it"""
        preds = {b.label: [] for b in self.blocks}
        for b in self.blocks:
            for s in b.successors():
                if s not in preds:
                    raise IRError(f"@{self.name}: block {b.label} branches to missing block {s}")
                if b.label not in preds[s]:
                    preds[s].append(b.label)
        return preds

    def instructions(self):
        """@return every instruction of the function, block by block"""
        for b in self.blocks:
            yield from b.instrs

    def replace_all_uses(self, old: str, new: str) -> None:
        """
        @brief Replace every use of one value in the function by another.

        @param old the value to replace
        @param new the replacement
        """
        for instr in self.instructions():
            instr.replace_uses(old, new)

    def remove_unreachable_blocks(self) -> None:
        """@brief Delete the blocks that cannot be reached from the entry block, and their phi operands."""
        reachable, stack = set(), [self.blocks[0].label]
        while stack:
            label = stack.pop()
            if label not in reachable:
                reachable.add(label)
                stack.extend(self.block(label).successors())
        self.blocks = [b for b in self.blocks if b.label in reachable]
        for b in self.blocks:
            for phi in b.phis():
                phi.incoming = [(v, label) for v, label in phi.incoming if label in reachable]

    def dominators(self) -> dict[str, set[str]]:
        """
        @brief Compute dominators with the iterative dataflow algorithm.

        This is only for checking your own results; PA5 asks you to compute
        dominators yourself.

        @return for each block's label, the labels of the blocks that dominate it
        """
        labels = [b.label for b in self.blocks]
        preds = self.predecessors()
        dom = {label: set(labels) for label in labels}
        entry = labels[0]
        dom[entry] = {entry}
        changed = True
        while changed:
            changed = False
            for label in labels[1:]:
                incoming = [dom[p] for p in preds[label]]
                new = {label} | (set.intersection(*incoming) if incoming else set())
                if new != dom[label]:
                    dom[label], changed = new, True
        return dom

    def verify(self) -> list[str]:
        """
        @brief Check that the function is well-formed SSA.

        Every block ends with its only terminator, phis come first, every
        branch target exists, every value is defined once, every use is
        dominated by its definition, and every phi has one operand per
        predecessor. `--verify` runs this after each of your passes.

        @return the problems found; [] if there are none
        """
        problems = []
        if not self.blocks:
            return ["the function has no blocks"]
        labels = {b.label for b in self.blocks}
        definitions = {}  # value -> (block label, index)
        for _, name in self.params:
            definitions[name] = (None, -1)
        for b in self.blocks:
            if b.terminator is None:
                problems.append(f"block {b.label} does not end with a terminator")
            for k, instr in enumerate(b.instrs):
                if instr.is_terminator() and k != len(b.instrs) - 1:
                    problems.append(f"block {b.label} has a terminator before its end")
                if instr.op == "phi" and any(i.op != "phi" for i in b.instrs[:k]):
                    problems.append(f"block {b.label} has a phi after another instruction")
                for target in instr.targets:
                    if target not in labels:
                        problems.append(f"block {b.label} branches to missing block {target}")
                if instr.result:
                    if instr.result in definitions:
                        problems.append(f"{instr.result} is defined twice")
                    definitions[instr.result] = (b.label, k)
        if problems:
            return problems
        preds = self.predecessors()
        dom = self.dominators()
        for b in self.blocks:
            for k, instr in enumerate(b.instrs):
                if instr.op == "phi":
                    sources = [label for _, label in instr.incoming]
                    if sorted(sources) != sorted(preds[b.label]):
                        problems.append(
                            f"{instr.result} in {b.label} needs one operand for each predecessor "
                            f"{sorted(preds[b.label])}, has {sorted(sources)}"
                        )
                    for value, label in instr.incoming:
                        where = definitions.get(value) if value.startswith("%") else None
                        if value.startswith("%") and where is None:
                            problems.append(f"{value} is used but never defined")
                        elif where and where[0] is not None and label in dom and where[0] not in dom[label]:
                            problems.append(
                                f"Instruction does not dominate all uses: {value} reaches {instr.result} from {label}"
                            )
                    continue
                for value in instr.uses():
                    if not value.startswith("%"):
                        continue
                    where = definitions.get(value)
                    if where is None:
                        problems.append(f"{value} is used in {b.label} but never defined")
                    elif where[0] is not None and (
                        where[0] not in dom[b.label] or (where[0] == b.label and where[1] >= k)
                    ):
                        problems.append(f"Instruction does not dominate all uses: {value} is used in {b.label}")
        return problems


class Module:
    """Module is a list of functions, with the declarations and globals kept as text."""

    def __init__(self):
        self.header: list[str] = []  # declarations and globals, kept as text
        self.functions: list[Function] = []

    def render(self) -> str:
        """@return the module as LLVM IR text"""
        parts = ["\n".join(self.header)] if self.header else []
        for fn in self.functions:
            params = ", ".join(f"{t} {n}" for t, n in fn.params)
            lines = [f"define {fn.return_type} @{fn.name}({params}) {{"]
            for b in fn.blocks:
                lines.append(f"{b.label}:")
                lines.extend(f"  {i}" for i in b.instrs)
            lines.append("}")
            parts.append("\n".join(lines))
        return "\n\n".join(parts) + "\n"


# Parsing ------------------------------------------------------------------------------


def split_top(text: str) -> list[str]:
    """Split on commas that are not inside { } or [ ] or ( )."""
    parts, depth, current = [], 0, []
    for ch in text:
        if ch in "{[(":
            depth += 1
        elif ch in "}])":
            depth -= 1
        if ch == "," and depth == 0:
            parts.append("".join(current).strip())
            current = []
        else:
            current.append(ch)
    if "".join(current).strip():
        parts.append("".join(current).strip())
    return parts


def typed_value(text: str) -> tuple[str, str]:
    """'i32 %t1' -> ('i32', '%t1'); '{ i32, [0 x i8] } ...' is not expected here."""
    t, v = text.rsplit(None, 1)
    return t.strip(), v.strip()


def parse_instruction(line: str) -> Instr:
    """
    @brief Read one instruction.

    @param line the instruction's text, without indentation
    @return the instruction; raises IRError for an instruction the course does not emit
    """
    m = re.match(rf"({NAME})\s*=\s*(.*)$", line)
    result, body = (m.group(1), m.group(2)) if m else (None, line)
    op, _, rest = body.partition(" ")
    rest = rest.strip()
    if op == "alloca":
        return Instr("alloca", result, rest.split(",")[0].strip())
    if op == "load":
        t, pointer = split_top(rest)
        return Instr("load", result, t.strip(), [pointer.split()[-1]])
    if op == "store":
        value, pointer = split_top(rest)
        t, v = typed_value(value)
        return Instr("store", None, t, [v, pointer.split()[-1]])
    if op in BINARY:
        words = rest.split()
        while words and words[0] in ("nsw", "nuw", "exact"):
            words.pop(0)
        rest = " ".join(words)
        a, b = split_top(rest)
        t, va = typed_value(a)
        return Instr(op, result, t, [va, b.strip()])
    if op == "icmp":
        pred, rest = rest.split(None, 1)
        a, b = split_top(rest)
        t, va = typed_value(a)
        return Instr("icmp", result, t, [va, b.strip()], pred=pred)
    if op == "select":
        c, a, b = split_top(rest)
        _, vc = typed_value(c)
        t, va = typed_value(a)
        _, vb = typed_value(b)
        return Instr("select", result, t, [vc, va, vb])
    if op in CASTS:
        m2 = re.match(r"(.*)\s+to\s+(\S+)$", rest)
        t, v = typed_value(m2.group(1))
        return Instr(op, result, t, [v], to_type=m2.group(2))
    if op == "getelementptr":
        rest = re.sub(r"^inbounds\s+", "", rest)
        parts = split_top(rest)
        source_type, pointer = parts[0], parts[1].split()[-1]
        index_types, indices = [], []
        for p in parts[2:]:
            t, v = typed_value(p)
            index_types.append(t)
            indices.append(v)
        return Instr("getelementptr", result, source_type, [pointer] + indices, index_types=index_types)
    if op == "call":
        m2 = re.match(rf"(.*?)\s*({NAME})\((.*)\)\s*$", rest)
        ret_type, callee, args_text = m2.group(1).strip(), m2.group(2), m2.group(3)
        arg_types, args = [], []
        for a in split_top(args_text):
            t, v = typed_value(a)
            arg_types.append(t)
            args.append(v)
        return Instr("call", result, ret_type, args, callee=callee, arg_types=arg_types)
    if op == "br":
        labels = re.findall(r"label\s+%([-\w$.]+)", rest)
        if rest.startswith("label"):
            return Instr("br", None, None, [], targets=labels)
        condition = split_top(rest)[0].split()[-1]
        return Instr("br", None, None, [condition], targets=labels)
    if op == "ret":
        if rest == "void":
            return Instr("ret", None, "void")
        t, v = typed_value(rest)
        return Instr("ret", None, t, [v])
    if op == "unreachable":
        return Instr("unreachable")
    if op == "phi":
        t, pairs = rest.split(None, 1)
        incoming = [(v.strip(), label.strip()) for v, label in re.findall(r"\[\s*([^,\]]+),\s*%([-\w$.]+)\s*\]", pairs)]
        return Instr("phi", result, t, incoming=incoming)
    raise IRError(f"unknown instruction: {line}")


def parse(text: str) -> Module:
    """
    @brief Read the LLVM IR the course's code generators print.

    @param text the IR of a whole module
    @return the module
    """
    module = Module()
    function = None
    block = None
    for number, raw in enumerate(text.splitlines(), start=1):
        line = raw.split(";", 1)[0].rstrip() if not raw.lstrip().startswith("@") else raw.rstrip()
        stripped = line.strip()
        if not stripped:
            continue
        try:
            if function is None:
                if stripped.startswith("define"):
                    m = re.match(r"define\s+(.+?)\s+@([-\w$.]+)\((.*)\)\s*\{$", stripped)
                    params = [typed_value(p) for p in split_top(m.group(3))]
                    function = Function(m.group(2), m.group(1), params)
                    module.functions.append(function)
                    block = None
                else:
                    module.header.append(raw.rstrip())
                continue
            if stripped == "}":
                function = None
                continue
            m = re.match(r"^([-\w$.]+):$", stripped)
            if m:
                block = Block(m.group(1))
                function.blocks.append(block)
                continue
            if block is None:
                block = Block("entry")
                function.blocks.append(block)
            block.instrs.append(parse_instruction(stripped))
        except (IRError, AttributeError, ValueError) as e:
            raise IRError(f"line {number}: cannot read {stripped!r} ({e})")
    return module
