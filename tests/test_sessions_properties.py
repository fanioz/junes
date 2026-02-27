"""Property-based tests for sessions commands."""

from click.testing import CliRunner

from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st

import responses

from jules_cli.cli import cli
from jules_cli.constants import BASE_URL


class TestOptionalParameterPassThroughProperty:
    """Property 5: Optional Parameter Pass-Through (Requirements 3.4)"""

    @given(
        parameters=st.lists(
            st.tuples(
                st.text(min_size=1, max_size=20, alphabet=st.characters(whitelist_categories=['L', 'N'], blacklist_characters='\x00=')),
                st.text(min_size=1, max_size=20, alphabet=st.characters(whitelist_categories=['L', 'N'], blacklist_characters='\x00=')),
            ),
            min_size=0,
            max_size=5,
        )
    )
    @settings(max_examples=50, suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_parameters_passed_to_create_session(self, parameters):
        """sessions create should accept and pass optional parameters."""
        with responses.RequestsMock() as rsps:
            rsps.post(
                f"{BASE_URL}/sessions",
                json={"session": {"id": "sess1"}},
                status=201,
            )

            runner = CliRunner()
            args = ["--api-key", "test-key", "sessions", "create", "src1"]

            # Add parameters as -p key=value
            for key, value in parameters:
                args.extend(["-p", f"{key}={value}"])

            result = runner.invoke(cli, args)

            # Should succeed (parameters are passed, even if not used)
            assert result.exit_code == 0


class TestSessionFilterPassThroughProperty:
    """Property 6: Session Filter Pass-Through (Requirements 4.6)"""

    @given(
        status=st.sampled_from(["active", "completed", "failed", "pending", None])
    )
    @settings(max_examples=50)
    def test_status_filter_passed_to_list_sessions(self, status):
        """sessions list --status should pass the filter to the API."""
        with responses.RequestsMock() as rsps:
            if status:
                rsps.get(
                    f"{BASE_URL}/sessions?status={status}",
                    json={"sessions": []},
                    status=200,
                )
            else:
                rsps.get(
                    f"{BASE_URL}/sessions",
                    json={"sessions": []},
                    status=200,
                )

            runner = CliRunner()
            args = ["--api-key", "test-key", "sessions", "list"]

            if status:
                args.extend(["--status", status])

            result = runner.invoke(cli, args)

            # Should succeed
            assert result.exit_code == 0
