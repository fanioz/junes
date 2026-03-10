"""CLI command definitions.

Performance Note: This module uses lazy imports for JulesAPIClient and
OutputFormatter to minimize CLI startup time. These heavy dependencies
(through requests and tabulate) are only imported when actually needed
by sub-commands, not when displaying help or version information.
"""

import sys

import click

from jules_cli import __version__
from jules_cli.config import ConfigManager
from jules_cli.exceptions import ConfigurationError, JulesAPIError


@click.group(invoke_without_command=True)
@click.option(
    "--api-key",
    "-k",
    help="API key for authentication",
    envvar="JULES_API_KEY",
)
@click.option(
    "--format",
    "-f",
    type=click.Choice(["json", "table", "plain"], case_sensitive=False),
    default="plain",
    help="Output format (default: plain)",
)
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    help="Enable verbose logging",
)
@click.version_option(version=__version__, prog_name="jules")
@click.pass_context
def cli(ctx, api_key, format, verbose):
    """
    Jules CLI - A command-line interface for the Jules REST API.

    API key can be provided via:
      - --api-key option
      - JULES_API_KEY environment variable
      - Config file (use 'jules config init' to set up)
    """
    ctx.ensure_object(dict)
    ctx.obj["api_key"] = api_key
    ctx.obj["format"] = format.lower()
    ctx.obj["verbose"] = verbose

    # Get the actual API key using priority: CLI > ENV > Config
    if api_key is None:
        try:
            config_manager = ConfigManager()
            actual_api_key = config_manager.get_api_key(cli_arg_key=None)
            ctx.obj["actual_api_key"] = actual_api_key
        except ConfigurationError:
            # Don't fail immediately - commands might not need API key
            ctx.obj["actual_api_key"] = None
    else:
        ctx.obj["actual_api_key"] = api_key

    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())
        sys.exit(0)



@cli.group()
@click.pass_context
def sources(ctx):
    """Manage sources."""
    pass


@sources.command("list")
@click.pass_context
def sources_list(ctx):
    """List available sources."""
    from jules_cli.client import JulesAPIClient
    from jules_cli.formatter import OutputFormatter

    api_key = ctx.obj.get("actual_api_key")
    if not api_key:
        click.echo("Error: API key not found. Use --api-key, JULES_API_KEY env var, or 'jules config init'", err=True)
        sys.exit(1)

    try:
        client = JulesAPIClient(api_key=api_key, verbose=ctx.obj.get("verbose", False))
        formatter = OutputFormatter(ctx.obj.get("format", "plain"))

        data = client.list_sources()
        output = formatter.format_sources(data)
        click.echo(output)

    except JulesAPIError as e:
        formatter = OutputFormatter(ctx.obj.get("format", "plain"))
        error_output = formatter.format_error(str(e))
        click.echo(error_output, err=True)
        sys.exit(1)


@cli.group()
@click.pass_context
def sessions(ctx):
    """Manage sessions."""
    pass


@sessions.command("create")
@click.option("--prompt", "-p", required=True, help="Task description for Jules to execute")
@click.option("--title", "-t", default=None, help="Optional title for the session")
@click.option("--source", "-s", default=None, help="Source resource name (e.g. sources/github-myorg-myrepo)")
@click.option("--branch", "-b", default=None, help="Starting branch name (e.g. main)")
@click.option("--require-approval", is_flag=True, default=False, help="Require explicit plan approval before execution")
@click.option("--auto-pr", is_flag=True, default=False, help="Automatically create pull requests when code changes are ready")
@click.pass_context
def sessions_create(ctx, prompt, title, source, branch, require_approval, auto_pr):
    """Create a new session to start a coding task."""
    from jules_cli.client import JulesAPIClient
    from jules_cli.formatter import OutputFormatter

    api_key = ctx.obj.get("actual_api_key")
    if not api_key:
        click.echo("Error: API key not found. Use --api-key, JULES_API_KEY env var, or 'jules config init'", err=True)
        sys.exit(1)

    try:
        client = JulesAPIClient(api_key=api_key, verbose=ctx.obj.get("verbose", False))
        formatter = OutputFormatter(ctx.obj.get("format", "plain"))

        kwargs = {}
        if title is not None:
            kwargs["title"] = title
        if source is not None:
            kwargs["source"] = source
        if branch is not None:
            kwargs["starting_branch"] = branch
        if require_approval:
            kwargs["require_plan_approval"] = True
        if auto_pr:
            kwargs["automation_mode"] = "AUTO_CREATE_PR"

        data = client.create_session(prompt=prompt, **kwargs)
        output = formatter.format_session_details(data)
        click.echo(output)

    except JulesAPIError as e:
        formatter = OutputFormatter(ctx.obj.get("format", "plain"))
        error_output = formatter.format_error(str(e))
        click.echo(error_output, err=True)
        sys.exit(1)


