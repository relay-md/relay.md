# -*- coding: utf-8 -*-

from datetime import datetime

from fastapi import APIRouter, Depends, Form, Request, status
from starlette.responses import RedirectResponse

from ..config import Settings, get_config
from ..database import Session, get_session
from ..exceptions import BadRequest, NotAllowed
from ..models.billing import OrderItem, PersonalInformation
from ..repos.billing import InvoiceRepo
from ..repos.team import Team, TeamRepo
from ..templates import templates
from ..utils.pricing import get_price
from ..utils.user import User, require_user

router = APIRouter(prefix="/teams/billing")


@router.post("/plan")
async def team_billing_post(
    request: Request,
    config: Settings = Depends(get_config),
    type: str = Form(default="public"),
    yearly: bool = Form(default=False),
    team_name: str = Form(default=""),
    user: User = Depends(require_user),
    db: Session = Depends(get_session),
):
    team_repo = TeamRepo(db)

    if not team_name:
        return RedirectResponse(
            url=request.url_for("pricing"),
            status_code=status.HTTP_302_FOUND,
        )

    team_name = team_name.lower()
    if not Team.validate_team_name(team_name):
        raise BadRequest(
            "The team name is invalid! Alphanumeric names only (a-z, 0-9 and _)"
        )

    # check if team exists owned by user
    team = team_repo.get_by_kwargs(name=team_name)
    if team and team.user_id != user.id:
        raise NotAllowed("This team exists already and it is not yours!")

    if not team:
        team = team_repo.create_from_kwargs(name=team_name, user_id=user.id)

    if type == "private":
        # make the team private (or rather, non public)
        team_repo.update(team, public_permissions=0)
    else:
        return RedirectResponse(
            url=request.url_for("settings", team_name=team_name),
            status_code=status.HTTP_302_FOUND,
        )
    price_total = get_price(yearly=yearly, private=True)
    if yearly:
        price_interval = "yearly"
    else:
        price_interval = "monthly"
    return templates.TemplateResponse("billing.pug", context=dict(**locals()))


@router.post("/payment/new")
async def team_billing_payment(
    request: Request,
    config: Settings = Depends(get_config),
    user: User = Depends(require_user),
    db: Session = Depends(get_session),
    # Form payload
    type: str = Form(default="public"),
    yearly: bool = Form(default=False),
    team_name: str = Form(default=""),
    address_line1: str = Form(default=""),
    address_line2: str = Form(default=""),
    city: str = Form(default=""),
    zip: str = Form(default=""),
    state: str = Form(default=""),
    country_code: str = Form(default=""),
    phone_country_code: str = Form(default=""),
    phone: str = Form(default=""),
):
    team_repo = TeamRepo(db)

    # check if team exists owned by user
    team = team_repo.get_by_kwargs(name=team_name)
    if team and team.user_id != user.id:
        raise NotAllowed("This team exists already and it is not yours!")

    price_total = get_price(yearly=yearly, private=True)
    if yearly:
        quantity = 12
        stripe_key = "team-yearly"
    else:
        quantity = 1
        stripe_key = "team-monthly"

    invoice_repo = InvoiceRepo(db)
    products = [
        OrderItem(
            name="Team Subscription",
            quantity=quantity,
            price=int(price_total * 100),
            description=f"Team: {team_name}",
            team_id=team.id,
            stripe_key=stripe_key,
        )
    ]
    person = PersonalInformation(
        name=user.name,
        email=user.email,
        address_line1=address_line1,
        address_line2=address_line2,
        city=city,
        state=state,
        zip=zip,
        country_code=country_code,
        phone_country_code=phone_country_code,
        phone_number=phone,
    )
    datetime.utcnow()
    invoice = invoice_repo.create_from_kwargs(
        user_id=user.id,
        customer=person,
        products=products,
    )

    return RedirectResponse(
        # Pay externally, but seems to not support subscriptions via Ayden
        # url=invoice_repo.get_payment_link(invoice),
        url=request.url_for("payment_invoice", invoice_id=invoice.id),
        status_code=status.HTTP_302_FOUND,
    )
