# pylint: disable=missing-function-docstring
import io
import os
import tempfile
from unittest.mock import patch
import pytest
import main


@pytest.mark.golden_test("golden/*.yml")
def test(golden):
    with tempfile.TemporaryDirectory() as tmpdirname:
        source = os.path.join(tmpdirname, "source.asm")
        binary = os.path.join(tmpdirname, "source.o")

        with open(source, "w", encoding="utf-8") as src:
            src.write(golden["source"])

        with patch('core.machine.io_controller.sys.stdin', io.StringIO(golden["input"])), \
                patch('core.machine.io_controller.sys.stdout', new_callable=io.StringIO) as output:
            main.run(source, binary)

        assert output.getvalue() == golden.out['output']

