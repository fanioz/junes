"""Output formatting for CLI commands."""

import json
from typing import Any, Dict


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
            # Lazy import to improve CLI startup time by ~120ms
            from tabulate import tabulate
            if not sources:
                return "No sources found."
            headers = ["ID", "Name"]
            rows = [[s.get("id", ""), s.get("name", "")] for s in sources]
            return tabulate(rows, headers=headers, tablefmt="grid", disable_numparse=True)

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
            # Lazy import to improve CLI startup time by ~120ms
            from tabulate import tabulate
            if not sessions:
                return "No sessions found."
            headers = ["ID", "Title", "State", "Created"]
            rows = [[
                s.get("id", ""),
                s.get("title", ""),
                s.get("state", ""),
                s.get("createTime", ""),
            ] for s in sessions]
            return tabulate(rows, headers=headers, tablefmt="grid", disable_numparse=True)

        # Plain format
        if not sessions:
            return "No sessions found."
        lines = [f"Sessions ({len(sessions)}):"]
        for session in sessions:
            state = session.get("state", "unknown")
            title = session.get("title", "")
            sid = session.get("id", "unknown")
            label = f"{title} ({sid})" if title else sid
            lines.append(f"  - [{state}] {label}")
        return "\n".join(lines)

    def format_session_details(self, data: Dict[str, Any]) -> str:
        """
        Format session details.

        The API returns a flat Session object (not nested under a 'session' key).

        Args:
            data: API response data (Session object)

        Returns:
            str: Formatted output
        """
        if self.format == "json":
            return json.dumps(data, indent=2)

        # Display key fields in a readable order
        display_fields = [
            ("name", "Name"),
            ("id", "ID"),
            ("title", "Title"),
            ("state", "State"),
            ("prompt", "Prompt"),
            ("url", "URL"),
            ("createTime", "Created"),
            ("updateTime", "Updated"),
        ]

        lines = ["Session Details:"]
        for field_key, label in display_fields:
            value = data.get(field_key)
            if value is not None:
                lines.append(f"  {label}: {value}")

        # Display outputs if present
        outputs = data.get("outputs", [])
        if outputs:
            lines.append("  Outputs:")
            for output in outputs:
                pr = output.get("pullRequest", {})
                if pr:
                    lines.append(f"    PR: {pr.get('url', '')}")
                    if pr.get("title"):
                        lines.append(f"    PR Title: {pr['title']}")

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
            key=lambda a: a.get("createTime", "")
        )

        if self.format == "table":
            # Lazy import to improve CLI startup time by ~120ms
            from tabulate import tabulate
            if not sorted_activities:
                return "No activities found."
            headers = ["ID", "Time", "Originator", "Description"]
            rows = [[
                f"\u200b{a.get('id', '')}" if a.get("id") else "",
                str(a.get("createTime", "")),
                str(a.get("originator", "")),
                str(a.get("description", "")[:50]),  # Truncate long descriptions
            ] for a in sorted_activities]
            return tabulate(rows, headers=headers, tablefmt="grid")

        # Plain format
        if not sorted_activities:
            return "No activities found."
        lines = [f"Activities ({len(sorted_activities)}):"]
        for activity in sorted_activities:
            originator = activity.get("originator", "")
            description = activity.get("description", "")
            create_time = activity.get("createTime", "")
            origin_tag = f" ({originator})" if originator else ""
            lines.append(f"  - [{create_time}] ({activity.get('id', '')}){origin_tag} {description}")
        return "\n".join(lines)

    def format_message_response(self, data: Dict[str, Any]) -> str:
        """
        Format agent message response.

        The API returns an empty SendMessageResponse on success.

        Args:
            data: API response data

        Returns:
            str: Formatted output
        """
        if self.format == "json":
            return json.dumps(data, indent=2)

        # The API returns empty response on success
        if not data:
            return "Message sent successfully."

        response = data.get("response", {})
        content = response.get("content", "")

        if self.format == "table":
            return f"Agent Response:\n{content}"

        # Plain format
        return content if content else "Message sent successfully."

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
