"""Ask llama3.2 which tool to use, run it, then ask for a final answer."""

from calculator import calculate
from datetime_tool import get_current_datetime
from file_tool import read_text_file
from local_llm import ask_local_llm

# The model has no real tools. This text is how we teach it the contract:
# pick one tool in a fixed format, or say none. Python runs the tool below.
TOOL_INSTRUCTIONS = """
You are a helpful assistant. You have three tools.

calculator — evaluates arithmetic expressions using numbers, parentheses,
+, -, *, and /.
datetime — returns the current local date and time. It does not need an input.
file_reader — reads a local UTF-8 text file. It requires a file path.

Reply using exactly one of these formats and nothing else.

If you need the calculator:
TOOL: calculator
INPUT: 2 + 2

If you need the current date and time:
TOOL: datetime

If you need to read a local text file:
TOOL: file_reader
INPUT: notes.txt

If you do not need a tool:
TOOL: none
""".strip()


def execute_tool(reply: str) -> str:
    """Read the model's TOOL/INPUT lines and run the matching local function."""
    lines = [line.strip() for line in reply.splitlines() if line.strip()]

    tool_name = None
    tool_input = None
    for line in lines:
        label, _, value = line.partition(":")
        if label.strip().lower() == "tool":
            tool_name = value.strip().lower()
        elif label.strip().lower() == "input":
            tool_input = value.strip()

    if not tool_name:
        raise ValueError("The model reply did not include a TOOL: line.")

    if tool_name == "none":
        return "No tool is needed."

    if tool_name == "datetime":
        return get_current_datetime()

    if tool_name == "calculator":
        if not tool_input:
            raise ValueError("calculator requires an INPUT: expression.")
        return str(calculate(tool_input))

    if tool_name == "file_reader":
        if not tool_input:
            raise ValueError("file_reader requires an INPUT: file path.")
        return read_text_file(tool_input)

    raise ValueError(f"Unknown tool: {tool_name}")


def main() -> None:
    question = input("Ask a question: ").strip()
    if not question:
        raise SystemExit("Please enter a question.")

    # Step 1: the model only chooses a tool (or none). It does not run code.
    prompt = f"{TOOL_INSTRUCTIONS}\n\nUser question:\n{question}"
    reply = ask_local_llm(prompt)

    print("\nTool choice:")
    print(reply)

    # Step 2: Python runs the local function the model named.
    tool_result = execute_tool(reply)

    print("\nTool result:")
    print(tool_result)

    # Step 3: send the original question plus the tool result back for a
    # normal answer. The model should use the tool output, not redo the work.
    final_prompt = (
        "This is the result returned by the tool.\n"
        "Use this result to answer the user's original question.\n"
        "Do not perform the calculation yourself if a calculator result is provided.\n"
        "Do not mention internal tool instructions unless necessary.\n"
        "Give the user a normal concise answer.\n\n"
        f"User question:\n{question}\n\n"
        f"Tool result:\n{tool_result}"
    )
    final_reply = ask_local_llm(final_prompt)

    print("\nFinal answer:")
    print(final_reply)


if __name__ == "__main__":
    main()
