import unittest
from wdlfmt.checker import StyleChecker, Status

_HEADER = "version 1.0\n"


def _check(wdl: str):
    return {r.rule: r for r in StyleChecker(_HEADER + wdl).run_all()}


class TestLineLengthCheck(unittest.TestCase):
    def test_all_short_lines_pass(self):
        wdl = "task MyTask {\n" + "    " + "x" * 90 + "\n}\n"
        r = _check(wdl)["Line length ≤ 100 chars"]
        self.assertEqual(r.status, Status.PASS)

    def test_long_line_fails(self):
        wdl = "task MyTask {\n" + "    " + "x" * 110 + "\n}\n"
        r = _check(wdl)["Line length ≤ 100 chars"]
        self.assertEqual(r.status, Status.FAIL)
        self.assertIn("1 line", r.details)


class TestTaskNaming(unittest.TestCase):
    def test_upper_camel_passes(self):
        r = _check("task MyTask {\n    command <<< echo >>>\n}\n")["Task names are UpperCamelCase"]
        self.assertEqual(r.status, Status.PASS)

    def test_lower_camel_fails(self):
        r = _check("task myTask {\n    command <<< echo >>>\n}\n")["Task names are UpperCamelCase"]
        self.assertEqual(r.status, Status.FAIL)
        self.assertIn("myTask", r.details)

    def test_snake_case_fails(self):
        r = _check("task my_task {\n    command <<< echo >>>\n}\n")["Task names are UpperCamelCase"]
        self.assertEqual(r.status, Status.FAIL)


class TestWorkflowNaming(unittest.TestCase):
    def test_upper_camel_passes(self):
        r = _check("workflow MyWorkflow {\n}\n")["Workflow names are UpperCamelCase"]
        self.assertEqual(r.status, Status.PASS)

    def test_lower_camel_fails(self):
        r = _check("workflow myWorkflow {\n}\n")["Workflow names are UpperCamelCase"]
        self.assertEqual(r.status, Status.FAIL)
        self.assertIn("myWorkflow", r.details)


class TestStructNaming(unittest.TestCase):
    def test_upper_camel_passes(self):
        r = _check("struct MyStruct {\n    String foo\n}\n")["Struct names are UpperCamelCase"]
        self.assertEqual(r.status, Status.PASS)

    def test_lower_fails(self):
        r = _check("struct myStruct {\n    String foo\n}\n")["Struct names are UpperCamelCase"]
        self.assertEqual(r.status, Status.FAIL)


class TestCallAliases(unittest.TestCase):
    def _result(self, wdl):
        return _check(wdl)["Call aliases are lowerCamelCase"]

    def test_lower_camel_alias_passes(self):
        wdl = "workflow W {\n    call MyTask as myTask { }\n}\n"
        r = self._result(wdl)
        self.assertEqual(r.status, Status.PASS)

    def test_upper_camel_alias_fails(self):
        wdl = "workflow W {\n    call MyTask as MyAlias { }\n}\n"
        r = self._result(wdl)
        self.assertEqual(r.status, Status.FAIL)
        self.assertIn("MyAlias", r.details)

    def test_missing_alias_warns(self):
        wdl = "workflow W {\n    call MyTask { }\n}\n"
        r = self._result(wdl)
        self.assertEqual(r.status, Status.WARN)
        self.assertIn("MyTask", r.details)


class TestSetPipefail(unittest.TestCase):
    def _result(self, wdl):
        return _check(wdl)["set -e -o pipefail in multi-command blocks"]

    def test_present_passes(self):
        wdl = (
            "task T {\n"
            "    command <<<\n"
            "        set -e -o pipefail\n"
            "        echo hello\n"
            "        echo world\n"
            "    >>>\n"
            "}\n"
        )
        r = self._result(wdl)
        self.assertEqual(r.status, Status.PASS)

    def test_absent_warns(self):
        wdl = (
            "task T {\n"
            "    command <<<\n"
            "        echo hello\n"
            "        echo world\n"
            "    >>>\n"
            "}\n"
        )
        r = self._result(wdl)
        self.assertEqual(r.status, Status.WARN)

    def test_single_command_no_warn(self):
        wdl = (
            "task T {\n"
            "    command <<<\n"
            "        echo hello\n"
            "    >>>\n"
            "}\n"
        )
        r = self._result(wdl)
        self.assertEqual(r.status, Status.PASS)


class TestParameterMeta(unittest.TestCase):
    def _result(self, wdl):
        return _check(wdl)["parameter_meta section present"]

    def test_present_passes(self):
        wdl = (
            "task T {\n"
            "    parameter_meta {\n"
            "        x: \"an input\"\n"
            "    }\n"
            "    command <<< echo >>>\n"
            "}\n"
        )
        r = self._result(wdl)
        self.assertEqual(r.status, Status.PASS)

    def test_absent_warns(self):
        wdl = "task T {\n    command <<< echo >>>\n}\n"
        r = self._result(wdl)
        self.assertEqual(r.status, Status.WARN)
        self.assertIn("task 'T'", r.details)


class TestDockerRuntime(unittest.TestCase):
    def _result(self, wdl):
        return _check(wdl)["docker defined in runtime blocks"]

    def test_docker_present_passes(self):
        wdl = (
            "task T {\n"
            "    command <<< echo >>>\n"
            "    runtime {\n"
            "        docker: \"ubuntu:22.04\"\n"
            "    }\n"
            "}\n"
        )
        r = self._result(wdl)
        self.assertEqual(r.status, Status.PASS)

    def test_docker_absent_warns(self):
        wdl = (
            "task T {\n"
            "    command <<< echo >>>\n"
            "    runtime {\n"
            "        memory: \"4G\"\n"
            "    }\n"
            "}\n"
        )
        r = self._result(wdl)
        self.assertEqual(r.status, Status.WARN)

    def test_no_runtime_warns(self):
        wdl = "task T {\n    command <<< echo >>>\n}\n"
        r = self._result(wdl)
        self.assertEqual(r.status, Status.WARN)


if __name__ == "__main__":
    unittest.main()
