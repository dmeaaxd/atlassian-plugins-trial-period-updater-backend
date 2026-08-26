import asyncio
import secrets

from src.database import new_session, setup_database
from src.models.plugins import PluginModel

# (тип, имя файла иконки в icons/, отображаемое имя)
PLUGINS = [
    ("jira", "Timesheets-by-Tempo.png", "Timesheets by Tempo"),
    ("jira", "Canned-Responses-Pro.png", "Canned Responses Pro"),
    ("jira", "Epic-Clone.png", "Epic Clone"),
    ("jira", "Extended-Schemes.png", "Extended Schemes"),
    ("jira", "Message-field.png", "Message field"),
    ("jira", "Time-Tracker-Jira-Time-Reports-&-Project-Dashboard.png", "Time Tracker - Jira Time Reports & Project Dashboard"),
    ("jira", "OKR-Board-for-Jira.png", "OKR Board for Jira"),
    ("jira", "Time-in-status-|-SLA.png", "Time in status | SLA"),
    ("jira", "Extender-for-Jira.png", "Extender for Jira"),
    ("jira", "Elements-Copy-&-Sync.png", "Elements Copy & Sync"),
    ("jira", "Custom-Field-Toolbox.png", "Custom Field Toolbox"),
    ("jira", "Zephyr-Scale.png", "Zephyr Scale"),
    ("jira", "sumUp-for-Jira.png", "sumUp for Jira"),
    ("confluence", "Aura-Content.png", "Aura Content"),
    ("confluence", "Easy-Forms-for-Confluence.png", "Easy Forms for Confluence"),
    ("confluence", "MultiExcerpt.png", "MultiExcerpt"),
    ("confluence", "Smart-Terms-for-Confluence.png", "Smart Terms for Confluence"),
    ("confluence", "Comala-Publishsing.png", "Comala Publishsing"),
]


async def seed() -> None:
    await setup_database()

    async with new_session() as session:
        for plugin_type, icon, name in PLUGINS:
            session.add(
                PluginModel(
                    name=name,
                    type=plugin_type.upper(),
                    image_hard_path=f"icons/{plugin_type}_plugins/{icon}",
                    api_key=secrets.token_hex(96),
                )
            )
        await session.commit()


if __name__ == "__main__":
    asyncio.run(seed())
    print(f"Seeded {len(PLUGINS)} plugins")
