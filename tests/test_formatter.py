"""Tests for output formatter."""

import json


from junes.formatter import OutputFormatter


class TestOutputFormatterInit:
    """Tests for OutputFormatter initialization."""

    def test_init_with_format(self):
        """OutputFormatter should be initialized with a format type."""
        formatter = OutputFormatter("json")
        assert formatter.format == "json"

    def test_init_defaults_to_plain(self):
        """OutputFormatter should default to plain format."""
        formatter = OutputFormatter()
        assert formatter.format == "plain"


class TestFormatSources:
    """Tests for format_sources method."""

    def test_format_sources_json_returns_valid_json(self):
        """format_sources should return valid JSON when format is json."""
        formatter = OutputFormatter("json")
        data = {"sources": [{"id": "src1", "name": "Source 1"}]}

        result = formatter.format_sources(data)

        parsed = json.loads(result)
        assert parsed == data

    def test_format_sources_table_returns_table(self):
        """format_sources should return a table when format is table."""
        formatter = OutputFormatter("table")
        data = {"sources": [{"id": "src1", "name": "Source 1"}]}

        result = formatter.format_sources(data)

        assert isinstance(result, str)
        assert "src1" in result
        assert "Source 1" in result

    def test_format_sources_plain_returns_text(self):
        """format_sources should return plain text when format is plain."""
        formatter = OutputFormatter("plain")
        data = {"sources": [{"id": "src1", "name": "Source 1"}]}

        result = formatter.format_sources(data)

        assert isinstance(result, str)
        assert "src1" in result or "Source 1" in result


class TestFormatSessions:
    """Tests for format_sessions method."""

    def test_format_sessions_json_returns_valid_json(self):
        """format_sessions should return valid JSON when format is json."""
        formatter = OutputFormatter("json")
        data = {"sessions": [{"id": "sess1", "state": "COMPLETED", "title": "Test Auth"}]}

        result = formatter.format_sessions(data)

        parsed = json.loads(result)
        assert parsed == data

    def test_format_sessions_table_returns_table(self):
        """format_sessions should return a table when format is table."""
        formatter = OutputFormatter("table")
        data = {"sessions": [{"id": "sess1", "state": "COMPLETED", "title": "Test Auth"}]}

        result = formatter.format_sessions(data)

        assert isinstance(result, str)
        assert "sess1" in result
        assert "COMPLETED" in result
        assert "Test Auth" in result


class TestFormatSessionDetails:
    """Tests for format_session_details method."""

    def test_format_session_details_json_returns_valid_json(self):
        """format_session_details should return valid JSON when format is json."""
        formatter = OutputFormatter("json")
        data = {"id": "sess1", "state": "COMPLETED", "title": "Test"}

        result = formatter.format_session_details(data)

        parsed = json.loads(result)
        assert parsed == data


class TestFormatActivities:
    """Tests for format_activities method."""

    def test_format_activities_json_returns_valid_json(self):
        """format_activities should return valid JSON when format is json."""
        formatter = OutputFormatter("json")
        data = {"activities": [
            {"id": "act1", "createTime": "2024-01-01T10:00:00Z"},
            {"id": "act2", "createTime": "2024-01-01T09:00:00Z"}
        ]}

        result = formatter.format_activities(data)

        parsed = json.loads(result)
        assert parsed == data

    def test_format_activities_chronological_order(self):
        """format_activities should order activities chronologically (oldest first)."""
        formatter = OutputFormatter("table")
        data = {"activities": [
            {"id": "act1", "createTime": "2024-01-01T10:00:00Z"},
            {"id": "act2", "createTime": "2024-01-01T09:00:00Z"}
        ]}

        result = formatter.format_activities(data)

        # In chronological order, act2 (09:00) should appear before act1 (10:00)
        assert result.index("act2") < result.index("act1")


class TestFormatMessageResponse:
    """Tests for format_message_response method."""

    def test_format_message_response_json_returns_valid_json(self):
        """format_message_response should return valid JSON when format is json."""
        formatter = OutputFormatter("json")
        data = {"response": {"content": "Hello"}}

        result = formatter.format_message_response(data)

        parsed = json.loads(result)
        assert parsed == data


class TestFormatError:
    """Tests for format_error method."""

    def test_format_error_returns_error_message(self):
        """format_error should return a formatted error message."""
        formatter = OutputFormatter("plain")

        result = formatter.format_error("Test error")

        assert isinstance(result, str)
        assert "error" in result.lower() or "Test error" in result


class TestJSONValidity:
    """Tests for JSON output validity."""

    def test_all_json_outputs_are_valid(self):
        """All JSON format outputs should be valid JSON."""
        formatter = OutputFormatter("json")

        # Test all format methods
        test_data = {
            "sources": {"sources": []},
            "sessions": {"sessions": []},
            "details": {"id": "sess1"},
            "activities": {"activities": []},
            "message": {"response": {}},
        }

        json_outputs = [
            formatter.format_sources(test_data["sources"]),
            formatter.format_sessions(test_data["sessions"]),
            formatter.format_session_details(test_data["details"]),
            formatter.format_activities(test_data["activities"]),
            formatter.format_message_response(test_data["message"]),
        ]

        for output in json_outputs:
            parsed = json.loads(output)
            assert isinstance(parsed, dict)
