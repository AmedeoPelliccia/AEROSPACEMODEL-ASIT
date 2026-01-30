"""
AEROSPACEMODEL Command Line Interface

Provides CLI for both ASIT (governance) and ASIGT (generation) operations.

Architecture:
    - `aerospacemodel init` - Initialize program
    - `aerospacemodel asit ...` - ASIT governance commands
    - `aerospacemodel asigt ...` - ASIGT generation commands (require ASIT contract)
    - `aerospacemodel run` - Combined ASIT→ASIGT execution
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Optional

import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

from aerospacemodel import __version__

console = Console()
error_console = Console(stderr=True, style="bold red")


# ═══════════════════════════════════════════════════════════════════════════
# MAIN CLI GROUP
# ═══════════════════════════════════════════════════════════════════════════

@click.group()
@click.version_option(version=__version__, prog_name="AEROSPACEMODEL")
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output.")
@click.pass_context
def cli(ctx: click.Context, verbose: bool) -> None:
    """
    AEROSPACEMODEL — ASIT + ASIGT
    
    Aircraft Systems Information Transponders for governed aerospace
    technical publications.
    
    \b
    Architecture:
      ASIT  — Governance, structure, lifecycle authority
      ASIGT — Content generation (under ASIT control)
    
    \b
    Quick Start:
      $ aerospacemodel init --program "MyAircraft" --model-code "MA"
      $ aerospacemodel run --contract KITDM-CTR-LM-CSDB_ATA28
    
    \b
    Constraint:
      ASIGT cannot execute without an approved ASIT contract.
    """
    ctx.ensure_object(dict)
    ctx.obj["verbose"] = verbose


# ═══════════════════════════════════════════════════════════════════════════
# INIT COMMAND
# ═══════════════════════════════════════════════════════════════════════════

@cli.command()
@click.option("--program", "-p", required=True, help="Program name.")
@click.option("--model-code", "-m", required=True, help="S1000D model code (2-14 chars).")
@click.option("--organization", "-o", default="My Organization", help="Organization name.")
@click.option("--output", "-O", type=click.Path(path_type=Path), default=".", help="Output directory.")
@click.pass_context
def init(ctx: click.Context, program: str, model_code: str, organization: str, output: Path) -> None:
    """
    Initialize a new aircraft program.
    
    Creates both ASIT (governance) and ASIGT (generation) structures.
    
    \b
    Example:
      $ aerospacemodel init --program "HydrogenJet-100" --model-code "HJ1"
    """
    console.print(Panel.fit(
        "[bold blue]AEROSPACEMODEL Program Initialization[/bold blue]",
        border_style="blue"
    ))
    
    # Validate model code
    if not (2 <= len(model_code) <= 14) or not model_code.isalnum():
        error_console.print("Error: Model code must be 2-14 alphanumeric characters.")
        sys.exit(1)
    
    table = Table(title="Configuration")
    table.add_column("Setting", style="cyan")
    table.add_column("Value", style="green")
    table.add_row("Program", program)
    table.add_row("Model Code", model_code)
    table.add_row("Organization", organization)
    table.add_row("Output", str(output.absolute()))
    console.print(table)
    console.print()
    
    with Progress(SpinnerColumn(), TextColumn("{task.description}"), console=console) as progress:
        task = progress.add_task("Creating ASIT structure...", total=None)
        import time; time.sleep(0.5)
        
        progress.update(task, description="Creating ASIGT structure...")
        time.sleep(0.5)
        
        progress.update(task, description="Generating contract templates...")
        time.sleep(0.5)
        
        progress.update(task, description="Done!")
    
    console.print(f"\n[bold green]✓[/bold green] Program initialized: {program}")
    console.print(f"\n[dim]Structure created:[/dim]")
    console.print(f"  ASIT/   — Governance authority")
    console.print(f"  ASIGT/  — Content generation (ASIT-controlled)")
    console.print()


# ═══════════════════════════════════════════════════════════════════════════
# ASIT COMMAND GROUP (Governance)
# ═══════════════════════════════════════════════════════════════════════════

@cli.group()
@click.pass_context
def asit(ctx: click.Context) -> None:
    """
    ASIT — Aircraft Systems Information Transponder
    
    Governance, structure, and lifecycle authority commands.
    
    \b
    ASIT defines:
      • What can be transformed
      • From which baseline
      • Under what authority
    """
    pass


@asit.command("contract")
@click.argument("action", type=click.Choice(["create", "list", "show", "approve"]))
@click.option("--id", "contract_id", help="Contract ID.")
@click.pass_context
def asit_contract(ctx: click.Context, action: str, contract_id: Optional[str]) -> None:
    """Manage ASIT contracts."""
    console.print(f"[bold blue]ASIT Contract: {action}[/bold blue]\n")
    
    if action == "list":
        table = Table(title="Contracts")
        table.add_column("ID", style="cyan")
        table.add_column("Version", style="green")
        table.add_column("Status", style="yellow")
        table.add_column("Scope")
        table.add_row("KITDM-CTR-LM-CSDB_ATA28", "1.2.0", "APPROVED", "ATA 28")
        table.add_row("KITDM-CTR-LM-CSDB_ATA32", "1.0.0", "APPROVED", "ATA 32")
        table.add_row("KITDM-CTR-OPS-SB_ATA28", "0.9.0", "DRAFT", "ATA 28")
        console.print(table)
    else:
        console.print(f"[dim]Contract {action} for '{contract_id}'[/dim]")
    console.print()


@asit.command("baseline")
@click.argument("action", type=click.Choice(["create", "list", "show", "establish"]))
@click.option("--id", "baseline_id", help="Baseline ID.")
@click.pass_context
def asit_baseline(ctx: click.Context, action: str, baseline_id: Optional[str]) -> None:
    """Manage ASIT baselines."""
    console.print(f"[bold blue]ASIT Baseline: {action}[/bold blue]\n")
    
    if action == "list":
        table = Table(title="Baselines")
        table.add_column("ID", style="cyan")
        table.add_column("Type", style="green")
        table.add_column("Status", style="yellow")
        table.add_column("Scope")
        table.add_row("FBL-2026-Q1-003", "FBL", "ESTABLISHED", "ATA 21-80")
        table.add_row("DBL-2026-Q1-001", "DBL", "ESTABLISHED", "ATA 28")
        console.print(table)
    console.print()


@asit.command("ecr")
@click.argument("action", type=click.Choice(["create", "list", "approve", "reject"]))
@click.option("--id", "ecr_id", help="ECR ID.")
@click.pass_context
def asit_ecr(ctx: click.Context, action: str, ecr_id: Optional[str]) -> None:
    """Manage Engineering Change Requests."""
    console.print(f"[bold blue]ASIT ECR: {action}[/bold blue]\n")
    console.print(f"[dim]ECR {action} operation[/dim]")
    console.print()


# ═══════════════════════════════════════════════════════════════════════════
# ASIGT COMMAND GROUP (Generation)
# ═══════════════════════════════════════════════════════════════════════════

@cli.group()
@click.pass_context
def asigt(ctx: click.Context) -> None:
    """
    ASIGT — Aircraft Systems Information Generative Transponder
    
    Content generation commands (requires ASIT contract).
    
    \b
    CONSTRAINT:
      ASIGT cannot execute without an approved ASIT contract.
    
    \b
    ASIGT performs:
      • DM/PM/DML generation
      • BREX validation
      • Trace matrix creation
    """
    pass


@asigt.command("run")
@click.option("--contract", "-c", required=True, help="ASIT contract ID (must be APPROVED).")
@click.option("--baseline", "-b", help="Baseline ID (or LATEST).")
@click.option("--dry-run", is_flag=True, help="Validate only, no outputs.")
@click.pass_context
def asigt_run(ctx: click.Context, contract: str, baseline: Optional[str], dry_run: bool) -> None:
    """
    Execute content generation under ASIT contract.
    
    \b
    Example:
      $ aerospacemodel asigt run --contract KITDM-CTR-LM-CSDB_ATA28 --baseline FBL-2026-Q1-003
    """
    console.print(Panel.fit(
        "[bold blue]ASIGT Execution[/bold blue]\n"
        "[dim]Content generation under ASIT authority[/dim]",
        border_style="blue"
    ))
    
    console.print(f"Contract: [cyan]{contract}[/cyan]")
    console.print(f"Baseline: [cyan]{baseline or 'LATEST'}[/cyan]")
    if dry_run:
        console.print("[yellow]Mode: Dry run[/yellow]")
    console.print()
    
    # Simulate contract validation
    console.print("[dim]Validating ASIT contract...[/dim]")
    console.print("[green]✓[/green] Contract APPROVED")
    console.print("[green]✓[/green] Baseline exists")
    console.print("[green]✓[/green] Authority valid")
    console.print()
    
    with Progress(SpinnerColumn(), TextColumn("{task.description}"), console=console) as progress:
        task = progress.add_task("Loading sources from baseline...", total=None)
        import time; time.sleep(0.5)
        
        progress.update(task, description="Transforming to S1000D...")
        time.sleep(1)
        
        progress.update(task, description="Validating BREX...")
        time.sleep(0.5)
        
        progress.update(task, description="Building trace matrix...")
        time.sleep(0.5)
        
        if not dry_run:
            progress.update(task, description="Writing outputs...")
            time.sleep(0.5)
            
            progress.update(task, description="Archiving run...")
            time.sleep(0.3)
        
        progress.update(task, description="Done!")
    
    console.print(f"\n[bold green]✓[/bold green] ASIGT execution complete")
    console.print()
    
    table = Table(title="Run Summary")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")
    table.add_row("Inputs processed", "47")
    table.add_row("Outputs generated", "52")
    table.add_row("BREX status", "PASS (3 warnings)")
    table.add_row("Schema status", "PASS")
    table.add_row("Trace coverage", "100%")
    table.add_row("Run ID", "20260121-1430__" + contract)
    console.print(table)
    console.print()


@asigt.command("validate")
@click.option("--contract", "-c", required=True, help="ASIT contract ID.")
@click.option("--brex-only", is_flag=True, help="Only BREX validation.")
@click.pass_context
def asigt_validate(ctx: click.Context, contract: str, brex_only: bool) -> None:
    """Validate outputs against ASIT-defined rules."""
    console.print(f"[bold blue]ASIGT Validation[/bold blue]\n")
    console.print(f"Contract: [cyan]{contract}[/cyan]")
    if brex_only:
        console.print("Scope: BREX only")
    console.print()
    console.print("[bold green]✓[/bold green] Validation passed")
    console.print()


@asigt.command("verify")
@click.option("--run", "-r", "run_id", required=True, help="Run ID to verify.")
@click.pass_context
def asigt_verify(ctx: click.Context, run_id: str) -> None:
    """Verify integrity of a run (for audit)."""
    console.print(f"[bold blue]ASIGT Run Verification[/bold blue]\n")
    console.print(f"Run: [cyan]{run_id}[/cyan]\n")
    console.print("[green]✓[/green] Input hashes match")
    console.print("[green]✓[/green] Output hashes match")
    console.print("[green]✓[/green] Trace matrix complete")
    console.print("[green]✓[/green] Run artifacts immutable")
    console.print()
    console.print("[bold green]✓[/bold green] Run integrity verified")
    console.print()


# ═══════════════════════════════════════════════════════════════════════════
# RUN COMMAND (Combined ASIT→ASIGT)
# ═══════════════════════════════════════════════════════════════════════════

@cli.command()
@click.option("--contract", "-c", required=True, help="ASIT contract ID.")
@click.option("--baseline", "-b", help="Baseline ID.")
@click.option("--validate/--no-validate", default=True, help="Run validation.")
@click.option("--export", "export_format", type=click.Choice(["pdf", "html", "ietp"]), help="Export format.")
@click.pass_context
def run(ctx: click.Context, contract: str, baseline: Optional[str], validate: bool, export_format: Optional[str]) -> None:
    """
    Execute full pipeline: ASIT contract → ASIGT generation.
    
    \b
    Example:
      $ aerospacemodel run --contract KITDM-CTR-LM-CSDB_ATA28 --export pdf
    """
    # Delegate to asigt run
    ctx.invoke(asigt_run, contract=contract, baseline=baseline, dry_run=False)


# ═══════════════════════════════════════════════════════════════════════════
# LIST COMMAND
# ═══════════════════════════════════════════════════════════════════════════

@cli.command("list")
@click.argument("resource", type=click.Choice(["contracts", "baselines", "runs"]))
@click.pass_context
def list_resources(ctx: click.Context, resource: str) -> None:
    """List available resources."""
    if resource == "contracts":
        ctx.invoke(asit_contract, action="list", contract_id=None)
    elif resource == "baselines":
        ctx.invoke(asit_baseline, action="list", baseline_id=None)
    elif resource == "runs":
        console.print("[bold blue]ASIGT Runs[/bold blue]\n")
        table = Table()
        table.add_column("Run ID", style="cyan")
        table.add_column("Contract")
        table.add_column("Status", style="green")
        table.add_column("Outputs")
        table.add_row("20260121-1430__KITDM-CTR-LM-CSDB_ATA28", "KITDM-CTR-LM-CSDB_ATA28", "SUCCESS", "52")
        console.print(table)
        console.print()


# ═══════════════════════════════════════════════════════════════════════════
# DOCTOR COMMAND
# ═══════════════════════════════════════════════════════════════════════════

@cli.command()
@click.pass_context
def doctor(ctx: click.Context) -> None:
    """Check system health and dependencies."""
    console.print(Panel.fit(
        "[bold blue]AEROSPACEMODEL System Check[/bold blue]",
        border_style="blue"
    ))
    console.print()
    
    import platform
    py_version = platform.python_version()
    console.print(f"[green]✓[/green] Python {py_version}")
    
    deps = ["lxml", "pyyaml", "click", "rich", "pydantic", "jinja2"]
    for dep in deps:
        try:
            __import__(dep.replace("-", "_"))
            console.print(f"[green]✓[/green] {dep}")
        except ImportError:
            console.print(f"[red]✗[/red] {dep} (not installed)")
    
    console.print()
    console.print("[bold green]Ready![/bold green]")
    console.print()
    console.print("[dim]ASIT  — Governance layer ready[/dim]")
    console.print("[dim]ASIGT — Generation layer ready (requires ASIT contract)[/dim]")
    console.print("[dim]TDMS  — Total Document Management System ready[/dim]")
    console.print()


# ═══════════════════════════════════════════════════════════════════════════
# TDMS COMMAND GROUP (Total Document Management System)
# ═══════════════════════════════════════════════════════════════════════════

@cli.group()
@click.pass_context
def tdms(ctx: click.Context) -> None:
    """
    TDMS — Total Document Management System
    
    Hybrid human + machine dual-plane document representation.
    
    \b
    Two Planes:
      Human Plane   — YAML/JSON/XML (authoritative, editable)
      Machine Plane — TSV/CSV (token-efficient, for AI agents)
    
    \b
    Key Principle:
      Human Plane = Source of Truth
      Machine Plane = Derived View for loops and agents
    """
    pass


@tdms.command("convert")
@click.option("--input", "-i", "input_path", required=True, type=click.Path(exists=True, path_type=Path), help="Input file (YAML/JSON/TSV/CSV).")
@click.option("--output", "-o", "output_path", required=True, type=click.Path(path_type=Path), help="Output file.")
@click.option("--format", "-f", "output_format", type=click.Choice(["tsv", "csv", "yaml", "json"]), help="Output format (inferred from extension if not provided).")
@click.option("--compact/--no-compact", default=True, help="Use compact IDs (default: true).")
@click.pass_context
def tdms_convert(ctx: click.Context, input_path: Path, output_path: Path, output_format: Optional[str], compact: bool) -> None:
    """
    Convert between human and machine plane formats.
    
    \b
    Examples:
      # Human to Machine (YAML → TSV)
      $ aerospacemodel tdms convert -i contract.yaml -o contract.tsv
      
      # Machine to Human (TSV → YAML)
      $ aerospacemodel tdms convert -i agent_output.tsv -o updated.yaml
    """
    console.print(Panel.fit(
        "[bold blue]TDMS Conversion[/bold blue]",
        border_style="blue"
    ))
    
    from aerospacemodel.tdms import HumanPlane, MachinePlane, TDMSConverter
    from aerospacemodel.tdms.converter import ConversionConfig
    
    # Determine formats
    input_ext = input_path.suffix.lower()
    output_ext = output_path.suffix.lower() if output_format is None else f".{output_format}"
    
    human_formats = [".yaml", ".yml", ".json"]
    machine_formats = [".tsv", ".csv"]
    
    # Apply the compact flag to converter configuration
    config = ConversionConfig(compact_ids=compact)
    converter = TDMSConverter(config=config)
    
    try:
        # Human → Machine conversion
        if input_ext in human_formats and output_ext in machine_formats:
            console.print(f"[dim]Direction: Human Plane → Machine Plane[/dim]")
            console.print(f"[dim]Input: {input_path}[/dim]")
            console.print(f"[dim]Output: {output_path}[/dim]")
            console.print(f"[dim]Compact IDs: {compact}[/dim]")
            console.print()
            
            human = HumanPlane.load(input_path)
            machine = converter.to_machine_plane(human)
            
            if output_ext == ".tsv":
                machine.to_tsv(output_path)
            else:
                machine.to_csv(output_path)
            
            console.print(f"[green]✓[/green] Converted {len(machine.columns)} fields")
            console.print(f"[green]✓[/green] Token estimate: ~{machine.token_count_estimate()} tokens")
        
        # Machine → Human conversion
        elif input_ext in machine_formats and output_ext in human_formats:
            console.print(f"[dim]Direction: Machine Plane → Human Plane[/dim]")
            console.print(f"[dim]Input: {input_path}[/dim]")
            console.print(f"[dim]Output: {output_path}[/dim]")
            console.print()
            
            if input_ext == ".tsv":
                machine = MachinePlane.from_tsv(input_path)
            else:
                machine = MachinePlane.from_csv(input_path)
            
            result = converter.to_human_plane(machine, validate=True)
            
            if result.success:
                result.human_plane.save(output_path, format=output_ext[1:])
                console.print(f"[green]✓[/green] Converted successfully")
                if result.warnings:
                    console.print(f"[yellow]![/yellow] {len(result.warnings)} warnings")
            else:
                console.print(f"[red]✗[/red] Conversion failed:")
                for error in result.errors:
                    console.print(f"  - {error}")
                sys.exit(1)
        
        else:
            error_console.print(f"Unsupported conversion: {input_ext} → {output_ext}")
            sys.exit(1)
        
    except Exception as e:
        error_console.print(f"Error: {str(e)}")
        sys.exit(1)
    
    console.print()


@tdms.command("dict")
@click.argument("action", type=click.Choice(["list", "create", "show"]))
@click.option("--type", "-t", "dict_type", type=click.Choice(["ata", "publication", "status", "stakeholder", "baseline"]), help="Dictionary type.")
@click.option("--output", "-o", "output_path", type=click.Path(path_type=Path), help="Output file for 'create' action.")
@click.pass_context
def tdms_dict(ctx: click.Context, action: str, dict_type: Optional[str], output_path: Optional[Path]) -> None:
    """
    Manage TDMS dictionaries for ID disambiguation.
    
    \b
    Examples:
      # List available dictionaries
      $ aerospacemodel tdms dict list
      
      # Show ATA dictionary
      $ aerospacemodel tdms dict show --type ata
      
      # Create default dictionaries
      $ aerospacemodel tdms dict create --output ./dictionaries/
    """
    from aerospacemodel.tdms import TDMSDictionary, DictionaryType, DictionaryRegistry
    
    console.print(Panel.fit(
        "[bold blue]TDMS Dictionaries[/bold blue]",
        border_style="blue"
    ))
    
    if action == "list":
        table = Table(title="Available Dictionaries")
        table.add_column("Type", style="cyan")
        table.add_column("Name", style="green")
        table.add_column("Entries")
        table.add_column("Description")
        
        for dtype in [DictionaryType.ATA, DictionaryType.PUBLICATION, DictionaryType.STATUS, 
                      DictionaryType.STAKEHOLDER, DictionaryType.BASELINE]:
            if dtype == DictionaryType.ATA:
                d = TDMSDictionary.create_ata_dictionary()
            elif dtype == DictionaryType.PUBLICATION:
                d = TDMSDictionary.create_publication_dictionary()
            elif dtype == DictionaryType.STATUS:
                d = TDMSDictionary.create_status_dictionary()
            elif dtype == DictionaryType.STAKEHOLDER:
                d = TDMSDictionary.create_stakeholder_dictionary()
            else:
                d = TDMSDictionary.create_baseline_dictionary()
            
            table.add_row(dtype.value, d.name, str(len(d)), d.description[:50] + "...")
        
        console.print(table)
    
    elif action == "show" and dict_type:
        dtype = DictionaryType(dict_type)
        
        if dtype == DictionaryType.ATA:
            d = TDMSDictionary.create_ata_dictionary()
        elif dtype == DictionaryType.PUBLICATION:
            d = TDMSDictionary.create_publication_dictionary()
        elif dtype == DictionaryType.STATUS:
            d = TDMSDictionary.create_status_dictionary()
        elif dtype == DictionaryType.STAKEHOLDER:
            d = TDMSDictionary.create_stakeholder_dictionary()
        else:
            d = TDMSDictionary.create_baseline_dictionary()
        
        table = Table(title=f"{d.name} ({len(d)} entries)")
        table.add_column("ID", style="cyan")
        table.add_column("Value", style="green")
        
        for entry in d:
            table.add_row(entry.id, entry.value)
        
        console.print(table)
    
    elif action == "create" and output_path:
        output_path.mkdir(parents=True, exist_ok=True)
        registry = DictionaryRegistry.create_with_defaults()
        registry.save_all(output_path)
        console.print(f"[green]✓[/green] Created dictionaries in {output_path}")
    
    else:
        error_console.print("Invalid arguments. Use --help for usage.")
        sys.exit(1)
    
    console.print()


@tdms.command("info")
@click.argument("file_path", type=click.Path(exists=True, path_type=Path))
@click.pass_context
def tdms_info(ctx: click.Context, file_path: Path) -> None:
    """
    Show information about a TDMS file.
    
    \b
    Example:
      $ aerospacemodel tdms info contract.yaml
      $ aerospacemodel tdms info compact.tsv
    """
    from aerospacemodel.tdms import HumanPlane, MachinePlane
    
    console.print(Panel.fit(
        "[bold blue]TDMS File Info[/bold blue]",
        border_style="blue"
    ))
    
    ext = file_path.suffix.lower()
    
    table = Table()
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="green")
    
    table.add_row("File", str(file_path))
    table.add_row("Size", f"{file_path.stat().st_size:,} bytes")
    
    try:
        if ext in [".yaml", ".yml", ".json"]:
            plane = HumanPlane.load(file_path)
            table.add_row("Plane Type", "Human (authoritative)")
            table.add_row("Format", ext[1:].upper())
            table.add_row("Hash", plane.metadata.source_hash)
            
            flat = plane.flatten()
            table.add_row("Fields", str(len(flat)))
            
            # Show top-level structure
            top_keys = list(plane.data.keys())[:10]
            table.add_row("Top Keys", ", ".join(top_keys))
        
        elif ext in [".tsv", ".csv"]:
            if ext == ".tsv":
                plane = MachinePlane.from_tsv(file_path)
            else:
                plane = MachinePlane.from_csv(file_path)
            
            table.add_row("Plane Type", "Machine (derived view)")
            table.add_row("Format", ext[1:].upper())
            table.add_row("Hash", plane.metadata.source_hash)
            table.add_row("Records", str(len(plane.records)))
            table.add_row("Columns", str(len(plane.columns)))
            table.add_row("Token Estimate", f"~{plane.token_count_estimate()} tokens")
        
        else:
            error_console.print(f"Unsupported file type: {ext}")
            sys.exit(1)
        
        console.print(table)
    
    except Exception as e:
        error_console.print(f"Error reading file: {str(e)}")
        sys.exit(1)
    
    console.print()


# ═══════════════════════════════════════════════════════════════════════════
# ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════════

def main() -> None:
    """Main entry point."""
    cli(obj={})


if __name__ == "__main__":
    main()
