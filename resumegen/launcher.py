#!/usr/bin/env python3
"""
ResumeGen Launcher - Simplified Dual Mode

Modes:
1. Local Script: Install package and run CLI commands
2. Microservice: Docker Compose with HTTP APIs
"""

import subprocess
import sys
from pathlib import Path
import typer

app = typer.Typer(help="ResumeGen Launcher - Choose your deployment mode")


@app.command()
def script():
    """Run in local script mode (CLI commands)"""
    typer.echo("🖥️  Local Script Mode")
    typer.echo("Available commands:")
    typer.echo("  resumegen generate-resume")
    typer.echo("  resumegen generate-cover-letter")
    typer.echo("")
    typer.echo("Run 'resumegen --help' for full options")


@app.command()
def microservice():
    """Start microservice mode (Docker Compose)"""
    typer.echo("🚀 Starting Microservice Mode...")
    typer.echo("Services will be available at:")
    typer.echo("  - Resume API: http://localhost:8000")
    typer.echo("  - PDF Service: http://localhost:3000")
    typer.echo("")

    try:
        # Run docker-compose up
        subprocess.run(["docker-compose", "up", "--build"], check=True)
    except subprocess.CalledProcessError as e:
        typer.echo(f"❌ Failed to start services: {e}", err=True)
        sys.exit(1)
    except FileNotFoundError:
        typer.echo("❌ Docker Compose not found. Please install Docker.", err=True)
        sys.exit(1)


@app.command()
def status():
    """Check the status of both modes"""
    typer.echo("📊 ResumeGen Status")
    typer.echo("")

    # Check if package is installed
    try:
        import resumegen

        typer.echo("✅ Local package: Installed")
    except ImportError:
        typer.echo("❌ Local package: Not installed (run 'pip install -e .')")

    # Check Docker services
    try:
        result = subprocess.run(
            ["docker-compose", "ps", "--services", "--filter", "status=running"],
            capture_output=True,
            text=True,
            check=True,
        )

        if result.stdout.strip():
            typer.echo("✅ Docker services: Running")
            for service in result.stdout.strip().split("\n"):
                typer.echo(f"   - {service}")
        else:
            typer.echo("❌ Docker services: Not running")
    except (subprocess.CalledProcessError, FileNotFoundError):
        typer.echo("❌ Docker services: Not available")


if __name__ == "__main__":
    app()
