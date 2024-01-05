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
    sitemap_data = {
        "url": [
            {
                "loc": request.url_for(site),
                "lastmod": datetime.utcnow().isoformat(),
                "changefreq": "daily",
                "priority": 1.0,
            }
            for site in site_map_routes
        ]
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