@sessions.command("list")
@click.option("--status", type=click.Choice(["active", "completed", "failed", "pending"], case_sensitive=False), default=None, help="Filter by session status")
@click.option("--page-size", type=int, default=None, help="Number of sessions to return (1-100, default: 30)")
@click.option("--page-token", default=None, help="Page token from a previous list response")
@click.pass_context
def sessions_list(ctx, status, page_size, page_token):
    """List sessions."""
    from jules_cli.client import JulesAPIClient
    from jules_cli.formatter import OutputFormatter

    api_key = ctx.obj.get("actual_api_key")
    if not api_key:
        click.echo("Error: API key not found. Use --api-key, JULES_API_KEY env var, or 'jules config init'", err=True)
        sys.exit(1)

    try:
        client = JulesAPIClient(api_key=api_key, verbose=ctx.obj.get("verbose", False))
        formatter = OutputFormatter(ctx.obj.get("format", "plain"))

        params = {}
        if status is not None:
            params["status"] = status
        if page_size is not None:
            params["pageSize"] = page_size
        if page_token is not None:
            params["pageToken"] = page_token

        data = client.list_sessions(**params)
        output = formatter.format_sessions(data)
        click.echo(output)

    except JulesAPIError as e:
        formatter = OutputFormatter(ctx.obj.get("format", "plain"))
        error_output = formatter.format_error(str(e))
        click.echo(error_output, err=True)
        sys.exit(1)


@sessions.command("get")
@click.argument("session-id")
@click.pass_context
def sessions_get(ctx, session_id):
    """Get session details."""
    from jules_cli.client import JulesAPIClient
    from jules_cli.formatter import OutputFormatter

    api_key = ctx.obj.get("actual_api_key")
    if not api_key:
        click.echo("Error: API key not found. Use --api-key, JULES_API_KEY env var, or 'jules config init'", err=True)
        sys.exit(1)

    try:
        client = JulesAPIClient(api_key=api_key, verbose=ctx.obj.get("verbose", False))
        formatter = OutputFormatter(ctx.obj.get("format", "plain"))

        data = client.get_session(session_id)
        output = formatter.format_session_details(data)
        click.echo(output)

    except JulesAPIError as e:
        formatter = OutputFormatter(ctx.obj.get("format", "plain"))
        error_output = formatter.format_error(str(e))
        click.echo(error_output, err=True)
        sys.exit(1)


@sessions.command("delete")
@click.argument("session-id")
@click.option("--yes", "-y", is_flag=True, help="Skip confirmation prompt")
@click.pass_context
def sessions_delete(ctx, session_id, yes):
    """Delete a session."""
    from jules_cli.client import JulesAPIClient
    from jules_cli.formatter import OutputFormatter

    api_key = ctx.obj.get("actual_api_key")
    if not api_key:
        click.echo("Error: API key not found. Use --api-key, JULES_API_KEY env var, or 'jules config init'", err=True)
        sys.exit(1)

    if not yes:
        click.confirm(f"Are you sure you want to delete session {session_id}?", abort=True)

    try:
        client = JulesAPIClient(api_key=api_key, verbose=ctx.obj.get("verbose", False))

        client.delete_session(session_id)
        click.echo(f"Session {session_id} deleted successfully.")

    except JulesAPIError as e:
        formatter = OutputFormatter(ctx.obj.get("format", "plain"))
        error_output = formatter.format_error(str(e))
        click.echo(error_output, err=True)
        sys.exit(1)


