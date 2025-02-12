# ceda-status

## Introduction

This repo provides the schema and instance document for the JSON-format feed of status information for CEDA and JASMIN services.

It provides the content for:

- the CEDA status page at https://www.ceda.ac.uk/status
- the "Latest Incidents" list displayed in the Message Of The Day (MOTD) login screen on JASMIN `login` & `sci` hosts.

## Setup

To make sure your JSON file is validated when editing, please install the Poetry package in this repository and the corresponding pre-commit hook:

```
poetry install
poetry run pre-commit install
```

Now, the next time you commit any JSON, the pre-commit hook will run. If the change passes the validator then it will commit normally. If not:
- In VS Code, a popup will appear. Press "Show Command Output" to see where the validator failed.
- In your terminal, `git commit` will show the output of the pre-commit hooks.

If you edit the repository directly on the GitHub website, please look out for a green tick next to your commit message or check the Actions tab for the CI status.

## Editing

The JSON content is stored in `status.json` and is fed by the "raw" view at the URL
https://raw.githubusercontent.com/cedadev/ceda-status/main/status.json

The schema file `statuspage.schema.json` is designed to be used in conjunction with the online [Json-Editor](https://pmk65.github.io/jedemov2/dist/demo.html) tool. Hence it includes some configuration for that tool as well as schema rules to validate a `statuspage` JSON document.

The JSON content can be edited manually, but the Json-Editor tool provides useful validation to avoid syntax / structural errors.

Procedure:

- In the environment where you are using this repo, go to the `main` branch and do a `git pull`, to ensure you're starting from the latest version.
- **Option 1**: edit `status.json` manually (but you must follow the schema rules)
- **Option 2**: use the JSON-Editor tool to edit the content with the help of a graphical form & validation against the schema
  - In the JSON-Editor, go to the **Schema** tab and upload or copy/paste the contents of the file `statuspage.schema.json`.
  - Navigate to the **Form** tab, and press "Generate Form" at the top of the page
  - Go to the **Output** tab and copy/paste the content of the current `main` version of `status.json`. Overwrite any content (e.g. the brackets `[]` which may be there by default)
  - Navigate to the "Form" tab
  - Use the form to edit the status content and add new items as needed
  - Navigate to the "Output" tab: the JSON content should be updated with (valid) changes
  - Copy that JSON content back to your own editor as new content for `statuspage.schema.json`
- Committing and pushing your changes to `status.json` in the `main` branch on GitHub means that these changes are made live.
- The CEDA status page at `www.ceda.ac.uk/status` has JQuery code to read the JSON feed from the "raw" URL above.
- A user viewing the status page should now see the updated status content in their browser.

## Content guidance

**PLEASE BE AS TERSE AS POSSIBLE: THERE IS LIMITED SCREEN-SPACE WHEN DISPLAYED IN THE MOTD**

The JSON file can have 0 or more incidents, with each incident having the following fields:

Field | Required | Details | Example
--- | --- | --- | ---
status | yes | Overal current status of the incident | Must be one of `down`, `resolved`, `degraded` or `at risk`.
affectedServices | yes | **Concise** list of affected services | `LOTUS & /gws/nopw/jo4/*` (free text)
summary | yes | Concise summary of the incident (but not its status) | `Issue with storage systems`
date | yes | date/time of **initial report or future planned date** of incident | `2024-03-31T09:00` (locale: en-GB)
updates | at least 1 | see below | |

There should be at least 1 `update`, each having the following:

Field | Required | Details | Example
--- | --- | --- | ---
date | yes | date of the update/report | format as above
details | yes | **Concise** text report | `Issue reported: under investigation`, `Issue now resolved, please report any further issues`, `Planned maintenance`, etc.
url | no | URL of related news item or other info | 

## Content management

- Order of incidents within the JSON file is not significant
  - the CEDA status page orders them by date automatically
  - the MOTD script will order them in order of each incident's most recent update.
- Incidents should be removed after being marked as `resolved` for 5-7 days (enough time for people to take note that they're resolved).
- Future incidents should have an initial update, including date/time corresponding to the planned downtime and a `details` field with initially-expected impact. This can be superceded by subsequent updates.
- Leave the most recent 2-3 `update`s in place on a particular incident (to provide a brief history), unless their continued presence causes confusion (eg. if initial diagnosis / impact was incorrect).
- If you have posted an incident, don't forget to check regularly with the Ops team to get info from them so that you can post updates to the incident.
- Users will see the updates in the terminal environment, so it's important that the information is correct and up-to-date.
