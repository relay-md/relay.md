# -*- coding: utf-8 -*-

import io
from datetime import datetime

import xmltodict
from fastapi import APIRouter, Depends, Request
from fastapi.responses import StreamingResponse

from backend.database import Session, get_session
from backend.repos.document import DocumentRepo

router = APIRouter(prefix="")
site_map_routes = [
    "contact",
    "news",
    "welcome",
    "obsidian_plugin",
    "relay_basics",
    "tos",
    "pricing",
]


def generate_sitemap(request: Request, db: Session = Depends(get_session)):
    document_repo = DocumentRepo(db)
    news_documents = document_repo.latest_news(size=50)

    # Retrieve the list of URLs to include in the sitemap
    lastmod = datetime.utcnow()
    urls = [
        {
            "loc": request.url_for(site),
            "lastmod": lastmod.strftime("%Y-%m-%d"),
            "changefreq": "weekly",
            "priority": 1.0,
        }
        for site in site_map_routes
    ]
    for document in news_documents:
        urls.append(
            {
                "loc": request.url_for("get_document_from_id", id=str(document.id)),
                "lastmod": lastmod.strftime("%Y-%m-%d"),
                "changefreq": "weekly",
                "priority": 1.0,
            }
        )
    sitemap_data = {
        "@xmlns": "http://www.sitemaps.org/schemas/sitemap/0.9",
        "@xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
        "@xsi:schemaLocation": "http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd",
        "url": urls,
    }

    # Convert the data to XML string
    xml_string = xmltodict.unparse(dict(urlset=sitemap_data), pretty=True)

    # Create a StreamingResponse for efficient content transfer
    response = StreamingResponse(
        io.BytesIO(xml_string.encode("utf-8")),
        media_type="application/xml",
        headers={"Content-Disposition": "attachment; filename=sitemap.xml"},
    )

    return response


@router.get("/sitemap.xml")
async def generate_sitemap_endpoint(
    sitemap: str = Depends(generate_sitemap),
):
    return sitemap