@sessions.command("approve")
@click.argument("session-id")
@click.pass_context
def sessions_approve(ctx, session_id):
    """Approve a pending plan."""
    from jules_cli.client import JulesAPIClient
    from jules_cli.formatter import OutputFormatter

    api_key = ctx.obj.get("actual_api_key")
    if not api_key:
        click.echo("Error: API key not found. Use --api-key, JULES_API_KEY env var, or 'jules config init'", err=True)
        sys.exit(1)

    try:
        client = JulesAPIClient(api_key=api_key, verbose=ctx.obj.get("verbose", False))

        data = client.approve_plan(session_id)
        click.echo(f"Plan approved for session {session_id}")

    except JulesAPIError as e:
        formatter = OutputFormatter(ctx.obj.get("format", "plain"))
        error_output = formatter.format_error(str(e))
        click.echo(error_output, err=True)
        sys.exit(1)


@cli.group()
@click.pass_context
def activities(ctx):
    """Manage activities."""
    pass


@activities.command("list")
@click.argument("session-id")
@click.pass_context
def activities_list(ctx, session_id):
    """List activities for a session."""
    from jules_cli.client import JulesAPIClient
    from jules_cli.formatter import OutputFormatter

    api_key = ctx.obj.get("actual_api_key")
    if not api_key:
        click.echo("Error: API key not found. Use --api-key, JULES_API_KEY env var, or 'jules config init'", err=True)
        sys.exit(1)

    try:
        client = JulesAPIClient(api_key=api_key, verbose=ctx.obj.get("verbose", False))
        formatter = OutputFormatter(ctx.obj.get("format", "plain"))

        data = client.list_activities(session_id)
        output = formatter.format_activities(data)
        click.echo(output)

    except JulesAPIError as e:
        formatter = OutputFormatter(ctx.obj.get("format", "plain"))
        error_output = formatter.format_error(str(e))
        click.echo(error_output, err=True)
        sys.exit(1)


@cli.group()
@click.pass_context
def agent(ctx):
    """Interact with the agent."""
    pass


@agent.command("send")
@click.argument("session-id")
@click.argument("message", required=False)
@click.pass_context
def agent_send(ctx, session_id, message):
    """Send a message to the agent."""
    from jules_cli.client import JulesAPIClient
    from jules_cli.formatter import OutputFormatter

    api_key = ctx.obj.get("actual_api_key")
    if not api_key:
        click.echo("Error: API key not found. Use --api-key, JULES_API_KEY env var, or 'jules config init'", err=True)
        sys.exit(1)

    if message is None:
        message = sys.stdin.read()

    try:
        client = JulesAPIClient(api_key=api_key, verbose=ctx.obj.get("verbose", False))
        formatter = OutputFormatter(ctx.obj.get("format", "plain"))

        data = client.send_message(session_id, message)
        output = formatter.format_message_response(data)
        click.echo(output)

    except JulesAPIError as e:
        formatter = OutputFormatter(ctx.obj.get("format", "plain"))
        error_output = formatter.format_error(str(e))
        click.echo(error_output, err=True)
        sys.exit(1)


@cli.group()
@click.pass_context
def config(ctx):
    """Manage configuration."""
    pass


@config.command("init")
@click.option("--api-key", prompt=True, hide_input=True, help="API key")
@click.option(
    "--format",
    type=click.Choice(["json", "table", "plain"], case_sensitive=False),
    default="plain",
    prompt=True,
    help="Default output format",
)
@click.pass_context
def config_init(ctx, api_key, format):
    """Initialize configuration file."""
    try:
        config_manager = ConfigManager()
        config_manager.init_config(api_key=api_key, format=format.lower())
        config_path = config_manager.config_file
        click.echo(f"Configuration initialized: {config_path}")
    except Exception as e:
        click.echo(f"Error initializing configuration: {e}", err=True)
        sys.exit(1)
