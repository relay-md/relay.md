# -*- coding: utf-8 -*-


from datetime import datetime

from fastapi import APIRouter, Depends, Form, Query, Request, status
from fastapi.responses import PlainTextResponse
from starlette.responses import RedirectResponse

from ..config import Settings, get_config
from ..database import Session, get_session
from ..exceptions import NotAllowed
from ..models.billing import OrderItem, PersonalInformation
from ..models.permissions import Permissions
from ..repos.billing import InvoiceRepo
from ..repos.team import TeamRepo
from ..repos.user import UserRepo
from ..templates import templates
from ..utils.pricing import get_price
from ..utils.user import User, require_user

router = APIRouter(prefix="/teams")


@router.get("")
async def get_teams(
    request: Request,
    config: Settings = Depends(get_config),
    db: Session = Depends(get_session),
    user: User = Depends(require_user),
):
    user_repo = UserRepo(db)
    team_repo = TeamRepo(db)
    teams = team_repo.list()
    return templates.TemplateResponse(
        "teams.pug", context=dict(**locals(), Permissions=Permissions)
    )


@router.get("/new")
async def team_create(
    request: Request,
    type: str = Query(default="public"),
    yearly: bool = Query(default=False),
    config: Settings = Depends(get_config),
    user: User = Depends(require_user),
    db: Session = Depends(get_session),
):
    return templates.TemplateResponse("pricing.pug", context=dict(**locals()))


@router.post("/new/validate-team-name", response_class=PlainTextResponse)
async def team_create_validate_team_name(
    request: Request,
    team_name: str = Form(default=""),
    config: Settings = Depends(get_config),
    user: User = Depends(require_user),
    db: Session = Depends(get_session),
):
    team_repo = TeamRepo(db)
    if team_repo.team_name_search(team_name.lower()):
        return """<p class="help is-danger">A Team with this name already exists!</p>"""
    else:
        return ""


@router.post("/billing/plan")
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


@router.post("/billing/payment")
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
