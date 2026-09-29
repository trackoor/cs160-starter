# ===----------------------------------------------------------------------=== #
#
#                         CS160 ChocoPy Compiler
#
# emit.py
#
# Identification: compiler/emit.py
#
# Copyright (c) 2026, CS160 Course Staff, UC Santa Barbara
#
# ===----------------------------------------------------------------------=== #
"""The emitter collects the text of an LLVM module as your code generator produces it."""

RUNTIME_DECLARATIONS = """\
declare void @cp_print_int(i32)
declare void @cp_print_bool(i32)
declare void @cp_print_str(ptr)
declare ptr @cp_alloc(i64)
declare i32 @cp_str_eq(ptr, ptr)
declare void @cp_error_arg()
declare void @cp_error_div()
declare void @cp_error_oob()
declare void @cp_error_none()
declare void @llvm.memcpy.p0.p0.i64(ptr, ptr, i64, i1)"""


def is_terminator(instr: str) -> bool:
    """
    @brief Tell whether an instruction ends its block.

    @param instr the text of an instruction
    @return True for `br`, `ret` and `unreachable`
    """
    return instr == "ret void" or instr == "unreachable" or instr.startswith(("br ", "ret "))


class Function:
    """
    Function collects the instructions of one LLVM function. It numbers
    temporaries and labels, keeps every `alloca` in the entry block, and looks
    after block boundaries: an instruction emitted after a terminator would be
    unreachable, so a further terminator is dropped and any other instruction
    starts a fresh block named `dead.N`.
    """

    def __init__(self, header: str):
        """
        @brief Start a function.

        @param header the text before the body, such as 'define i32 @main()'
        """
        self.header = header
        self.allocas: list[str] = []
        self.body: list[str] = []
        self.slots: set[str] = set()
        self.temp_count = 0
        self.label_count = 0
        self.terminated = False

    def temp(self) -> str:
        """
        @brief Take a fresh temporary.

        @return its name: %t1, %t2, ...
        """
        self.temp_count += 1
        return f"%t{self.temp_count}"

    def labels(self, *kinds: str) -> list[str]:
        """
        @brief Take fresh labels that share one number.

        For example, `labels("while.cond", "while.body", "while.end")` returns
        `["while.cond.3", "while.body.3", "while.end.3"]`.

        @param kinds the labels' prefixes
        @return the labels
        """
        self.label_count += 1
        return [f"{kind}.{self.label_count}" for kind in kinds]

    def slot(self, name: str, llvm_type: str) -> str:
        """
        @brief Reserve a variable's stack slot, `%name.addr`, in the entry block.

        Asking for the same slot again returns it without a second `alloca`.

        @param name the variable's name
        @param llvm_type the type the slot holds, such as `i32`
        @return the slot
        """
        reg = f"%{name}.addr"
        if reg not in self.slots:
            self.slots.add(reg)
            self.allocas.append(f"  {reg} = alloca {llvm_type}")
        return reg

    def emit(self, instr: str) -> None:
        """
        @brief Append an instruction to the current block.

        @param instr the text of the instruction, such as `%t1 = add i32 %t0, 1`
        """
        if self.terminated:
            if is_terminator(instr):
                return
            (dead,) = self.labels("dead")
            self.body.append(f"{dead}:")
            self.terminated = False
        self.body.append("  " + instr)
        self.terminated = is_terminator(instr)

    def label(self, name: str) -> None:
        """
        @brief Start a new block.

        If the current block has no terminator yet, first add `br label %name`,
        so that control falls through.

        @param name the block's label
        """
        if not self.terminated:
            self.body.append(f"  br label %{name}")
        self.body.append(f"{name}:")
        self.terminated = False

    def render(self, final_terminator: str) -> str:
        """
        @brief Finish the function.

        @param final_terminator the terminator that ends the last block if it is still open
        @return the text of the function
        """
        if not self.terminated:
            self.emit(final_terminator)
        return "\n".join([self.header + " {", "entry:", *self.allocas, *self.body, "}"])


def llvm_string_literal(value: str) -> str:
    """
    @brief Escape a string for an LLVM `c"..."` constant.

    @param value an ASCII string
    @return the characters between the quotes
    """
    out = []
    for ch in value:
        code = ord(ch)
        if 32 <= code < 127 and ch not in '"\\':
            out.append(ch)
        else:
            out.append(f"\\{code:02X}")
    return "".join(out)


class Module:
    """Module collects functions, global variables and string constants, and prints the `.ll` file."""

    def __init__(self):
        self.globals: list[str] = []
        self.strings: dict[str, str] = {}
        self.functions: list[str] = []

    def string(self, value: str) -> str:
        """
        @brief Get the global constant object that holds a string literal.

        The object has the layout `{ i32, [N x i8] }`: the length, then the
        characters. The same literal always gets the same object.

        @param value the string's characters
        @return the object's name, such as @str.1
        """
        if value not in self.strings:
            name = f"@str.{len(self.strings) + 1}"
            n = len(value)
            self.strings[value] = name
            self.globals.append(
                f"{name} = private unnamed_addr constant {{ i32, [{n} x i8] }} "
                f'{{ i32 {n}, [{n} x i8] c"{llvm_string_literal(value)}" }}'
            )
        return self.strings[value]

    def global_variable(self, line: str) -> None:
        """
        @brief Add a global variable.

        @param line its definition, such as `@gv.count = global i32 0`
        """
        self.globals.append(line)

    def add_function(self, text: str) -> None:
        """
        @brief Add a finished function.

        @param text the text `Function.render` returned
        """
        self.functions.append(text)

    def render(self) -> str:
        """
        @brief Print the module.

        @return the text of the `.ll` file: the runtime's declarations, the globals and the functions
        """
        parts = ["; Generated by the CS160 ChocoPy compiler", RUNTIME_DECLARATIONS]
        if self.globals:
            parts.append("\n".join(self.globals))
        parts.extend(self.functions)
        return "\n\n".join(parts) + "\n"
