import json
import os
import re
from dataclasses import asdict, dataclass
from typing import List, Optional
from urllib.parse import quote

import requests
from azure.core.exceptions import ClientAuthenticationError
from azure.identity import AzureCliCredential
from dotenv import load_dotenv

load_dotenv()

ADO_API_VERSION = "7.1"
ADO_SCOPE = "499b84ac-1321-4277-99ee-85fc3a0523c2/.default"


@dataclass
class UserStory:
    """Work item fields pulled from Azure DevOps for later use."""

    id: int
    title: str
    description_html: str
    description_plain: str
    priority: Optional[str]
    state: Optional[str]
    iteration_path: Optional[str]
    area_path: Optional[str]
    work_item_type: Optional[str]
    assigned_to: Optional[str]
    tags: Optional[str]

    def combined_text(self) -> str:
        """Title plus plain description (same idea as the previous single string)."""
        if self.description_plain:
            return f"{self.title}\n{self.description_plain}".strip() if self.title else self.description_plain
        return (self.title or "").strip()

    def as_dict(self) -> dict:
        return asdict(self)


def _wiql_string_literal(value: str) -> str:
    return value.replace("'", "''")


def _get_bearer_token() -> str:
    credential = AzureCliCredential()
    try:
        token = credential.get_token(ADO_SCOPE)
    except ClientAuthenticationError as exc:
        raise RuntimeError(
            "Could not get an Azure DevOps token from Azure CLI. "
            "Install the Azure CLI, run `az login`, then try again. "
            f"Details: {exc}"
        ) from exc
    return token.token


def _html_to_plain(html: str) -> str:
    if not html or not isinstance(html, str):
        return ""
    plain = re.sub(r"<[^>]+>", " ", html)
    return re.sub(r"\s+", " ", plain).strip()


def _assigned_to_display(fields: dict) -> Optional[str]:
    v = fields.get("System.AssignedTo")
    if v is None:
        return None
    if isinstance(v, dict):
        return v.get("displayName") or v.get("uniqueName")
    return str(v)


def _fields_to_user_story(work_item_id: int, fields: dict) -> UserStory:
    title = (fields or {}).get("System.Title") or ""
    desc_html = (fields or {}).get("System.Description") or ""
    if not isinstance(desc_html, str):
        desc_html = str(desc_html) if desc_html is not None else ""

    pr = (fields or {}).get("Microsoft.VSTS.Common.Priority")
    priority = str(pr) if pr is not None else None

    return UserStory(
        id=work_item_id,
        title=title,
        description_html=desc_html,
        description_plain=_html_to_plain(desc_html),
        priority=priority,
        state=(fields or {}).get("System.State"),
        iteration_path=(fields or {}).get("System.IterationPath"),
        area_path=(fields or {}).get("System.AreaPath"),
        work_item_type=(fields or {}).get("System.WorkItemType"),
        assigned_to=_assigned_to_display(fields or {}),
        tags=(fields or {}).get("System.Tags"),
    )


def fetch_user_story() -> List[UserStory]:
    """
    Load user stories for the configured iteration using Azure DevOps REST APIs.
    Authentication uses the same identity as `az login` (no PAT).

    Each ``UserStory`` exposes title, description (HTML and plain), priority, state,
    iteration, area, type, assignee, and tags as separate attributes.
    """
    org = os.environ.get("ADO_ORG")
    project = os.environ.get("ADO_PROJECT")
    iteration_path = os.environ.get("ADO_ITERATION_PATH")
    work_item_type = os.environ.get("ADO_WORK_ITEM_TYPE", "User Story")

    if not org or not project or not iteration_path:
        raise ValueError(
            "Set ADO_ORG, ADO_PROJECT, and ADO_ITERATION_PATH (e.g. in .env)."
        )

    token = _get_bearer_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    base = f"https://dev.azure.com/{quote(org.strip(), safe='')}"
    project_enc = quote(project.strip(), safe="")

    wiql_query = (
        "SELECT [System.Id], [System.Title], [System.State], [System.WorkItemType] "
        "FROM workitems "
        f"WHERE [System.WorkItemType] = '{_wiql_string_literal(work_item_type)}' "
        f"AND [System.IterationPath] = '{_wiql_string_literal(iteration_path)}' "
        "ORDER BY [System.Id]"
    )

    wiql_url = f"{base}/{project_enc}/_apis/wit/wiql?api-version={ADO_API_VERSION}"
    wiql_resp = requests.post(
        wiql_url, headers=headers, json={"query": wiql_query}, timeout=120
    )
    wiql_resp.raise_for_status()
    work_refs = wiql_resp.json().get("workItems") or []
    ids = [int(ref["id"]) for ref in work_refs]

    if not ids:
        return []

    results: List[UserStory] = []
    chunk_size = 200

    for i in range(0, len(ids), chunk_size):
        chunk = ids[i : i + chunk_size]
        ids_param = ",".join(str(x) for x in chunk)
        items_url = (
            f"{base}/_apis/wit/workitems"
            f"?ids={ids_param}&$expand=all&api-version={ADO_API_VERSION}"
        )
        items_resp = requests.get(items_url, headers=headers, timeout=120)
        items_resp.raise_for_status()
        by_id = {item["id"]: item for item in (items_resp.json().get("value") or [])}
        for wid in chunk:
            item = by_id.get(wid)
            if not item:
                continue
            fields = item.get("fields") or {}
            results.append(_fields_to_user_story(wid, fields))

    return results


def fetch_user_story_json() -> str:
    """Same as ``fetch_user_story`` but returns JSON for tools / logging."""
    return json.dumps([u.as_dict() for u in fetch_user_story()], indent=2, default=str)
