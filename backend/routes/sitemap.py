# -*- coding: utf-8 -*-

import io
from datetime import datetime

import xmltodict
from fastapi import APIRouter, Depends, Request
from fastapi.responses import StreamingResponse

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


def generate_sitemap(request: Request):
    # Retrieve the list of URLs to include in the sitemap
    lastmod = datetime.utcnow()
    sitemap_data = {
        "@xmlns": "http://www.sitemaps.org/schemas/sitemap/0.9",
        "@xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
        "@xsi:schemaLocation": "http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd",
        "url": [
            {
                "loc": request.url_for(site),
                "lastmod": lastmod.strftime("%Y-%m-%d"),
                "changefreq": "weekly",
                "priority": 1.0,
            }
            for site in site_map_routes
        ],
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
async def generate_sitemap_endpoint(sitemap: str = Depends(generate_sitemap)):
    return sitemap
