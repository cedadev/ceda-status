import datetime as dt
import json

import click

from . import model


@click.group()
def cli() -> None:
    """Script to help manage entries on the status page."""


@cli.command()
@click.option(
    "--status",
    prompt=True,
    type=click.Choice(list(model.Status.__members__.keys())),
    default=model.Status.DOWN.name,
    help="Current status of this service to be shown to users.",
)
@click.option(
    "--affected-services",
    prompt=True,
    type=str,
    help="Free-text list of services which are affected. E.g. 'sof storage'. Keep it short!",
)
@click.option(
    "--summary",
    prompt=True,
    type=str,
    help="One-list summary of the problem. Keep it short!",
)
@click.option(
    "--details",
    prompt=True,
    type=str,
    help="Longer summary of the problem. Still keep it short!",
)
@click.option(
    "--start-date",
    prompt=True,
    type=click.DateTime(
        formats=[
            "%d/%m/%Y %H:%M",
            "%Y-%m-%d",
            "%Y%m%d",
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%d %H:%M",
        ]
    ),
    # Round down to nearest hour
    default=dt.datetime.now().replace(minute=0, second=0, microsecond=0),
    help="Time this incident will be shown to have started, and time of the first update.",
)
def add_entry(
    status: str,
    affected_services: str,
    start_date: dt.datetime,
    details: str,
    summary: str,
) -> None:
    """Update status.json with an extra incident."""
    # Create a new incident from CLI data.
    update = model.Update(
        date=start_date,
        details=details,
    )
    incident = model.Incident(
        status=model.Status[status].value,
        affectedServices=affected_services,
        summary=summary,
        date=start_date,
        updates=[update],
    )

    # Read in existing file and parse it.
    with open("status.json", "r", encoding="utf-8") as thefile:
        status_file_contents = json.load(thefile)
    status_file_model = model.StatusPage.model_validate(status_file_contents)

    # Add in the new incident.
    status_file_model.root.append(incident)

    # Write the file back.
    with open("status.json", "w", encoding="utf-8") as thefile:
        thefile.write(status_file_model.model_dump_json(indent=2, exclude_none=True))


if __name__ == "__main__":
    cli()
