import datetime as dt
import json

import click
import pydantic.json
import pydantic.tools

from . import model


@click.group()
def cli():
    """Script to help manage entries on the status page."""


@cli.command()
@click.option(
    "--status",
    prompt=True,
    type=click.Choice(model.Status.__members__),
    default=model.Status.DOWN._name_,
    help="Current status of this service to be shown to users.",
)
@click.option(
    "--affected-services",
    prompt=True,
    type=str,
    help="Free-text list of services which are affected. Eg 'sof storage'. Keep it short!",
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
    type=click.DateTime(),
    default=dt.datetime.now(),
    help="Time this incident will be shown to have started, and time of the first update.",
)
def add_entry(
    status: str,
    affected_services: str,
    start_date: dt.datetime,
    details: str,
    summary: str,
):
    """Update status.json with an extra incident."""
    # Create a new incident from CLI data.
    update = model.Update(
        date=str(start_date.strftime(model.INPUT_DATE_FORMAT)),
        details=details,
    )
    incident = model.Incident(
        status=model.Status[status].value,
        affectedServices=affected_services,
        summary=summary,
        date=str(start_date.strftime(model.INPUT_DATE_FORMAT)),
        updates=[update],
    )

    # Read in existing file and parse it.
    with open("status.json", "r", encoding="utf-8") as thefile:
        status_file_contents = json.load(thefile)
    status_file_model = pydantic.tools.parse_obj_as(
        model.StatusPage, status_file_contents
    )

    # Add in the new incident.
    status_file_model.root.append(incident)

    # Write the file back.
    with open("status.json", "w", encoding="utf-8") as thefile:
        thefile.write(status_file_model.model_dump_json(indent=2))


if __name__ == "__main__":
    cli()
