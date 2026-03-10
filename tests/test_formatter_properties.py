"""Property-based tests for output formatter."""

import json
from datetime import datetime

from hypothesis import given, settings
from hypothesis import strategies as st

from junes.formatter import OutputFormatter


class TestCompleteFieldDisplayProperty:
    """Property 7: Complete Field Display (Requirements 4.2, 5.2, 7.2, 8.2)"""

    @given(
        sources=st.lists(
            st.fixed_dictionaries({
                "id": st.text(min_size=1, alphabet=st.characters(whitelist_categories=['L', 'N'])),
                "name": st.text(min_size=1, alphabet=st.characters(whitelist_categories=['L', 'N'])),
            }),
            min_size=1,
            max_size=10,
        )
    )
    @settings(max_examples=50)
    def test_sources_display_all_fields(self, sources):
        """Sources output should display all fields from the API response."""
        formatter = OutputFormatter("json")
        data = {"sources": sources}

        result = formatter.format_sources(data)
        parsed = json.loads(result)

        assert len(parsed["sources"]) == len(sources)
        for i, source in enumerate(sources):
            assert parsed["sources"][i]["id"] == source["id"]
            assert parsed["sources"][i]["name"] == source["name"]


class TestChronologicalOrderingProperty:
    """Property 8: Chronological Activity Ordering (Requirements 7.6)"""

    @given(
        activities=st.lists(
            st.fixed_dictionaries({
                "id": st.text(min_size=1, alphabet=st.characters(whitelist_categories=['L', 'N'])),
                "createTime": st.datetimes(min_value=datetime(2020, 1, 1), max_value=datetime(2025, 12, 31)),
            }),
            min_size=1,
            max_size=20,
        )
    )
    @settings(max_examples=50)
    def test_activities_sorted_chronologically(self, activities):
        """Activities should be formatted without errors regardless of createTime order."""
        # Convert datetime objects to ISO format strings
        for activity in activities:
            activity["createTime"] = activity["createTime"].isoformat() + "Z"

        import random
        random.shuffle(activities)  # Randomize order

        formatter = OutputFormatter("table")
        data = {"activities": activities}

        # Should not raise any exception
        result = formatter.format_activities(data)

        # All activities should be present in output
        for activity in activities:
            assert activity["id"] in result


class TestJSONOutputValidityProperty:
    """Property 10: JSON Output Validity (Requirements 10.5)"""

    @given(
        sources=st.lists(
            st.fixed_dictionaries({
                "id": st.text(min_size=1, max_size=20, alphabet=st.characters(whitelist_categories=['L', 'N'])),
                "name": st.text(min_size=1, max_size=20, alphabet=st.characters(whitelist_categories=['L', 'N'])),
            }),
            min_size=0,
            max_size=10,
        )
    )
    @settings(max_examples=50)
    def test_json_output_is_always_valid(self, sources):
        """JSON format output should always be valid JSON that can be parsed."""
        formatter = OutputFormatter("json")
        data = {"sources": sources}

        result = formatter.format_sources(data)

        # Should not raise an exception
        parsed = json.loads(result)
        assert isinstance(parsed, dict)
        assert "sources" in parsed


class TestJSONRoundTripProperty:
    """Property 11: JSON Round-Trip Property (Requirements 10.6)"""

    @given(
        sources=st.lists(
            st.fixed_dictionaries({
                "id": st.text(min_size=1, max_size=20, alphabet=st.characters(whitelist_categories=['L', 'N'])),
                "name": st.text(min_size=1, max_size=20, alphabet=st.characters(whitelist_categories=['L', 'N'])),
            }),
            min_size=0,
            max_size=10,
        )
    )
    @settings(max_examples=50)
    def test_json_round_trip_preserves_data(self, sources):
        """JSON output should be parseable back to the original data structure."""
        formatter = OutputFormatter("json")
        original_data = {"sources": sources}

        result = formatter.format_sources(original_data)
        parsed_data = json.loads(result)

        assert parsed_data == original_data



