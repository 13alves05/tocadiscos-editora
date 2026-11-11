import sys
import tempfile
import types
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

SRC_DIR = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC_DIR))

# history imports the index builder; stub it so these tests need no Whoosh install.
search_engine = types.ModuleType("searchEngine")
search_engine.build_unified_index = Mock()
sys.modules.setdefault("searchEngine", search_engine)

import history  # noqa: E402


class SnapshotSafetyTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.history_dir = self.root / "data" / "history"
        self.history_dir.mkdir(parents=True)
        self.data_dir = self.root / "data"
        self.files = [
            self.data_dir / "authors_table.csv",
            self.data_dir / "albums_table.csv",
            self.data_dir / "raw_tracks.csv",
        ]
        for path in self.files:
            path.write_text("current", encoding="utf-8")
        self.patches = [
            patch.object(history, "HIST_DIR", str(self.history_dir)),
            patch.object(history, "FILES", [str(path) for path in self.files]),
            patch.object(history, "build_unified_index", Mock()),
        ]
        for active_patch in self.patches:
            active_patch.start()
        self.addCleanup(self._cleanup)

    def _cleanup(self):
        for active_patch in reversed(self.patches):
            active_patch.stop()
        self.temp_dir.cleanup()

    def make_snapshot(self, name, include_all=True):
        snapshot = self.history_dir / name
        snapshot.mkdir()
        for index, source in enumerate(self.files):
            if include_all or index == 0:
                (snapshot / source.name).write_text(f"snapshot-{index}", encoding="utf-8")
        return snapshot

    def test_rejects_path_traversal_without_changing_data(self):
        outside = self.root / "outside"
        outside.mkdir()
        for source in self.files:
            (outside / source.name).write_text("malicious", encoding="utf-8")

        self.assertFalse(history.reverter_snapshot("../outside"))
        self.assertTrue(all(path.read_text(encoding="utf-8") == "current" for path in self.files))

    def test_rejects_incomplete_snapshot_before_copying(self):
        self.make_snapshot("incomplete", include_all=False)

        self.assertFalse(history.reverter_snapshot("incomplete"))
        self.assertTrue(all(path.read_text(encoding="utf-8") == "current" for path in self.files))

    def test_restores_complete_snapshot(self):
        self.make_snapshot("complete")

        self.assertTrue(history.reverter_snapshot("complete"))
        self.assertEqual(
            [path.read_text(encoding="utf-8") for path in self.files],
            ["snapshot-0", "snapshot-1", "snapshot-2"],
        )
        history.build_unified_index.assert_called_once()


if __name__ == "__main__":
    unittest.main()
