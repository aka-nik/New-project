"""Serve the local quality dashboard and its deterministic report endpoint."""

import argparse
import json
import re
import sqlite3
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

try:
    from scripts.check_quality import build_quality_report, summarize_quality_report
except ModuleNotFoundError:
    from check_quality import build_quality_report, summarize_quality_report


def read_mapping_proposals(database: Path) -> list[dict[str, object]]:
    """Read persisted mapping proposals without requiring a warehouse file."""
    if not database.is_file():
        return []
    with sqlite3.connect(database) as connection:
        try:
            rows = connection.execute(
                "SELECT proposal_id, raw_value, proposed_value, confidence, status "
                "FROM dq_proposed_mappings ORDER BY proposal_id"
            ).fetchall()
        except sqlite3.OperationalError:
            return []
    return [
        {
            "proposal_id": row[0],
            "raw_value": row[1],
            "proposed_value": row[2],
            "confidence": row[3],
            "status": row[4],
        }
        for row in rows
    ]


def make_handler(source_dir: Path, frontend_dir: Path, database: Path):
    class DashboardHandler(SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(frontend_dir), **kwargs)

        def do_GET(self):
            route = urlparse(self.path).path
            if route == "/":
                self.path = "/dashboard.html"
                return super().do_GET()
            if route == "/api/quality-report":
                reports = build_quality_report(source_dir)
                payload = {"summary": summarize_quality_report(reports), "tables": reports}
                encoded = json.dumps(payload).encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(encoded)))
                self.end_headers()
                self.wfile.write(encoded)
                return
            if route == "/api/mappings":
                encoded = json.dumps(read_mapping_proposals(database)).encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(encoded)))
                self.end_headers()
                self.wfile.write(encoded)
                return
            super().do_GET()

        def do_POST(self):
            if urlparse(self.path).path == "/api/source-files":
                filename = self.headers.get("X-Filename", "")
                content_length = int(self.headers.get("Content-Length", "0"))
                if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]*\.csv", filename):
                    self.send_error(400, "Upload a CSV file with a simple filename.")
                    return
                if content_length < 1 or content_length > 100 * 1024 * 1024:
                    self.send_error(400, "CSV files must be between 1 byte and 100 MB.")
                    return
                source_dir.mkdir(parents=True, exist_ok=True)
                (source_dir / filename).write_bytes(self.rfile.read(content_length))
                encoded = json.dumps({"filename": filename, "bytes": content_length}).encode("utf-8")
                self.send_response(201)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(encoded)))
                self.end_headers()
                self.wfile.write(encoded)
                return
            if urlparse(self.path).path != "/api/mappings/approve":
                self.send_error(404)
                return
            try:
                proposal_id = int(self.rfile.read(int(self.headers["Content-Length"])))
                with sqlite3.connect(database) as connection:
                    from sentinel.warehouse import approve_mapping

                    approve_mapping(connection, proposal_id)
            except (ValueError, TypeError, sqlite3.Error) as error:
                self.send_error(400, str(error))
                return
            self.send_response(204)
            self.end_headers()

    return DashboardHandler


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source_dir", type=Path, nargs="?", default=Path("data/source"))
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--database", type=Path, default=Path("data/sentinel.db"))
    arguments = parser.parse_args()
    frontend_dir = Path(__file__).resolve().parent.parent / "frontend"
    server = ThreadingHTTPServer(
        (arguments.host, arguments.port),
        make_handler(arguments.source_dir, frontend_dir, arguments.database),
    )
    print(f"Dashboard: http://{arguments.host}:{arguments.port}")
    server.serve_forever()


if __name__ == "__main__":
    main()
