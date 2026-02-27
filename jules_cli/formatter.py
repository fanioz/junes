"""Output formatting for CLI commands."""

import json
from typing import Any, Dict, List

from tabulate import tabulate


class OutputFormatter:
    """Format API responses for CLI output."""

    def __init__(self, format: str = "plain"):
        """
        Initialize the formatter.

        Args:
            format: Output format - "json", "table", or "plain"
        """
        if format not in ("json", "table", "plain"):
            raise ValueError(f"Invalid format: {format}")
        self.format = format

    def format_sources(self, data: Dict[str, Any]) -> str:
        """
        Format sources list.

        Args:
            data: API response data

        Returns:
            str: Formatted output
        """
        sources = data.get("sources", [])

        if self.format == "json":
            return json.dumps(data, indent=2)

        if self.format == "table":
            if not sources:
                return "No sources found."
            headers = ["ID", "Name"]
            rows = [[s.get("id", ""), s.get("name", "")] for s in sources]
            return tabulate(rows, headers=headers, tablefmt="grid")

        # Plain format
        if not sources:
            return "No sources found."
        lines = [f"Sources ({len(sources)}):"]
        for source in sources:
            lines.append(f"  - {source.get('name', source.get('id', 'Unknown'))}")
        return "\n".join(lines)

    def format_sessions(self, data: Dict[str, Any]) -> str:
        """
        Format sessions list.

        Args:
            data: API response data

        Returns:
            str: Formatted output
        """
        sessions = data.get("sessions", [])

        if self.format == "json":
            return json.dumps(data, indent=2)

        if self.format == "table":
            if not sessions:
                return "No sessions found."
            headers = ["ID", "Source ID", "Status", "Created"]
            rows = [[
                s.get("id", ""),
                s.get("source_id", ""),
                s.get("status", ""),
                s.get("created_at", ""),
            ] for s in sessions]
            return tabulate(rows, headers=headers, tablefmt="grid")

        # Plain format
        if not sessions:
            return "No sessions found."
        lines = [f"Sessions ({len(sessions)}):"]
        for session in sessions:
            status = session.get("status", "unknown")
            sid = session.get("id", "unknown")
            lines.append(f"  - [{status}] {sid}")
        return "\n".join(lines)

    def format_session_details(self, data: Dict[str, Any]) -> str:
        """
        Format session details.

        Args:
            data: API response data

        Returns:
            str: Formatted output
        """
        if self.format == "json":
            return json.dumps(data, indent=2)

        session = data.get("session", {})
        lines = ["Session Details:"]
        for key, value in session.items():
            lines.append(f"  {key}: {value}")
        return "\n".join(lines)

    def format_activities(self, data: Dict[str, Any]) -> str:
        """
        Format activities list in chronological order.

        Args:
            data: API response data

        Returns:
            str: Formatted output
        """
        activities = data.get("activities", [])

        if self.format == "json":
            # JSON format preserves original order
            return json.dumps(data, indent=2)

        # For table and plain, sort chronologically (oldest first)
        sorted_activities = sorted(
            activities,
            key=lambda a: a.get("timestamp", "")
        )

        if self.format == "table":
            if not sorted_activities:
                return "No activities found."
            headers = ["ID", "Time", "Type", "Description"]
            rows = [[
                a.get("id", ""),
                a.get("timestamp", ""),
                a.get("type", ""),
                a.get("description", "")[:50],  # Truncate long descriptions
            ] for a in sorted_activities]
            return tabulate(rows, headers=headers, tablefmt="grid")

        # Plain format
        if not sorted_activities:
            return "No activities found."
        lines = [f"Activities ({len(sorted_activities)}):"]
        for activity in sorted_activities:
            lines.append(f"  - [{activity.get('timestamp', '')}] {activity.get('type', '')}")
        return "\n".join(lines)

    def format_message_response(self, data: Dict[str, Any]) -> str:
        """
        Format agent message response.

        Args:
            data: API response data

        Returns:
            str: Formatted output
        """
        if self.format == "json":
            return json.dumps(data, indent=2)

        response = data.get("response", {})
        content = response.get("content", "")

        if self.format == "table":
            return f"Agent Response:\n{content}"

        # Plain format
        return content if content else "No response content."

    def format_error(self, message: str) -> str:
        """
        Format error message.

        Args:
            message: Error message

        Returns:
            str: Formatted error
        """
        if self.format == "json":
            return json.dumps({"error": message}, indent=2)

        return f"Error: {message}"
