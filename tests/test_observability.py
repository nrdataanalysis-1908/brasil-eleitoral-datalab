import json
import logging
import unittest
from io import StringIO

from brasil_eleitoral.observability import JsonFormatter


class ObservabilityTests(unittest.TestCase):
    def test_formatter_emits_machine_readable_event(self):
        record = logging.LogRecord("pipeline", logging.INFO, "", 0, "stage_finished", (), None)
        record.stage = "silver"
        record.status = "success"
        payload = json.loads(JsonFormatter().format(record))
        self.assertEqual(payload["event"], "stage_finished")
        self.assertEqual(payload["stage"], "silver")
        self.assertEqual(payload["status"], "success")


if __name__ == "__main__":
    unittest.main()
